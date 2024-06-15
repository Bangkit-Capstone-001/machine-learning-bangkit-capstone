Updates to keyboard shortcuts … On Thursday, August 1, 2024, Drive keyboard shortcuts will be updated to give you first-letters navigation.Learn more
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://andrafarm.com/_andra.php?_i=daftar-tkpi&jobs=&perhal=4000"
response = requests.get(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
    timeout=10)

soup = BeautifulSoup(response.content, 'html.parser')
tables = soup.find_all('table')
headers_row = tables[17].find_all('th')
headers = [header.text.strip() for header in headers_row]

results = []
rows = tables[17].find_all('tr')[4:-1]
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    results.append(cols)
    print(cols)
print(f"Successfully added {len(rows)} rows of data")

df = pd.DataFrame(results, columns=headers)
df.columns = [
    'no', 'kode', 'nama_bahan_makanan', 'komposisi_air_g', 'komposisi_energi_kal',
    'komposisi_protein_g', 'komposisi_lemak_g', 'komposisi_karbohidrat_g', 'komposisi_serat_g',
    'komposisi_abu_g', 'komposisi_kalsium_mg', 'komposisi_fosfor_mg', 'komposisi_besi_mg',
    'komposisi_natrium_mg', 'komposisi_kalium_mg', 'komposisi_tembaga_mg', 'komposisi_seng_mg',
    'komposisi_vitamin_a_mcg', 'komposisi_beta_karoten_mcg', 'komposisi_karoten_total_mcg',
    'komposisi_vitamin_b1_mg', 'komposisi_vitamin_b2_mg', 'komposisi_vitamin_b3_mg',
    'komposisi_vitamin_c_mg', 'komposisi_bdd_%', 'jenis_bahan_makanan', 'kelompok_makanan',
    'sumber'
]

csv_file_path = "data/Tabel_Komposisi_Pangan_Indonesia_2019.csv"
df.to_csv(csv_file_path, index=False, mode='w')
print(f"CSV file saved to {csv_file_path}")