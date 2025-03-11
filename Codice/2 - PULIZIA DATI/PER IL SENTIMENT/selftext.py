# PRIMO SCRIPT

import json
import os

# Directory contenente i file JSON
input_directory = './'  # Sostituisci con il percorso della tua directory
output_file = 'selftext.json'

# Lista per accumulare i selftext
selftext_list = []

# Iterazione su tutti i file nella directory
for filename in os.listdir(input_directory):
    if filename.endswith('.json'):  # Considera solo file con estensione .json
        filepath = os.path.join(input_directory, filename)
        
        # Lettura e parsing del file JSON
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Estrazione del campo selftext per ogni elemento
            for item in data:
                if 'selftext' in item and item['selftext']:
                    selftext_list.append(item['selftext'])

# Scrittura dei selftext in un file JSON di output
with open(output_file, 'w', encoding='utf-8') as out_file:
    json.dump(selftext_list, out_file, ensure_ascii=False, indent=4)

print(f"I selftext estratti sono stati salvati in {output_file}.")