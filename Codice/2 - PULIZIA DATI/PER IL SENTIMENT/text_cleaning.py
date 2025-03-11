# SECONDO SCRIPT

import json
import re
import html

# 1. Caricare il file JSON
def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

# 2. Rimuovere gli URL
def remove_urls(text):
    return re.sub(r'http\S+', '', text)

# 3. Rimuovere entità HTML
def remove_html_entities(text):
    return html.unescape(text)

# 4. Rimuovere righe vuote o blocchi di spazi
def remove_empty_blocks(text):
    return re.sub(r'\s+', ' ', text).strip()

# 5. Rimuovere simboli markdown inutili come `**`
def remove_markdown_symbols(text):
    return re.sub(r'\*\*', '', text)

# 6. Convertire il testo in minuscolo
def to_lowercase(text):
    return text.lower()

# 7. Rimuovere ritorni a capo e sostituirli con uno spazio
def remove_carriage_return(text):
    return text.replace('\n', ' ')

# 8. Pulizia completa dei dati
def clean_data(data):
    cleaned_data = []
    for entry in data:
        entry = remove_urls(entry)  # Rimuove gli URL
        entry = remove_html_entities(entry)  # Rimuove entità HTML
        entry = remove_markdown_symbols(entry)  # Rimuove simboli markdown
        entry = remove_carriage_return(entry)  # Rimuove i ritorni a capo
        entry = remove_empty_blocks(entry)  # Rimuove blocchi vuoti
        entry = to_lowercase(entry)  # Converte in minuscolo
        cleaned_data.append(entry)  # Aggiunge il commento pulito alla lista
    return cleaned_data

# 9. Salvare i dati puliti in un nuovo file di testo (.txt)
def save_cleaned_data(cleaned_data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for entry in cleaned_data:
            file.write(entry + "\n")  # Scrive ogni commento su una nuova riga

# 10. Main
if __name__ == "__main__":
    input_filename = "selftext.json"  # Sostituisci con il nome del tuo file JSON
    data = load_json(input_filename)

    # Assicurati che 'data' sia una lista di stringhe (commenti)
    # Se il tuo JSON contiene una struttura complessa, estrai la lista dei commenti
    # Ad esempio, se i commenti sono in "data['comments']", puoi fare:
    # data = data['comments']

    # Pulisci i dati
    cleaned_data = clean_data(data)

    # Salva i dati puliti in un nuovo file txt
    output_filename = "cleaned_data.txt"  # Nuovo file txt di output
    save_cleaned_data(cleaned_data, output_filename)

    print(f"Dati puliti salvati in {output_filename}")
