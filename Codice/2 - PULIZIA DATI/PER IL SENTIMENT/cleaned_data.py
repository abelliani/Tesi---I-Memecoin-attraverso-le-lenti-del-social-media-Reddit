# TERZO SCRIPT

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

# Leggi il file di input
def load_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

# Salva il testo pulito in un file
def save_cleaned_text(cleaned_data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in cleaned_data:
            f.write(line + '\n')

if __name__ == "__main__":
    input_file = "cleaned_data.txt"  # Sostituisci con il tuo file di input
    output_file = "cleaned_text.txt"  # Nome del file di output

    # Carica il testo
    raw_data = load_text_file(input_file)

    # Pulisci ogni post mantenendo la suddivisione
    cleaned_data = [clean_text(line) for line in raw_data]

    # Salva i risultati
    save_cleaned_text(cleaned_data, output_file)
    print(f"Testo pulito salvato in: {output_file}")
