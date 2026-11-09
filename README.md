# Sito Faccin Auto

Sito statico (HTML, nessun server) pensato per GitHub Pages con dominio `www.faccinauto.it`.

## 1. Dominio su Aruba
1. Acquista **solo il dominio** `faccinauto.it`: non serve un piano di hosting Aruba.
2. Intestalo alla ditta (Faccin Auto di Massimo Faccin, con P.IVA), così il dominio è dell’attività.
3. Nel pannello Aruba apri **Gestione DNS** del dominio e imposta:

| Tipo | Nome | Valore |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | pierlucafaccin.github.io |

Elimina eventuali record A o CNAME già presenti per `@` e `www` (pagina di parcheggio Aruba).

## 2. GitHub Pages
1. Carica il contenuto di questa cartella nel repository (il file `CNAME` contiene già `www.faccinauto.it`).
2. Settings → Pages → Custom domain: `www.faccinauto.it` → attendi la verifica DNS → spunta **Enforce HTTPS**.
3. `faccinauto.it` senza www viene reindirizzato automaticamente.

## 3. Google
- **Search Console**: aggiungi la proprietà `faccinauto.it` (verifica con record TXT su Aruba) e invia `https://www.faccinauto.it/sitemap.xml`.
- **Profilo dell’attività Google**: imposta il sito web su `https://www.faccinauto.it`. È la cosa che conta di più per la ricerca locale.
- **Link recensione**: Profilo → Chiedi recensioni → copia il link e incollalo in `index.html` nella riga `const GOOGLE_REVIEW_URL = ...`.

## 4. Usato in salone
1. Carica le foto in `img/usato/` (formato orizzontale 4:3, idealmente larghe 1200 px; vanno bene anche JPG).
2. Modifica `usato.json` (su GitHub: apri il file → matita → Commit). Ogni auto:

```json
{
  "id": "panda-2018-bianca",
  "marca": "Fiat",
  "modello": "Panda",
  "versione": "1.2 Easy",
  "anno": 2018,
  "km": 62000,
  "alimentazione": "Benzina",
  "cambio": "Manuale",
  "potenza": "69 CV",
  "colore": "Bianco",
  "porte": 5,
  "descrizione": "Unico proprietario, tagliandi regolari.",
  "foto": ["img/usato/panda-2018-1.jpg", "img/usato/panda-2018-2.jpg"],
  "stato": "disponibile"
}
```

- `stato`: `disponibile`, `riservata` (mostra il bollino) o `venduta` (l’auto sparisce dal sito).
- Le auto sono separate da una virgola. **Cancella i 3 esempi** (`"esempio": true`) prima di andare online.
- Il sito si aggiorna da solo dopo circa un minuto dal commit.

## 5. Recensioni automatiche (facoltativo)
Una GitHub Action (`.github/workflows/recensioni.yml`) aggiorna ogni giorno `reviews.json` con valutazione media, numero di recensioni e le recensioni che Google rende disponibili.
1. Google Cloud Console → nuovo progetto → abilita **Places API (New)** → crea una chiave API e limitala a quella sola API.
2. GitHub → Settings → Secrets and variables → Actions → nuovo secret `GOOGLE_PLACES_API_KEY`.
3. Actions → “Aggiorna recensioni Google” → Run workflow. Il log stampa il Place ID: salvalo nel secret `GOOGLE_PLACE_ID`.

Limiti: Google restituisce al massimo 5 recensioni, scelte da lui; le altre restano quelle scritte a mano in `index.html` (`RECENSIONI`). Le nuove compaiono in testa al carosello.

## 6. Privacy
`privacy.html` è una base da far controllare. Completa **REA** e **PEC** (sono nella visura camerale) togliendo il commento nel file.
