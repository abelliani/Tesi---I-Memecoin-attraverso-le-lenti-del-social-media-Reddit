from moralis import evm_api  # Importa l'oggetto evm_api dalla libreria moralis
from time import sleep  # Importa la funzione sleep dalla libreria time
import json  # Importa la libreria json

# File di configurazione
file_transactions = "output_transactions_39.json"  # File dove salvare le transazioni
file_cursor = "data/transactions_cursor.txt"  # File dove salvare il cursore

# Parametri iniziali
params = {
    "address": "0xbA2aE424d960c26247Dd6c32edC70B295c744C43",  # Indirizzo del contratto
    "chain": "bsc",  # Blockchain (Binance Smart Chain)
    "limit": 100,  # Numero massimo di transazioni per chiamata
    "cursor": None,  # Il cursore sarà caricato da file, se esiste
}

# Legge la chiave API da file
with open("key/moralis_7.key", "r") as fileApi:
    api_key = fileApi.read().strip()
# Prova a caricare il cursore da un file, se disponibile
try:
    with open(file_cursor, "r") as f:
        params["cursor"] = f.read().strip()  # Imposta il cursore dai dati salvati
        print(f"Cursore caricato: {params['cursor']}")
except FileNotFoundError:
    print("Nessun cursore trovato, avvio dalla prima pagina.")
transactions = []  # Lista per salvare tutte le transazioni
n = 0  # Contatore di chiamate API
save_interval = 100  # Intervallo per salvataggi intermedi

while True:
    try:
        # Effettua la chiamata API per ottenere le transazioni
        result = evm_api.token.get_token_transfers(api_key=api_key, params=params)
        cursor = result.get("cursor")  # Recupera il cursore per la prossima chiamata
        params["cursor"] = cursor  # Aggiorna il cursore nei parametri
        transactions += result["result"]  # Aggiungi le nuove transazioni

        # Se non ci sono più dati da elaborare, interrompi il ciclo
        if cursor is None:
            print("Tutte le transazioni recuperate.")
            break

        # Salvataggio intermedio ogni 100 iterazioni
        if n % save_interval == 0 and n > 0:
            with open(file_cursor, "w") as f:
                f.write(cursor)  # Salva il cursore corrente
            with open(file_transactions, "w") as f:
                json.dump(transactions, f, indent=4)  # Salva le transazioni
            print(f"Salvataggio intermedio dopo {n} chiamate.")

        sleep(0.5)  # Pausa tra le chiamate per rispettare i limiti API
        n += 1

    except Exception as e:
        # Salva i dati e il cursore in caso di errore
        with open(file_cursor, "w") as f:
            f.write(params["cursor"] or "")
        with open(file_transactions, "w") as f:
            json.dump(transactions, f, indent=4)
        print(f"Errore: {e}")

        # Gestione degli errori specifici dell'API
        if hasattr(e, "status"):
            if e.status == 429:  # Troppe richieste
                print("Troppe richieste. Attesa...")
                sleep(60)  # Aspetta un minuto
            elif e.status in [400, 424, 401]:  # Errori critici
                print(f"Errore irreversibile: {e.status}.")
                break
            elif e.status == 500:  # Errore interno
                sleep(60)
        else:
            break

# Salvataggio finale dei dati
with open(file_transactions, "w") as f:
    json.dump(transactions, f, indent=4)
print(f"Salvataggio finale completato dopo {n} chiamate.")
