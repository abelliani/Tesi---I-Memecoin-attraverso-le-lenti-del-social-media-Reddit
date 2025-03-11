from transformers import pipeline, AutoTokenizer
import json

# Carica il modello e il tokenizer
model_name = "ElKulako/cryptobert"
pipe = pipeline("text-classification", model=model_name, truncation=True, max_length=512)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Mappatura delle etichette personalizzate
label_mapping = {
    "Bearish": "bearish",
    "Neutral": "neutral",
    "Bullish": "bullish"
}

# Funzione per suddividere un testo in segmenti basati sul numero massimo di token senza spezzare frasi
def split_text_into_segments(text, max_length=512):  
    sentences = text.split('.')  # Divide il testo in frasi
    segments = []
    current_segment = ""

    for sentence in sentences:
        if not sentence.strip():
            continue
        sentence = sentence.strip() + '.'  # Aggiungi il punto alla fine della frase

        # Calcola il numero di token del segmento corrente più la nuova frase
        tokens = tokenizer(current_segment + " " + sentence, truncation=False, add_special_tokens=False)["input_ids"]

        if len(tokens) > max_length:
            # Se supera il limite, salva il segmento corrente
            if current_segment.strip():  # Aggiungi il segmento solo se non è vuoto
                segments.append(current_segment.strip())
            current_segment = sentence  # Inizia un nuovo segmento con la frase corrente
        else:
            # Altrimenti, aggiungi la frase al segmento corrente
            current_segment += " " + sentence

    # Aggiungi l'ultimo segmento
    if current_segment.strip():
        segments.append(current_segment.strip())

    return segments


# Calcola la media degli score per ciascun sentiment
def calculate_average_scores(predictions):
    sentiment_scores = {"bearish": {"total": 0.0, "count": 0},
                        "neutral": {"total": 0.0, "count": 0},
                        "bullish": {"total": 0.0, "count": 0}}

    # Somma gli score per ciascun sentiment
    for prediction in predictions:
        sentiment = prediction["sentiment"]
        score = prediction["score"]
        sentiment_scores[sentiment]["total"] += score
        sentiment_scores[sentiment]["count"] += 1
    
    # Calcola la media per ciascun sentiment
    average_scores = {}
    for sentiment in sentiment_scores:
        count = sentiment_scores[sentiment]["count"]
        if count > 0:
            average_scores[sentiment] = sentiment_scores[sentiment]["total"] / count
        else:
            average_scores[sentiment] = 0.0  # Se non ci sono frasi per quel sentiment, impostiamo la media a 0

    return average_scores

# Funzione per contare la frequenza di ciascun sentiment
def count_label_frequencies(predictions):
    label_counts = {"bearish": 0, "neutral": 0, "bullish": 0}

    for prediction in predictions:
        sentiment = prediction["sentiment"]
        label_counts[sentiment] += 1

    return label_counts

# Leggi i post dal file di testo
def load_posts_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

# Salva i risultati in un file JSON
def save_results_to_json(predictions, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(predictions, f, ensure_ascii=False, indent=4)

# Main
if __name__ == "__main__":
    input_txt_path = "cleaned_text.txt"  # File di input
    output_json_path = "cryptobert_sentiment.json"  # File JSON di output

    # Carica i post dal file di testo
    posts = load_posts_from_txt(input_txt_path)

    # Predizioni per ogni post suddiviso in segmenti
    results = []
    sentiment_counter = 0  # Contatore di sentiment analizzati

    for post in posts:
        # Suddividi il post in segmenti basati sul limite di token
        segments = split_text_into_segments(post)

        # Predici il sentiment di ogni segmento
        segment_predictions = []
        for segment in segments:
            pred = pipe(segment)[0]
            sentiment_counter += 1  # Incrementa il contatore
            if sentiment_counter % 50 == 0:
                print(f"{sentiment_counter} sentiment analizzati finora...")  # Messaggio di progresso

            segment_predictions.append({
                "segment": segment,
                "sentiment": label_mapping[pred['label']],
                "score": pred['score']  # Arrotonda lo score per segmento a 1 decimale
            })

        # Calcola le medie degli score per il post
        average_predictions = calculate_average_scores(segment_predictions)
        
        # Conta la frequenza di ciascun sentiment
        label_counts = count_label_frequencies(segment_predictions)

        # Aggiungi i risultati per il post
        results.append({
            "post": post,
            "predictions": segment_predictions,
            "average_predictions": average_predictions,
            "label_counts": label_counts  # Frequenza dei sentimenti
        })

    # Salva i risultati in un file JSON
    save_results_to_json(results, output_json_path)
    print(f"Predizioni salvate in {output_json_path}")
