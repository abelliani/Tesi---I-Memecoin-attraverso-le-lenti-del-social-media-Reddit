import json

# Array contenente i nomi dei file JSONL di commenti da cui filtrare i post
file_commenti = ["r_dogecoin_comments.jsonl"]  # Aggiungi altri nomi di file se necessario

# Carica i post filtrati (reddit_posts_filtrati_unico.json)
with open('reddit_posts_filtrati_1.json', 'r', encoding="UTF-8") as f:
    try:
        # Carica l'intero array di post
        post_filtrati = json.load(f)
        print("Post caricati con successo.")
    except json.JSONDecodeError as e:
        print(f"Errore nel caricamento del JSON: {e}")
        exit(1)  # Esci se il caricamento fallisce

# Crea un set di id_post dai post filtrati per confronto rapido (incluso 't3_' nel 'name')
id_post_filtrati = {post['name'] for post in post_filtrati}

# Definisci il nome del file di output
output_file_name = 'reddit_comments_filtrati_1.json'

# Apri il file di output una sola volta per scrivere tutti i risultati
with open(output_file_name, 'w', encoding="UTF-8") as f_out:
    # Scrivi l'apertura del JSON array
    f_out.write("[\n")

    # Itera attraverso i file dei commenti
    first = True  # Per gestire la virgola tra gli elementi nel file JSON
    for file_name in file_commenti:
        # Carica i commenti (file JSONL corrente)
        with open(file_name, 'r', encoding="UTF-8") as f:
            # Filtra i commenti che appartengono ai post filtrati (confronto tramite parent_id)
            commenti_filtrati = []
            for line in f:
                commento = json.loads(line)  # Carica ogni riga come un oggetto JSON
                # Controlla se il commento ha un parent_id che corrisponde a un post filtrato
                if 'parent_id' in commento and commento['parent_id'] in id_post_filtrati:
                    commenti_filtrati.append(commento)

        # Scrivi i commenti filtrati direttamente nel file di output
        for commento in commenti_filtrati:
            if not first:
                f_out.write(",\n")  # Aggiungi la virgola solo dopo il primo oggetto
            json.dump(commento, f_out, indent=4)
            first = False

        # Stampa il numero di commenti filtrati per ogni file
        print(f"Numero di commenti filtrati da {file_name}: {len(commenti_filtrati)}")

        # Liberiamo la memoria utilizzata
        del commenti_filtrati

    # Scrivi la chiusura del JSON array
    f_out.write("\n]")

# Stampa il messaggio finale
print("Scrittura completata nel file di output.")
