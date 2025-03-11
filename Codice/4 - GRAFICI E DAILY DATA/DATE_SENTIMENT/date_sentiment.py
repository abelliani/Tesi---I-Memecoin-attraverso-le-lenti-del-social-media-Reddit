import json
from rapidfuzz import fuzz
from collections import defaultdict

# Funzione per caricare il file JSON con una codifica sicura
def load_json_safe(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        return json.load(f)

# Carica i file JSON
sentiment_data = load_json_safe('cryptobert_sentiment.json')
posts_data = load_json_safe('cleaned_data_.json')

# Funzione per normalizzare il testo (opzionale)
def normalize_text(text):
    return text.strip().lower()

# Soglia di similarità per considerare i testi come "uguali"
SIMILARITY_THRESHOLD = 80

# Crea un dizionario con i post basato su una normalizzazione del testo
post_dict = defaultdict(list)
for post in posts_data:
    post_selftext = normalize_text(post['selftext'])
    post_dict[post_selftext].append(post['created_date'])

# Aggiungi la data a ogni post nel sentiment_data
total_comparisons = 0  # Contatore per il numero di confronti effettuati
for sentiment in sentiment_data:
    post_text = normalize_text(sentiment['post'])
    sentiment_found = False  # Flag per indicare se il post è stato trovato

    # Cerchiamo il post corrispondente nel dizionario
    for stored_text, dates in post_dict.items():
        similarity_score = fuzz.ratio(post_text, stored_text)

        total_comparisons += 1  # Incrementa il contatore

        if similarity_score >= SIMILARITY_THRESHOLD:
            # Se la similarità è maggiore o uguale alla soglia, aggiungi la data
            sentiment['created_date'] = dates[0]  # Usato il primo valore se ci sono più corrispondenze
            sentiment_found = True
            break

    # Se il post non è stato trovato, imposta un campo di errore o lascialo vuoto
    if not sentiment_found:
        sentiment['created_date'] = None

    # Stampa il progresso ogni 100 confronti
    if total_comparisons % 100 == 0:
        print(f"Confronti effettuati: {total_comparisons} / {len(sentiment_data) * len(posts_data)}")

# Salva il risultato nel nuovo file JSON
with open('melania_cryptobert_sentiment.json', 'w', encoding='utf-8') as f:
    json.dump(sentiment_data, f, indent=4)

print("Il file con la data è stato salvato come 'melania_cryptobert_sentiment.json'.")
