# SCRIPT 2: Pulizia dei dati

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

# 8. Pulizia completa dei dati (applicata solo a selftext)
def clean_data(post):
    # Estrai il selftext e la data
    selftext = post.get('selftext', '')
    created_date = post.get('created_date', '')  # Mantieni la data senza modificarla

    # Pulisci il selftext
    selftext = remove_urls(selftext)  # Rimuove gli URL
    selftext = remove_html_entities(selftext)  # Rimuove entità HTML
    selftext = remove_markdown_symbols(selftext)  # Rimuove simboli markdown
    selftext = remove_carriage_return(selftext)  # Rimuove ritorni a capo
    selftext = remove_empty_blocks(selftext)  # Rimuove blocchi vuoti
    selftext = to_lowercase(selftext)  # Converte in minuscolo

    return {
        'selftext': selftext,
        'created_date': created_date  # Mantieni la data originale
    }

# 9. Salvare i dati puliti in un nuovo file JSON
def save_cleaned_data(cleaned_data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(cleaned_data, file, ensure_ascii=False, indent=4)

# 10. Main
if __name__ == "__main__":
    input_filename = "selftext.json"  # Sostituisci con il nome del tuo file JSON
    data = load_json(input_filename)

    # Estrazione e pulizia dei dati
    cleaned_data = [clean_data(post) for post in data]

    # Salva i dati puliti in un nuovo file JSON
    output_filename = "cleaned_data.json"  # Nuovo file JSON di output
    save_cleaned_data(cleaned_data, output_filename)

    print(f"Dati puliti e con la data salvati in {output_filename}")
