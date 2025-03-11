import requests
import json
import time

# File di configurazione
file_transactions = "output_swaps_1.json"
file_cursor = "data/swaps_cursor_bnana.txt"

# Chiave API
with open("key/moralis_7.key", "r") as fileApi:
    api_key = fileApi.read().strip()

# Parametri iniziali 
base_url = "https://solana-gateway.moralis.io/token/mainnet/8dohvHJs5pj6dqbWj1EHeatK6yoz85SiUwEx9sKx7TKV/swaps" #"https://solana-gateway.moralis.io/token/mainnet/mpoxP5wyoR3eRW8L9bZjGPFtCsmX8WcqU5BHxFW1xkn/swaps" #"https://solana-gateway.moralis.io/token/mainnet/FUAfBo2jgks6gB4Z4LfZkqSZgzNucisEHqnNebaRxM1P/swaps"
headers = {
    "Accept": "application/json",
    "X-API-Key": api_key
}
params = {
    "order": "DESC",
    "toDate": "2025-02-27T17:00:00.000Z", #"2025-02-19T09:27:57.000Z",
    "fromDate": "2024-04-01T00:00:00.000Z", #"2025-01-19T00:00:57.000Z",
    "cursor": None
}

# Carica il cursore se disponibile
try:
    with open(file_cursor, "r") as f:
        cursor_content = f.read().strip()
        if cursor_content:  # Se il cursore non è vuoto, usalo
            params["cursor"] = cursor_content
            print(f"Cursore caricato: {params['cursor']}")
        else:
            print("Il file del cursore era vuoto, avvio dalla prima pagina.")
except FileNotFoundError:
    print("Nessun cursore trovato, avvio dalla prima pagina.")


swaps = []  # Lista per salvare tutte le transazioni
n = 0  # Contatore di chiamate API
save_interval = 100  # Intervallo per salvataggi intermedi

while True:
    try:
        response = requests.get(base_url, headers=headers, params=params)
        data = response.json()
        
        swaps += data.get("result", [])  # Aggiungi le nuove transazioni
        params["cursor"] = data.get("cursor")  # Aggiorna il cursore

        # Se non ci sono più dati, interrompi il ciclo
        if params["cursor"] is None:
            print("Tutte le transazioni recuperate.")
            break

        # Salvataggio intermedio
        if n % save_interval == 0 and n > 0:
            with open(file_cursor, "w") as f:
                f.write(params["cursor"])
            with open(file_transactions, "w") as f:
                json.dump(swaps, f, indent=4)
            print(f"Salvataggio intermedio dopo {n} chiamate.")

        time.sleep(0.5)  # Rispetta i limiti API
        n += 1

    except Exception as e:
        # Salva i dati e il cursore in caso di errore
        with open(file_cursor, "w") as f:
            f.write(params["cursor"] or "")
        with open(file_transactions, "w") as f:
            json.dump(swaps, f, indent=4)
        print(f"Errore: {e}")
        
        # Gestione degli errori API
        if isinstance(e, requests.exceptions.RequestException):
            print("Errore di rete. Attesa di 60 secondi...")
            time.sleep(60)
        else:
            break

# Salvataggio finale
with open(file_transactions, "w") as f:
    json.dump(swaps, f, indent=4)
print(f"Salvataggio finale completato dopo {n} chiamate.")
