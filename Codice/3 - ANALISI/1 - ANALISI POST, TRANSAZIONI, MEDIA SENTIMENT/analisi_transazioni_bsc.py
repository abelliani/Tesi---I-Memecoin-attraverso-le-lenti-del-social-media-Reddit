import pandas as pd
import glob
import json

def analyze_transactions(input_files):
    # Variabili per accumulare risultati globali
    total_transactions = 0
    total_value = 0.0
    transaction_count_per_day = []
    transaction_count_per_week = []
    transaction_count_per_month = []
    from_address_counts = pd.Series(dtype=int)
    to_address_counts = pd.Series(dtype=int)
    value_per_from_address = pd.Series(dtype=float)
    value_per_to_address = pd.Series(dtype=float)
    token_values = pd.Series(dtype=float)

    for file in input_files:
        try:
            with open(file, 'r') as f:
                transactions = json.load(f)
            print(f"Caricato {len(transactions)} transazioni da '{file}'.")
        except json.JSONDecodeError as e:
            print(f"Errore nel file {file}: {e}")
            continue

        # Creazione del DataFrame per il file corrente
        transactions_df = pd.DataFrame(transactions)
        transactions_df['block_timestamp'] = pd.to_datetime(transactions_df['block_timestamp'])
        transactions_df['value_decimal'] = transactions_df['value_decimal'].astype(float)

        # Rimuovi i duplicati in base a tutte le colonne (puoi specificare colonne se necessario)
        initial_count = len(transactions_df)
        transactions_df = transactions_df.drop_duplicates()
        removed_duplicates = initial_count - len(transactions_df)
        print(f"Rimossi {removed_duplicates} duplicati da '{file}'.")

        # Aggiorna i conteggi globali
        total_transactions += len(transactions_df)
        total_value += transactions_df['value_decimal'].sum()

        # Analisi temporale per il file corrente
        daily_data = transactions_df.resample('D', on='block_timestamp').agg(
            daily_transaction_count=('value_decimal', 'size'),
            daily_transaction_value=('value_decimal', 'sum')
        ).reset_index()
        
        # Raggruppamento settimanale per transazioni, includendo l'anno
        weekly_data = transactions_df.resample('W-Mon', on='block_timestamp').agg(
            weekly_transaction_count=('value_decimal', 'size'),
            weekly_transaction_value=('value_decimal', 'sum')
        ).reset_index()
        
        # Aggiungi una colonna per l'anno e la settimana
        weekly_data['week'] = weekly_data['block_timestamp'].dt.strftime('%Y-%U')

        # Raggruppamento mensile per transazioni
        monthly_data = transactions_df.resample('ME', on='block_timestamp').agg(
            monthly_transaction_count=('value_decimal', 'size'),
            monthly_transaction_value=('value_decimal', 'sum')
        ).reset_index()

        transaction_count_per_day.append(daily_data)
        transaction_count_per_week.append(weekly_data)
        transaction_count_per_month.append(monthly_data)

        # Analisi per indirizzi e token
        from_address_counts = from_address_counts.add(transactions_df['from_address'].value_counts(), fill_value=0)
        to_address_counts = to_address_counts.add(transactions_df['to_address'].value_counts(), fill_value=0)
        value_per_from_address = value_per_from_address.add(transactions_df.groupby('from_address')['value_decimal'].sum(), fill_value=0)
        value_per_to_address = value_per_to_address.add(transactions_df.groupby('to_address')['value_decimal'].sum(), fill_value=0)
        token_values = token_values.add(transactions_df.groupby('token_name')['value_decimal'].sum(), fill_value=0)

        # Libera memoria dei dati parziali
        del transactions_df

    # Concatena i dati temporali da ogni file
    transactions_per_day = pd.concat(transaction_count_per_day).groupby('block_timestamp').sum().reset_index()
    transactions_per_week = pd.concat(transaction_count_per_week).groupby('block_timestamp').sum().reset_index()
    transactions_per_month = pd.concat(transaction_count_per_month).groupby('block_timestamp').sum().reset_index()

    # Unisci risultati conteggio e valore per gli indirizzi
    from_addresses_summary = pd.DataFrame({
        "address": from_address_counts.index,
        "transaction_count": from_address_counts.values,
        "total_value": value_per_from_address.reindex(from_address_counts.index, fill_value=0).values
    }).to_dict(orient='records')

    to_addresses_summary = pd.DataFrame({
        "address": to_address_counts.index,
        "transaction_count": to_address_counts.values,
        "total_value": value_per_to_address.reindex(to_address_counts.index, fill_value=0).values
    }).to_dict(orient='records')

    # Preparazione dei risultati finali
    results = {
        "total_transactions": total_transactions,
        "total_value": total_value,
        "average_value": total_value / total_transactions if total_transactions > 0 else 0,
        "transactions_per_day": transactions_per_day.assign(block_timestamp=transactions_per_day['block_timestamp'].dt.strftime('%Y-%m-%d')).to_dict(orient='records'),
        "transactions_per_week": transactions_per_week.assign(block_timestamp=transactions_per_week['block_timestamp'].dt.strftime('%Y-%m-%d')).to_dict(orient='records'),
        "transactions_per_month": transactions_per_month.assign(block_timestamp=transactions_per_month['block_timestamp'].dt.strftime('%Y-%m')).to_dict(orient='records'),
        "active_from_addresses": from_addresses_summary,
        "active_to_addresses": to_addresses_summary,
        "value_per_token": token_values.reset_index().rename(columns={'index': 'token_name', 0: 'total_value_per_token'}).to_dict(orient='records')
    }

    # Salvataggio in file JSON
    with open("transaction_analysis_results.json", "w") as output_file:
        json.dump(results, output_file, indent=4)
        print("Analisi delle transazioni completata e risultati salvati in 'transaction_analysis_results.json'.")

# Esegui l'analisi con i file di input
input_files = glob.glob("*.json")
analyze_transactions(input_files)
