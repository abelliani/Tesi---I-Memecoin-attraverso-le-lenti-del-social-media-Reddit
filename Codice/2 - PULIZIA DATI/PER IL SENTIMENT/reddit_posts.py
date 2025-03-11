import json
import re

# Array contenente i nomi dei file JSONL da cui filtrare i post
file_names = ["r_dogecoin_posts.jsonl"]  # Aggiungi altri nomi di file se necessario

# Definisci le parole chiave da cercare
parole_chiave = []

# Definisci le parole indesiderate da escludere dai post
parole_indesiderate = []

# Definisci il nome del file di output
output_file_name = "reddit_posts_filtrati_1.json"

# Lista per accumulare tutti i post filtrati
tutti_post_filtrati = []

# Itera attraverso i nomi dei file
for file_name in file_names:
    # Lista per accumulare i post filtrati per il file corrente
    post_filtrati = []

    # Carica il file JSONL che contiene una lista di oggetti
    with open(file_name, 'r', encoding="UTF-8") as f:
        # Filtra i post che contengono una delle parole chiave nel testo ('selftext')
        for line in f:
            post = json.loads(line)
            # Controlla se non ci sono restrizioni (parole chiave o indesiderate)
            if not parole_chiave and not parole_indesiderate:
                post_filtrati.append(post)
            else:
                # Verifica se 'selftext' è presente e applica i criteri di filtro
                if ('selftext' in post and
                    (any(re.search(r'\b' + parola + r'\b', post['selftext'].lower()) for parola in parole_chiave) or not parole_chiave) and
                    not any(parola in post['selftext'].lower() for parola in parole_indesiderate)):
                    post_filtrati.append(post)

    # Aggiungi i post filtrati alla lista totale
    tutti_post_filtrati.extend(post_filtrati)

    # Stampa il numero di post filtrati per ogni file
    print(f"Numero di post filtrati da {file_name}: {len(post_filtrati)}")

    # Liberiamo la memoria utilizzata
    del post_filtrati

# Scrivi i post filtrati nel file di output come un'unica lista
with open(output_file_name, 'w') as f_out:
    json.dump(tutti_post_filtrati, f_out, indent=4)

# Stampa il numero totale di post filtrati
print(f"Scrittura completata nel file di output con {len(tutti_post_filtrati)} post filtrati.")
