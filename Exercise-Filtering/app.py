import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load workout data (Excel File)
workout_data_body_only = pd.read_excel('../datasets/gym-exercises/Body Only.xlsx')
workout_data_minimal_equipment = pd.read_excel('../datasets/gym-exercises/Minimal Equipment.xlsx')
workout_data_full_equipment = pd.read_excel('../datasets/gym-exercises/Full Gym Equipment.xlsx')

def load_data(exercise_option):
    if exercise_option == "Body Only":
        return workout_data_body_only
    elif exercise_option == "Minimal Equipment":
        return workout_data_minimal_equipment
    elif exercise_option == "Full Gym Equipment":
        return workout_data_full_equipment

def process_data(workout_data, body_group):
    workout_data = workout_data.drop(columns=["guide_img_url", "youtube_links", "youtube_title"])
    
    if body_group == "Upper Body":
        workout_data = workout_data[workout_data['body_group'] == "Upper"]
    elif body_group == "Lower Body":
        workout_data = workout_data[workout_data['body_group'] == "Lower"]
    
    workout_data = workout_data.reset_index(drop=True)
    workout_data['combined_features'] = workout_data['short_description'] + ' ' + workout_data['instructions'].astype(str)
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(workout_data['combined_features'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    return workout_data, cosine_sim

def predict(user_favorites, workout_data, cosine_sim):
    indices = pd.Series(workout_data.index, index=workout_data['exercise_name'])
    
    sim_scores = []
    for workout in user_favorites:
        users_favorites_db = workout_data[workout_data['exercise_name'].str.contains(workout, case=False, na=False)]
        
        if not users_favorites_db.empty:
            for workout in users_favorites_db['exercise_name']:
                idx = indices[workout]
                sim_scores.append(cosine_sim[idx])
        else:
            print(f"Workout '{workout}' not found in the dataset.")
    
    if not sim_scores:
        return []
    
    sim_scores = sum(sim_scores) / len(sim_scores)
    workout_indices = sim_scores.argsort()[::-1]
    similarity_scores_table = workout_data.iloc[workout_indices].copy()
    non_favorite_workout = [workout for workout in similarity_scores_table['exercise_name'] if workout not in user_favorites]
    similarity_scores_table = similarity_scores_table.drop(columns=["short_description", "instructions", "equipment", "rating", "body_group", "combined_features"], errors='ignore')
    similarity_scores_table['similarity'] = sim_scores[workout_indices]
    similarity_scores_table = similarity_scores_table.sort_values(by='similarity', ascending=False)
    similarity_scores_table = similarity_scores_table[similarity_scores_table['exercise_name'].isin(non_favorite_workout)]
    
    return similarity_scores_table

@app.route('/recommend', methods=['POST'])
def recommend_workouts():
    data = request.get_json()
    body_group = data['body_group']
    exercise_option = data['exercise_option']
    user_favorites = data['user_favorites']
    
    workout_data = load_data(exercise_option)
    workout_data, cosine_sim = process_data(workout_data, body_group)
    recommended_workouts = predict(user_favorites, workout_data, cosine_sim)
    output = recommended_workouts[:10]['exercise_name'].tolist()
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
