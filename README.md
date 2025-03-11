# Progetto di Tesi: I Memecoin attraverso le lenti del social meddia Reddit
Il progetto è in fase di revisione per una pubblicazione su rivista.


## Progetto
 L’obiettivo principale della tesi è quello di evidenziare l’impatto reciproco tra dinamiche sociali ed economiche, 
 tramite l’analisi di eventi virali e delle fluttuazioni di mercato dei token memecoin. In particolare, la tesi si 
 concentra sull’analisi dei contenuti del social network Reddit, piattaforma chiave per la diffusione e l’evoluzione 
 dei memecoin, confrontando le tendenze emergenti nelle discussioni online con lo storico dei prezzi e le transazioni 
 di alcune di queste criptovalute. Abbiamo utilizzato sei memecoin per le nostre analisi.

## Suddivisione del lavoro
### Data Collection
Per i dati Reddit abbiamo utilizzato il tool Artic Shift: https://arctic-shift.photon-reddit.com/download-tool

Per le transazioni abbiamo utilizzato Moralis: https://developers.moralis.com/
	- Dopo essermi registrato ho inserito l'API Key in un file .key 
	- La chiave mi ha permesso di estrarre le transazioni (limite di 800 chiamate al giorno)

Per lo storico dei prezzi abbiamo utilizzato CoinMarketCap: https://coinmarketcap.com/it/
	- Ho cercato il token di mio interesse e dallo storico dei prezzi ho effettuato il download del CSV

### Data Cleaning
Durante questa fase abbiamo ripulito i dati eliminando informazioni superflue allo scopo della ricerca, 
tenendo intatti i dati dello storico dei prezzi (convertendo il CSV in Json) con relativo timestamp. In particolare, abbiamo filtrato i
post estratti, eliminando informazioni automaticamente generate o non direttamente legate al contenuto 
pubblicato dall’utente.

### Data Analysis
Questa fase è iniziata con un’analisi preliminare in cui abbiamo calcolato, per ciascuna memecoin e subreddit, il numero di transazioni, wallet, post e commenti.
Quindi, abbiamo deciso di effettuare una prima analisi di classificazione del sentiment dei post di Reddit. Abbiamo utilizzato il modello di classificazione CryptoBERT, 
preaddestrato e scaricato da Hugging Face. Nel codice, iteriamo su ogni post nella lista di post, avendo impostato in precedenza la lunghezza massima dei token 
da considerare per ogni post a 512. Chiamiamo la pipeline di transformers che esegue il modello di analisi del sentiment. Passando un post alla pipeline, il modello 
classifica il sentiment del testo, restituendo una lista di dizionari, in cui ogni dizionario contienen la label (etichetta) e uno score, un punteggio di confidenza 
compreso tra 0 e 1 che indica quanto il modello è sicuro della sua predizione. Indichiamo nel label_mapping come mappare le etichette assegnate dal modello: 
con "Bearish" il modello assegna al post sentiment negativo, con "Neutral" sentiment neutrale e con "Bullish" sentiment positivo. Infine, abbiamo recuperato il campo
timestamp dall’oggetto JSON originale, per ottenere la data del post.  Per la successiva analisi, ovvero il test di causalità di Granger, abbiamo raccolto per
ogni memecoin i dati relativi al prezzo, ai post, alle transazioni, associate alla data corrispondente in un file CSV. A questo punto con Pandas abbiamo caricato i dati e
utilizzato la funzione "grangercausalitytests" di statsmodels, che serve a verificare se una serie temporale (indipendente) contiene informazioni utili per prevedere 
un’altra serie temporale (dipendente). Seleziono le variabili interessate, ed eseguo il test per ogni combinazione di variabili, escluse le autocombinazioni,
su un lag (ritardo temporale) di 7 giorni precedenti e salvo in una matrice i risultati, in cui ogni cella contiene i p-value del test di Granger.

### Data Visualization
Infine, nella fase di Data Visualization, abbiamo rappresentato graficamente i nostri dati e i relativi risultati delle analisi svolte, al fine di evidenziare ciò che
abbiamo dedotto dal nostro studio, mostrando se esista o meno una relazione tra le transazioni, il valore del token e il parere degli utenti esposto su Reddit.
Abbiamo utilizzato Pandas e Matplotlib per ottenere i grafici.


## Output
- Grafici con andamento settimanale di post, transazioni, e prezzo
- Sentiment dei post di Reddit
- Grafici con andamento settimanale di post, transazioni, prezzo e sentiment
- Matrice di Causalità di Granger
