import pandas as pd
import matplotlib.pyplot as plt
import glob
import json
from matplotlib.lines import Line2D

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

# Funzione per caricare i dati del sentiment settimanale
def process_sentiment_data(sentiment_file):
    with open(sentiment_file, 'r') as f:
        sentiment_data = json.load(f)

    rows = []
    for entry in sentiment_data:
        date = pd.to_datetime(entry['created_date'])
        label_counts = entry['label_counts']
        total_posts = sum(label_counts.values())

        negative_count = label_counts.get('bearish', 0)
        neutral_count = label_counts.get('neutral', 0)
        positive_count = label_counts.get('bullish', 0)

        # Calcolo del sentiment pesato per il giorno
        weighted_sentiment = (negative_count * 0 + neutral_count * 0.5 + positive_count * 1)
        avg_sentiment = weighted_sentiment / total_posts if total_posts > 0 else 0

        rows.append({
            'day': date,
            'total_posts': total_posts,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'positive_count': positive_count,
            'avg_sentiment': avg_sentiment,
            'sentiment': 'bearish' if avg_sentiment < 0.33 else ('bullish' if avg_sentiment > 0.66 else 'neutral')
        })

    sentiment_df = pd.DataFrame(rows)

    # Raggruppamento settimanale per calcolare il sentiment aggregato
    sentiment_df.set_index('day', inplace=True)

    # Aggregazione settimanale (somma dei post per settimana)
    weekly_sentiment = sentiment_df.resample('W').agg(
        total_posts=('total_posts', 'sum'),
        negative_count=('negative_count', 'sum'),
        neutral_count=('neutral_count', 'sum'),
        positive_count=('positive_count', 'sum'),
        avg_sentiment=('avg_sentiment', 'mean')  # Media del sentiment settimanale
    ).reset_index()

    # Calcolo del sentiment settimanale basato sulla somma pesata dei post positivi, neutri e negativi
    weekly_sentiment['weighted_sentiment'] = (
        weekly_sentiment['negative_count'] * 0 +
        weekly_sentiment['neutral_count'] * 0.5 +
        weekly_sentiment['positive_count'] * 1
    )

    # Calcolo del sentiment settimanale medio
    weekly_sentiment['avg_sentiment'] = weekly_sentiment['weighted_sentiment'] / weekly_sentiment['total_posts']
    
    # Determina il sentiment settimanale
    weekly_sentiment['sentiment'] = weekly_sentiment['avg_sentiment'].apply(
        lambda x: 'bearish' if x < 0.33 else ('bullish' if x > 0.66 else 'neutral')
    )

    # Aggiungi la colonna 'week' basata sulla colonna 'day'
    weekly_sentiment['week'] = weekly_sentiment['day'].dt.to_period('W').apply(lambda r: r.start_time)
    
    return weekly_sentiment

# Caricamento dei file di transazioni e post
transazioni = carica_e_combina_file('transaction_analysis_results.json', tipo="transazioni")
reddit_posts = carica_e_combina_file('post_results.json', tipo="post")

# Caricamento e preparazione dei prezzi
with open('maga_price.json', 'r') as f:
    prezzi_data = json.load(f)

# Prepara il DataFrame dei prezzi con i dati corretti
prezzi_daily = pd.DataFrame(prezzi_data)

# Conversione della colonna 'snapped_at' in formato datetime
prezzi_daily['day'] = pd.to_datetime(prezzi_daily['snapped_at']) #snapped_at / timestamp

# La colonna 'price' è già il dato che ci interessa, quindi lo rinominiamo
prezzi_daily['close'] = pd.to_numeric(prezzi_daily['price'], errors='coerce') # close / price

# Caricamento del sentiment dal file JSON
sentiment_file = 'maga_cryptobert_sentiment.json'
weekly_sentiment = process_sentiment_data(sentiment_file)

# Aggiungi la colonna 'week' per i post di Reddit
reddit_posts['timestamp'] = pd.to_datetime(reddit_posts['date'])
reddit_posts['day'] = reddit_posts['timestamp']

# Aggiungi la colonna 'week' per i post di Reddit
reddit_posts['week'] = reddit_posts['day'].dt.to_period('W').apply(lambda r: r.start_time)

# Unisci i dati di sentiment con i post
reddit_daily = reddit_posts.groupby('week').agg(
    total_posts=('total_posts_per_day', 'sum')
).reset_index()

# Ora 'reddit_daily' ha la colonna 'week' che puoi usare per fare il merge
reddit_daily = reddit_daily.merge(weekly_sentiment[['week', 'sentiment']], on='week', how='left')

# Riempie eventuali valori NaN con 'neutral'
#reddit_daily['sentiment'] = reddit_daily['sentiment'].fillna('neutral')

# Creazione della colonna 'week' per weekly_sentiment
weekly_sentiment['week'] = weekly_sentiment['day'].dt.to_period('W').apply(lambda r: r.start_time)

# Assicurati che 'block_timestamp' sia di tipo datetime
transazioni['block_timestamp'] = pd.to_datetime(transazioni['block_timestamp'], errors='coerce')

# Creazione della colonna 'week' per transazioni
transazioni['week'] = transazioni['block_timestamp'].dt.to_period('W').apply(lambda r: r.start_time)

# Raggruppamento settimanale per transazioni
transazioni_weekly = transazioni.groupby('week').agg(
    total_transactions=('daily_transaction_count', 'sum')
).reset_index()

# Raggruppamento settimanale per post di Reddit
reddit_weekly = reddit_posts.groupby('week').agg(
    total_posts=('total_posts_per_day', 'sum')
).reset_index()

# Creazione di un DataFrame settimanale per i prezzi 
prezzi_daily['week'] = prezzi_daily['day'].dt.to_period('W').apply(lambda r: r.start_time)

prezzi_daily = prezzi_daily.sort_values(by='week')
# Selezioniamo l'ultimo prezzo per ogni settimana (ultimo giorno della settimana)
prezzi_weekly = prezzi_daily.groupby('week').agg(
    last_price=('close', 'last')  # Prendi l'ultimo valore 'close' per ogni settimana
).reset_index()

# Approssima il valore di last_price a 4 decimali
prezzi_weekly['last_price'] = prezzi_weekly['last_price'].round(4)

# Ora uniamo tutte le informazioni settimanali in un unico dataframe
weekly_data = pd.merge(transazioni_weekly, reddit_weekly, on='week', how='left')
#weekly_data = pd.merge(weekly_data, prezzi_daily, on='week', how='left')

weekly_data['total_posts'] = weekly_data['total_posts'].fillna(0)  # Se non ci sono post, impostiamo 0
weekly_data['total_transactions'] = weekly_data['total_transactions'].fillna(0)  # Se non ci sono transazioni, impostiamo 0

# Unione con il sentiment settimanale
#weekly_data = pd.merge(weekly_data, weekly_sentiment[['week', 'sentiment']], on='week', how='left')
weekly_data = pd.merge(weekly_data, weekly_sentiment[['week', 'sentiment', 'avg_sentiment']], on='week', how='left')
weekly_data = pd.merge(weekly_data, prezzi_weekly, on='week', how='left')
weekly_data['last_price'] = weekly_data['last_price'].fillna(method='ffill')

# Mappa i sentiment ai colori
sentiment_color_map = {
    'bearish': 'red',
    'neutral': 'yellow',
    'bullish': 'green'
}

# Salva il DataFrame weekly_data in un file CSV
weekly_data.to_csv(f'weekly_data_cryptobert_{nome_moneta}.csv', index=False, encoding='utf-8')

# Creazione della colonna 'marker_color' basata sul sentiment
weekly_data['marker_color'] = weekly_data['sentiment'].map(sentiment_color_map)

# Assicurati che non ci siano NaN nella colonna 'marker_color'
weekly_data['marker_color'] = weekly_data['marker_color'].fillna('orange')  # Sostituisci NaN con un colore di default (ad esempio 'gray')


# Creazione del grafico con tre assi Y
fig, ax1 = plt.subplots(figsize=(12, 5))  # Ridotto in altezza

# Mostra solo alcune etichette sull'asse x (aggiustamento dell'intervallo delle etichette)
step = 4  # Mostra un'etichetta ogni 4 settimane
ax1.set_xticks(range(0, len(transazioni_weekly['week']), step))  
ax1.set_xticklabels(transazioni_weekly['week'].astype(str)[::step], rotation=60, ha='right', fontsize=12)  # Testo più grande

# Primo asse Y per le transazioni (blu)
ax1.set_xlabel('Week', fontsize=18)
ax1.set_ylabel(f'Transactions', color='blue', fontsize=18)
ax1.plot(weekly_data['week'].astype(str), weekly_data['total_transactions'], color='blue', marker='o', label='Transactions')
ax1.tick_params(axis='y', labelcolor='blue', labelsize=12)

# Secondo asse Y per i post di Reddit (arancione)
ax2 = ax1.twinx()
ax2.set_ylabel('Weekly Reddit Posts', color='orange', fontsize=18)

# Plotta la linea che collega i post di Reddit (arancione)
ax2.plot(weekly_data['week'].astype(str), weekly_data['total_posts'], color='orange', marker='x', label="Weekly Reddit Posts")

# Plotta i post di Reddit con i colori personalizzati come marker 'x'
ax2.tick_params(axis='y', labelcolor='orange', labelsize=12)

# Terzo asse Y per il prezzo (verde)
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))  
ax3.set_ylabel('Closing Price', color='green', fontsize=18)

# Tracciamo il grafico del prezzo settimanale
ax3.plot(weekly_data['week'].astype(str), weekly_data['last_price'], color='green', marker='^', markersize=3, linestyle='-', label='Closing Price')
ax3.tick_params(axis='y', labelcolor='green', labelsize=12)



fig.tight_layout()  # Per evitare sovrapposizioni
plt.grid(True)

# Salvataggio del grafico settimanale
plt.savefig(f'weekly_chart_{nome_moneta}.jpeg', format='jpeg', dpi=300)
plt.close()