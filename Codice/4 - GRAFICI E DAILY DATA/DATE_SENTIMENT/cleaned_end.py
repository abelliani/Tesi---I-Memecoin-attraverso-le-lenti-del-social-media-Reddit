import json
import re

def clean_text(text):
    """
    Pulisce il testo rimuovendo link, caratteri speciali e normalizzando il contenuto.
    """
    # Rimuove link
    text = re.sub(r'http\S+|www\S+|[\(\[].*?[\)\]]', '', text)
    
    # Rimuove caratteri non alfabetici o numerici tranne spazi e punteggiatura di base
    text = re.sub(r'[^a-zA-Z0-9.,!?\'\"\s]', '', text)
    
    # Rimuove spazi multipli
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Normalizza il testo (minuscolo)
    text = text.lower()
    
    return text

# Funzione per caricare il file JSON
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Funzione per salvare i dati puliti in un nuovo file JSON
def save_cleaned_json(cleaned_data, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    input_filename = "cleaned_data.json"  # Sostituisci con il tuo file JSON di input
    output_filename = "cleaned_data_.json"  # Nome del file JSON di output

    # Carica il file JSON
    posts_data = load_json(input_filename)

    # Pulisci ogni post mantenendo i campi 'created_date' e 'selftext'
    cleaned_data = []
    for post in posts_data:
        # Pulisci il 'selftext' se presente
        selftext = post.get('selftext', '')
        cleaned_selftext = clean_text(selftext)
        
        # Mantieni la data originale (presumibilmente già in formato 'yyyy-mm-dd')
        created_date = post.get('created_date')

        # Aggiungi il post pulito con i campi 'created_date' e 'selftext'
        cleaned_data.append({
            'created_date': created_date,
            'selftext': cleaned_selftext
        })

    # Salva i risultati nel nuovo file JSON
    save_cleaned_json(cleaned_data, output_filename)
    
    print(f"Testo pulito salvato in: {output_filename}")
