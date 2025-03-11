import pandas as pd
import json

# Percorso del file CSV
file_path = "pox-usd-max.csv"  # Modifica il percorso del file se necessario

# Leggi il file CSV
data = pd.read_csv(file_path)

# Assicurati che la colonna 'snapped_at' sia trattata come una colonna di date con fuso orario UTC
data['snapped_at'] = pd.to_datetime(data['snapped_at'], errors='coerce', utc=True)

# Definisci il range di date per il filtro
start_date = pd.to_datetime("2024-02-26", utc=True)  # Data di inizio
end_date = pd.to_datetime("2025-02-19", utc=True)    # Data di fine

# Filtra i dati per selezionare solo le righe nell'intervallo di date
filtered_data = data[(data['snapped_at'] >= start_date) & (data['snapped_at'] <= end_date)]

# Lista per salvare i risultati
result = []

# Itera attraverso ogni riga del DataFrame filtrato
for index, row in filtered_data.iterrows():
    # Crea un dizionario per ogni riga usando i nomi delle colonne come chiavi
    row_dict = row.to_dict()
    
    # Converte la data 'snapped_at' nel formato yyyy-mm-dd (solo la data, non l'ora)
    row_dict['snapped_at'] = row_dict['snapped_at'].strftime('%Y-%m-%d')  # Converte la data in stringa

    # Aggiungi il dizionario alla lista dei risultati
    result.append(row_dict)

# Scrivi i risultati nel file JSON
output_file = "mpox_price.json"
with open(output_file, 'w', encoding='utf-8') as f_out:
    json.dump(result, f_out, ensure_ascii=False, indent=4)

# Messaggio di conferma
print(f"File di output scritto in {output_file}")
