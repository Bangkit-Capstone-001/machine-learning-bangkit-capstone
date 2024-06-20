# Machine Learning C241-PS014

# FitFirst-ML

This document contains a comprehensive approach to building a Machine Learning project that consists of two main parts: a workout recommender system and a food image classification system.

## Table of Contents
- [Introduction](#introduction)
- [Datasets](#datasets)
- [Model Architecture](#model-architecture)
- [Training](#training)
- [Evaluation](#evaluation)

## Introduction
FitFirst-ML is designed to provide personalized workout recommendations and accurate food image classification. The project leverages advanced machine learning techniques, including content-based filtering and transfer learning, to deliver these functionalities.

## Datasets
* [Gym Exercises (Workout Recommender)](https://drive.google.com/drive/folders/1GtexsAywKkM57FiDTbUIwEAnydOV9RqL?usp=sharing)
* [Food Images](https://drive.google.com/drive/folders/1HAV1u8pomMbwt6AvNk-LlgW6BSek-x6P?usp=sharing)
* [Indonesian Food Composition Table (IFCT, TKPI)](https://docs.google.com/spreadsheets/d/1Ql38aqKQYH4GM9rvFz7OgGcMRtNSvkIDGXj61djxKic/edit?usp=sharing)

For food image classification, we have 27 classes in total:
1. Ayam Bakar
2. Ayam Geprek
3. Ayam Goreng
4. Bakso
5. Batagor
6. Bebek Goreng
7. Cireng
8. Donut
9. French Fries (Kentang Goreng)
10. Gado - Gado
11. Gulai Kambing
12. Martabak Asin (Martabak Telur)
13. Martabak Manis
14. Mie Ayam 
15. Nasi Goreng
16. Nasi Kuning
17. Pecel Lele
18. Pempek
19. Pizza
20. Rendang
21. Sate Ayam
22. Sop Buntut
23. Soto
24. Tahu Goreng
25. Tekwan
26. Telur Dadar
27. Tempe Goreng

##  Model Architecture

### Workout Recommender
The workout recommender system does not use a traditional machine learning model. Instead, it employs a content-based filtering approach. Feature engineering is applied to combine relevant text data (descriptions and instructions) into a single feature. TF-IDF vectorization is then used to transform the text data and compute cosine similarity scores between the user's favorite exercises and other available exercises. Based on these similarity scores, the system recommends exercises that closely match the user's preferences and past favorites.

###  Food Image Classification
Transfer learning is a widely-used method in deep learning, where a pre-trained model serves as the foundation for a new task. In this project, three different architectures were used for model training: DenseNet121, InceptionV3, and ResNet50V2. After rigorously training and evaluating the models, DenseNet121 achieved the highest accuracy, reaching 86.7% on the validation dataset.

##  Training 
The training process is carefully detailed to ensure reproducibility and high performance. The workout recommender system uses feature engineering and TF-IDF vectorization, while the food image classification models utilize transfer learning with pre-trained architectures.

##  Evaluation
Evaluation of the models is conducted using standard metrics to ensure they meet the expected performance standards. For the workout recommender system, cosine similarity scores are used to evaluate the relevance of recommendations. For the food image classification, accuracy metrics are used to determine the model's performance on the validation dataset.
