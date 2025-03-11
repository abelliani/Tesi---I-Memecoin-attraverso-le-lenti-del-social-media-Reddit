import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests

# Memecoin di interesse
memecoin = 'Bnana'

# Carica i dati dal file CSV
df = pd.read_csv(f'daily_data_cryptobert_{memecoin}.csv')

# Prima riempi i dati mancanti per il prezzo con il valore della riga precedente
df['close'] = df['close'].fillna(method='ffill')

# Poi riempi tutti gli altri dati mancanti con 0
df.fillna(0, inplace=True)
df = df.loc[:, ~df.columns.duplicated()]
df = df.drop_duplicates()


# Seleziona solo le colonne numeriche rilevanti
variables = ['total_transactions', 'total_posts', 'avg_sentiment', 'close']
df = df[['day'] + variables]  # Considera solo le colonne rilevanti

# Numero massimo di lag da testare
max_lag = 7

# Matrice dei risultati
result_matrix = pd.DataFrame(index=variables, columns=variables)

# Calcolo del test di Granger per ogni coppia di variabili
for dependent in variables:
    for independent in variables:
        if dependent == independent:
            # Imposta "N/A" per i casi in cui la variabile dipendente è uguale alla variabile indipendente
            result_matrix.loc[dependent, independent] = "N/A"
        else:
            try:
                # Esegue il test di Granger
                test_result = grangercausalitytests(
                    df[[dependent, independent]], max_lag, verbose=False
                )
                
                # Prendi il p-value del lag con il miglior fit
                best_p_value = min([test_result[lag][0]['ssr_ftest'][1] for lag in range(1, max_lag + 1)])
                
                # Salva il risultato nella matrice
                result_matrix.loc[dependent, independent] = best_p_value
            except Exception as e:
                print(f"Error when testing Granger causality between {dependent} and {independent}: {e}")
                result_matrix.loc[dependent, independent] = "C"  # costante

# Aggiungi una colonna "variabili" alla matrice per identificare le variabili
result_matrix.insert(0, 'variabili', result_matrix.index)

# Salva la matrice in un file CSV
output_filename = f'granger_causality_cryptobert_{memecoin}.csv'
result_matrix.to_csv(output_filename, index=False)

print(f"La matrice dei p-value è stata salvata in '{output_filename}'.")

