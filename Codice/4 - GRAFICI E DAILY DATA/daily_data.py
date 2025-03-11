import pandas as pd
import matplotlib.pyplot as plt
import glob
import json
from matplotlib.lines import Line2D
from collections import defaultdict

# Nome della moneta
nome_moneta = 'MAGA'

# Funzione per caricare e combinare più file JSON
def carica_e_combina_file(percorso_pattern, tipo="transazioni"):
    file_list = glob.glob(percorso_pattern)  # Trova tutti i file che corrispondono al pattern
    data_list = []
    
    for file in file_list:
        with open(file, 'r') as f:
            data = json.load(f)  # Carica il JSON
            if tipo == "post":
                data_list.extend(data["posts_per_day"])  # Estrai i post per giorno
            elif tipo == "transazioni":
                data_list.extend(data["transactions_per_day"])  # Estrai le transazioni per giorno
    
    return pd.DataFrame(data_list)

# Funzione per caricare i dati del sentiment giornaliero
def process_sentiment_data(sentiment_file):
    with open(sentiment_file, 'r') as f:
        sentiment_data = json.load(f)
    
    daily_sentiment = defaultdict(lambda: {'total_posts': 0, 'weighted_sentiment': 0})
    
    for entry in sentiment_data:
        date = pd.to_datetime(entry['created_date']).date()
        label_counts = entry['label_counts']
        total_posts = sum(label_counts.values())
        
        negative_count = label_counts.get('bearish', 0)
        neutral_count = label_counts.get('neutral', 0)
        positive_count = label_counts.get('bullish', 0)
        
        weighted_sentiment = (negative_count * 0 + neutral_count * 0.5 + positive_count * 1)
        avg_sentiment = weighted_sentiment / total_posts if total_posts > 0 else 0
        
        daily_sentiment[date]['total_posts'] += total_posts
        daily_sentiment[date]['weighted_sentiment'] += avg_sentiment * total_posts
    
    rows = []
    for day, values in daily_sentiment.items():
        total_posts = values['total_posts']
        avg_sentiment = values['weighted_sentiment'] / total_posts if total_posts > 0 else 0
        sentiment_label = 'bearish' if avg_sentiment < 0.33 else ('bullish' if avg_sentiment > 0.66 else 'neutral')
        
        rows.append({
            'day': day,
            'total_posts': total_posts,
            'avg_sentiment': avg_sentiment,
            'sentiment': sentiment_label
        })
    
    return rows

# Caricamento dei dati del sentiment giornaliero
sentiment_file = 'maga_cryptobert_sentiment.json'
sentiment_daily = process_sentiment_data(sentiment_file)
sentiment_daily = pd.DataFrame(sentiment_daily)  # Converti la lista in DataFrame
sentiment_daily['day'] = pd.to_datetime(sentiment_daily['day']) # Converte la colonna 'day' in formato datetime
# Caricamento dei file di Reddit
reddit_posts = carica_e_combina_file('post_results.json', tipo="post")

# Aggiungi la colonna 'day' per i post di Reddit
reddit_posts['timestamp'] = pd.to_datetime(reddit_posts['date'])
reddit_posts['day'] = reddit_posts['timestamp']

# Unisci i dati di Reddit in base al giorno
reddit_daily = reddit_posts.groupby('day').agg(
    total_posts=('total_posts_per_day', 'sum')
).reset_index()

# Caricamento delle transazioni
transazioni = carica_e_combina_file('transaction_analysis_results.json', tipo="transazioni")
transazioni['day'] = pd.to_datetime(transazioni['block_timestamp'], errors='coerce')

# Raggruppamento giornaliero per transazioni
transazioni_daily = transazioni.groupby('day').agg(
    total_transactions=('daily_transaction_count', 'sum')
).reset_index()

# Caricamento e preparazione dei prezzi
with open('maga_price.json', 'r') as f:
    prezzi_data = json.load(f)

# Prepara il DataFrame dei prezzi con i dati corretti
prezzi_daily = pd.DataFrame(prezzi_data)

# Conversione della colonna 'snapped_at' in formato datetime
prezzi_daily['day'] = pd.to_datetime(prezzi_daily['snapped_at'])  # snapped_at / timestamp

# La colonna 'price' è già il dato che ci interessa, quindi lo rinominiamo
prezzi_daily['close'] = pd.to_numeric(prezzi_daily['price'], errors='coerce')  # close / price

# Ora unisci i dati di Reddit, transazioni e sentiment separatamente
daily_data = pd.merge(transazioni_daily, reddit_daily, on='day', how='left')
# Aggiungi i dati del sentiment senza fare un merge che sovrascrive
daily_data = pd.merge(daily_data, sentiment_daily[['day', 'sentiment', 'avg_sentiment']], on='day', how='left')

daily_data = pd.merge(daily_data, prezzi_daily[['day', 'close']], on='day', how='left')

# Riempie eventuali valori NaN con 0 o 'neutral'
daily_data['total_posts'] = daily_data['total_posts'].fillna(0)  # Se non ci sono post, impostiamo 0
daily_data['total_transactions'] = daily_data['total_transactions'].fillna(0)  # Se non ci sono transazioni, impostiamo 0
daily_data['sentiment'] = daily_data['sentiment'].fillna('neutral')  # Se non ci sono sentiment, impostiamo 'neutral'
daily_data['avg_sentiment'] = daily_data['avg_sentiment'].fillna(0)  # Se non c'è sentiment, impostiamo 0
daily_data['close'] = daily_data['close'].fillna(method='ffill')  # Riempie il prezzo mancante con l'ultimo valore disponibile

# Salva il DataFrame daily_data in un unico file CSV
daily_data.to_csv(f'daily_data_cryptobert_{nome_moneta}.csv', index=False, encoding='utf-8')

# Stampa il salvataggio
print(f"Dati giornalieri uniti e salvati correttamente in daily_data_cryptobert_{nome_moneta}.csv")
