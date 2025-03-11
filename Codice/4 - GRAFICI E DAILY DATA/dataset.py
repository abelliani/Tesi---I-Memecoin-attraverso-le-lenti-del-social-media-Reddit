import pandas as pd
import json

memecoin = "Bnana"
def process_csv(file_path):
    # Legge il CSV
    df = pd.read_csv(file_path)
    
    # Calcola il totale di total_transactions e total_posts
    total_transactions = df['total_transactions'].sum()
    total_posts = df['total_posts'].sum()
    
    print(f"Totale transazioni: {total_transactions}")
    print(f"Totale post: {total_posts}")
    
    return df, total_transactions, total_posts

def process_json(json_file):
    # Legge il JSON
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    comments_per_day = {entry['date']: entry['total_comments_per_day'] for entry in data['comments_per_day']}
    total_comments = sum(comments_per_day.values())
    
    print(f"Totale commenti: {total_comments}")
    
    return comments_per_day, total_comments

def process_address_json(address_json_file):
    # Carica i dati dal file JSON degli indirizzi
    with open(address_json_file, 'r') as file:
        data = json.load(file)
    
    # Estrai la lista di indirizzi
    active_from_addresses = data.get("active_from_addresses", [])
    
    # Contare il numero di indirizzi
    address_count = len(active_from_addresses)
    
    print(f"Il numero totale di address è: {address_count}")
    
    return address_count

def main(csv_file, json_file, address_json_file):
    df, total_transactions, total_posts = process_csv(csv_file)
    comments_per_day, total_comments = process_json(json_file)
    address_count = process_address_json(address_json_file)
    
    # Aggiunge il numero di commenti al DataFrame
    df['total_comments'] = df['day'].map(comments_per_day).fillna(0).astype(int)
    
    # Salva i risultati in un nuovo file
    summary_df = pd.DataFrame({'Metric': ['Total Transactions', 'Total Posts', 'Total Comments', 'Total Addresses'],
                               'Value': [total_transactions, total_posts, total_comments, address_count]})
    summary_df.to_csv(f'{memecoin}.csv', index=False)
    
    
    print("Risultati salvati in summary.csv e updated_data.csv")
    
# Esegui lo script con i file desiderati
csv_file = f'daily_data_cryptobert_{memecoin}.csv'  # Modifica con il percorso corretto
json_file = 'comment_results.json'  # Modifica con il percorso corretto
address_json_file = 'transaction_analysis_results.json'  # Modifica con il percorso corretto
main(csv_file, json_file, address_json_file)
