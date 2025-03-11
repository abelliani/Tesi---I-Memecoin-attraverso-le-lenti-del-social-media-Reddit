# SCRIPT 1: Estrazione dei selftext con la data da un file JSON

import json
from datetime import datetime

# Specifica il percorso del file JSON da processare
input_file = 'combined_posts_sorted.json'  # Sostituisci con il percorso del tuo file
output_file = 'selftext.json'

# Lista per accumulare i selftext con la data
selftext_list = []

# Funzione per convertire il timestamp in formato 'yyyy-mm-dd'
def convert_utc_to_date(created_utc):
    return datetime.fromtimestamp(created_utc).strftime('%Y-%m-%d')

# Lettura e parsing del file JSON
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

    # Estrazione del campo selftext e della data per ogni elemento
    for item in data:
        if 'selftext' in item and item['selftext']:
            post = {
                'selftext': item['selftext'],
                'created_date': convert_utc_to_date(item.get('created_utc', 0))  # Converti created_utc in data
            }
            selftext_list.append(post)

# Scrittura dei selftext con la data in un file JSON di output
with open(output_file, 'w', encoding='utf-8') as out_file:
    json.dump(selftext_list, out_file, ensure_ascii=False, indent=4)

print(f"I selftext con la data sono stati salvati in {output_file}.")
