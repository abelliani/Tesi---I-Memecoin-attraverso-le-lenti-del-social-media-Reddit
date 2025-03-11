import json
import pandas as pd

# 5. Caricamento e preparazione del sentiment
def process_sentiment_data(sentiment_file, output_file):
    # Caricamento dei dati dal file JSON
    with open(sentiment_file, 'r') as f:
        sentiment_data = json.load(f)

    # Elaborazione dei dati del sentiment
    rows = []
    for entry in sentiment_data:
        date = pd.to_datetime(entry['created_date'])  # Usa `created_date` come data
        label_counts = entry['label_counts']  # Conta delle etichette: bearish, neutral, bullish
        total_posts = sum(label_counts.values())  # Conta totale dei post del giorno

        # Estrazione dei conteggi per ciascuna etichetta
        bearish_count = label_counts.get('bearish', 0)
        neutral_count = label_counts.get('neutral', 0)
        bullish_count = label_counts.get('bullish', 0)

        # Calcolo del sentiment ponderato
        weighted_sentiment = (
            bearish_count * 0 +  # Bearish: peso 0
            neutral_count * 0.5 +  # Neutral: peso 0.5
            bullish_count * 1  # Bullish: peso 1
        )

        # Calcolo del sentiment medio
        if total_posts > 0:
            avg_sentiment = weighted_sentiment / total_posts
        else:
            avg_sentiment = 0  # Nel caso in cui non ci siano post

        # Determinazione del sentiment basato sulla media ponderata
        if avg_sentiment < 0.4:
            sentiment_class = 'bearish'
        elif avg_sentiment <= 0.6:
            sentiment_class = 'neutral'
        else:
            sentiment_class = 'bullish'

        # Aggiungi i dati della riga (data, sentiment e conteggio totale)
        rows.append({
            'day': date.strftime('%Y-%m-%d'),  # Formato data come stringa 'YYYY-MM-DD'
            'total_posts': total_posts,
            'bearish_count': bearish_count,
            'neutral_count': neutral_count,
            'bullish_count': bullish_count,
            'avg_sentiment': avg_sentiment,
            'sentiment': sentiment_class
        })

    # Salvataggio del risultato in un file JSON
    with open(output_file, 'w') as out_f:
        json.dump(rows, out_f, indent=4)

# Esempio di utilizzo
sentiment_file = 'squid_cryptobert_sentiment.json'
output_file = 'squid_cryptobert_sentiment_output.json'
process_sentiment_data(sentiment_file, output_file)

print(f"Dati sentiment salvati in {output_file}")
