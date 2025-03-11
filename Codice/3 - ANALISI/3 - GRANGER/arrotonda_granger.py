import pandas as pd

nome = "Bnana"  # Sostituisci con il nome della criptovaluta di interesse
# Leggi i dati da un file CSV di input
input_file = f"granger_causality_cryptobert_{nome}.csv"  # Sostituisci con il percorso del file di input
output_file = f"output_{nome}.csv"  # Sostituisci con il percorso del file di output
data = pd.read_csv(input_file)

# Sostituisci i valori NaN con "N/A" prima di applicare la funzione
data = data.fillna("N/A")

# Funzione per approssimare i valori a 4 cifre decimali
# Mantiene "N/A" o "C" invariati
def round_to_4_decimals(value):
    if value in ["N/A", "C"]:
        return value  # Mantiene "N/A" o "C" invariati
    try:
        return round(float(value), 2)  # Approssima se è un numero
    except ValueError:
        return value  # Restituisce il valore originale se non è un numero o stringa speciale

# Applica la funzione di arrotondamento a tutti i valori (eccetto l'intestazione)
data_rounded = data.applymap(round_to_4_decimals)

# Salva la nuova tabella in un file CSV di output
data_rounded.to_csv(output_file, index=False)

print(f"Tabella arrotondata salvata in {output_file}")
