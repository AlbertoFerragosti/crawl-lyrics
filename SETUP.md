# Discography Crawler - Guida all'Installazione e Utilizzo

## 🚀 Quick Start

### 1. Installazione

```bash
# Clona o scarica il progetto
cd crawl-lyrics

# Crea ambiente virtuale
python -m venv .venv

# Attiva ambiente (Windows)
.venv\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt
```

### 2. Utilizzo Base

```bash
# Cerca un artista
python main.py --search "Radiohead"

# Crawling discografia
python main.py "Radiohead"

# Con output personalizzato
python main.py "Pink Floyd" --output pink_floyd.json --pretty
```

## 📋 Comandi Disponibili

### Ricerca Artisti
```bash
python main.py --search "Nome Artista" --limit 5
```

### Crawling Discografia
```bash
# Base
python main.py "Nome Artista"

# Con API Last.fm (raccomandato)
python main.py "Nome Artista" --lastfm-key YOUR_API_KEY

# Output personalizzato
python main.py "Nome Artista" --output discografia.json --pretty

# Modalità silenziosa
python main.py "Nome Artista" --quiet

# Modalità verbose
python main.py "Nome Artista" --verbose
```

## 🔧 Configurazione Avanzata

### 1. API Key Last.fm (Opzionale ma Raccomandato)

1. Registrati su https://www.last.fm/api
2. Crea un'applicazione e ottieni la API key
3. Copia `.env.example` in `.env`
4. Inserisci la tua API key nel file `.env`

### 2. Variabili di Ambiente

Crea un file `.env` con:
```bash
LASTFM_API_KEY=your_api_key_here
RATE_LIMIT_REQUESTS=5
RATE_LIMIT_WINDOW=60
MAX_RETRIES=3
LOG_LEVEL=INFO
```

## 📊 Struttura Output JSON

```json
{
  "artist": {
    "name": "Nome Artista",
    "country": "IT",
    "musicbrainz_id": "uuid",
    "begin_date": "1990-01-01"
  },
  "albums": [
    {
      "title": "Nome Album",
      "release_year": 1995,
      "album_type": "album",
      "genre": ["Rock", "Alternative"],
      "tracks": [
        {
          "title": "Nome Canzone",
          "track_number": 1,
          "duration_ms": 240000
        }
      ]
    }
  ],
  "sources": ["MusicBrainz", "Last.fm"]
}
```

## 🧪 Test ed Esempi

```bash
# Esegui test
python -m pytest tests/ -v

# Demo con dati di esempio
python examples/demo.py

# Esempio base
python examples/basic_usage.py
```

## 📄 API Utilizzate

### MusicBrainz (Principale)
- Database musicale open source
- Metadati affidabili
- Nessuna registrazione richiesta
- Rate limit: 1 richiesta/secondo

### Last.fm (Opzionale)
- Informazioni aggiuntive su generi
- Statistiche di popolarità
- Richiede API key gratuita
- Arricchisce i dati MusicBrainz

## ⚖️ Note Legali

### ✅ Cosa FA il sistema:
- Recupera metadati pubblici
- Titoli di canzoni e album
- Date di rilascio
- Informazioni sull'artista
- Durata delle tracce

### ❌ Cosa NON FA il sistema:
- NON estrae testi completi delle canzoni
- NON viola copyright
- NON scarica musica
- NON fornisce contenuti protetti

### Uso Responsabile:
- Solo per scopi educativi/ricerca
- Rispetta i termini delle API
- Rate limiting automatico
- Conformità copyright

## 🛠️ Troubleshooting

### Problemi Comuni

1. **Nessun album trovato**
   - Prova varianti del nome artista
   - Usa la ricerca: `--search "Nome"`
   - Alcuni artisti hanno pochi dati su MusicBrainz

2. **Rate limit errors**
   - Il sistema gestisce automaticamente
   - Riduci `RATE_LIMIT_REQUESTS` se necessario

3. **Import errors**
   - Verifica ambiente virtuale attivato
   - Reinstalla: `pip install -r requirements.txt`

4. **API Last.fm non funziona**
   - Verifica API key nel file `.env`
   - Il sistema funziona anche senza Last.fm

### Log e Debug

```bash
# Modalità debug
python main.py "Artista" --verbose

# Controlla log file
cat crawler.log
```

## 🚀 Sviluppo

### Struttura Progetto
```
crawl-lyrics/
├── src/
│   ├── models/           # Modelli dati Pydantic
│   ├── services/         # Client API
│   ├── crawlers/         # Logica crawling
│   └── discography_crawler.py
├── tests/               # Test unitari
├── examples/            # Esempi e demo
├── main.py             # CLI interface
└── requirements.txt
```

### Estendere il Sistema

1. **Nuovi servizi**: Aggiungi client in `src/services/`
2. **Nuovi formati**: Modifica modelli in `src/models/`
3. **Nuove funzionalità**: Estendi `DiscographyCrawler`

## 💡 Suggerimenti d'Uso

### Per Sviluppatori
```python
from src.discography_crawler import crawl_artist_discography

# Uso programmatico
discography = await crawl_artist_discography("Pink Floyd")
print(f"Trovati {discography.total_albums} album")
```

### Per Analisi Dati
```python
# Analizza la discografia
albums_by_year = discography.get_albums_by_year()
albums_by_type = discography.get_albums_by_type()

# Esporta per elaborazione
discography.save_to_file("data.json")
```

### Per Statistiche
- Evoluzione della produzione musicale
- Analisi dei generi nel tempo
- Statistiche sulle durate
- Comparazione tra artisti

---

## 📞 Supporto

Per problemi, suggerimenti o contributi:
1. Controlla la documentazione
2. Verifica i log di debug
3. Consulta gli esempi forniti
4. Apri una issue su GitHub
