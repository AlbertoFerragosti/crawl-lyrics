# Music Discography Crawler

Un sistema Python professionale per recuperare informazioni sulla discografia degli artisti musicali utilizzando API pubbliche e web scraping etico.

## ⚠️ Disclaimer Copyright

Questo progetto rispetta rigorosamente le leggi sul copyright:
- ✅ Recupera solo **metadati pubblici** (titoli, anni, nomi album)  
- ❌ **NON estrae testi completi** delle canzoni
- ✅ Utilizza **API pubbliche legittime** (MusicBrainz, Last.fm)
- ✅ Implementa **rate limiting** per rispettare i servizi
- ✅ **Solo per scopi educativi/ricerca**

## 🚀 Quick Start

```bash
# Installazione
pip install -r requirements.txt

# Cerca un artista
python main.py --search "Radiohead"

# Crawling discografia completa
python main.py "Radiohead" --output radiohead.json --pretty

# Con API Last.fm per dati arricchiti (raccomandato)
python main.py "Pink Floyd" --lastfm-key YOUR_API_KEY
```

## ✨ Caratteristiche

- 🎵 **Discografia completa** per qualsiasi artista
- 📀 **Metadati dettagliati** su album e tracce
- 📅 **Date di pubblicazione** e informazioni cronologiche
- 🚀 **Architettura asincrona** e scalabile
- 🛡️ **Rate limiting** e gestione errori robusta
- 📊 **Output JSON strutturato** per analisi
- 🔍 **Ricerca intelligente** artisti
- 📈 **Statistiche automatiche** della discografia

## 📊 Esempio Output

```json
{
  "artist": {
    "name": "Radiohead",
    "country": "GB",
    "begin_date": "1985-01-01",
    "musicbrainz_id": "a74b1b7f-71a5-4011-9441-d0b5e4122711"
  },
  "albums": [
    {
      "title": "OK Computer",
      "release_year": 1997,
      "album_type": "album",
      "genre": ["Alternative Rock", "Art Rock"],
      "tracks": [
        {
          "title": "Airbag",
          "track_number": 1,
          "duration_ms": 284000
        }
      ]
    }
  ],
  "total_albums": 15,
  "total_tracks": 157,
  "sources": ["MusicBrainz", "Last.fm"]
}
```

## 🛠️ Installazione

```bash
# Clona il progetto
git clone [repository-url]
cd crawl-lyrics

# Crea ambiente virtuale
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Installa dipendenze
pip install -r requirements.txt
```

## 💻 Utilizzo

### CLI Interface

```bash
# Ricerca artisti
python main.py --search "Led Zeppelin" --limit 5

# Crawling base
python main.py "The Beatles"

# Con output personalizzato
python main.py "Pink Floyd" --output floyd.json --pretty

# Con API Last.fm (raccomandato)
python main.py "Nirvana" --lastfm-key YOUR_API_KEY --verbose

# Modalità silenziosa
python main.py "Queen" --quiet
```

### Uso Programmatico

```python
import asyncio
from src.discography_crawler import crawl_artist_discography

async def main():
    # Crawling semplice
    discography = await crawl_artist_discography("Radiohead")
    
    print(f"Artista: {discography.artist.name}")
    print(f"Album: {discography.total_albums}")
    print(f"Tracce: {discography.total_tracks}")
    
    # Analisi per anno
    by_year = discography.get_albums_by_year()
    for year, albums in by_year.items():
        print(f"{year}: {len(albums)} album")
    
    # Salva risultati
    discography.save_to_file("output.json")

asyncio.run(main())
```

## 📁 Struttura del Progetto

```
crawl-lyrics/
├── src/
│   ├── models/                 # Modelli dati Pydantic
│   │   └── discography.py     # Track, Album, Artist, Discography
│   ├── services/              # Client API
│   │   ├── musicbrainz_client.py  # API MusicBrainz
│   │   └── lastfm_client.py   # API Last.fm
│   ├── crawlers/              # Logica crawling
│   │   └── base_crawler.py    # Rate limiting, retry, stats
│   └── discography_crawler.py # Crawler principale
├── tests/                     # Test unitari e integrazione
├── examples/                  # Esempi e demo
│   ├── basic_usage.py        # Esempio completo
│   └── demo.py              # Demo con dati mock
├── main.py                   # Interface CLI
├── requirements.txt
├── SETUP.md                 # Guida dettagliata
└── LICENSE
```

## 🔧 Configurazione Avanzata

### API Last.fm (Raccomandato)

1. **Registrati** su https://www.last.fm/api
2. **Crea applicazione** e ottieni API key gratuita
3. **Configura ambiente**:

```bash
# Copia file di esempio
cp .env.example .env

# Modifica .env
LASTFM_API_KEY=your_api_key_here
RATE_LIMIT_REQUESTS=5
LOG_LEVEL=INFO
```

### Rate Limiting

```python
# Configurazione personalizzata
crawler = DiscographyCrawler(
    rate_limit_requests=3,    # 3 richieste
    rate_limit_window=60,     # per 60 secondi
    max_retries=5            # 5 tentativi per richiesta
)
```

## 🧪 Test ed Esempi

```bash
# Test completi
python -m pytest tests/ -v

# Solo test base (veloci)
python -m pytest tests/test_crawler.py::TestModels -v

# Test di integrazione (richiedono internet)
python -m pytest tests/ -m integration

# Demo interattivo
python examples/basic_usage.py

# Demo con dati di esempio
python examples/demo.py
```

## 📊 API e Fonti Dati

### MusicBrainz (Principale)
- 🌍 **Database musicale open source**
- ✅ **Dati accurati e verificati dalla community**
- 🆓 **Nessuna registrazione richiesta**
- ⏱️ **Rate limit: 1 richiesta/secondo**
- 📚 **Metadati completi su artisti, album, tracce**

### Last.fm (Opzionale)
- 🎯 **Informazioni aggiuntive su generi musicali**
- 📈 **Statistiche di popolarità**
- 🆓 **API key gratuita richiesta**
- 🎨 **Arricchisce i dati MusicBrainz**

## 📈 Funzionalità Analitiche

```python
# Statistiche automatiche
print(f"Periodo attività: {discography.discography_span}")
print(f"Album per tipo: {discography.get_albums_by_type()}")
print(f"Produzione per anno: {discography.get_albums_by_year()}")

# Durata totale discografia
total_duration = sum(album.total_duration_ms for album in discography.albums)
print(f"Durata totale: {total_duration / 3600000:.1f} ore")
```

## ⚖️ Note Legali e Etiche

### ✅ Conformità Copyright
- **Solo metadati pubblici**: titoli, date, durate
- **Nessun contenuto protetto**: no testi, no audio
- **API legittime**: MusicBrainz, Last.fm
- **Rate limiting**: rispetto dei termini di servizio

### 🎯 Casi d'Uso Legittimi
- 📚 **Ricerca accademica** sulla musica
- 📊 **Analisi statistiche** di mercato
- 🤖 **Sistemi di raccomandazione**
- 📱 **App di catalogazione** personale
- 📈 **Business intelligence** musicale

## 🚨 Limitazioni Importanti

1. **NO testi delle canzoni** (copyright protetti)
2. **Dipende dalla qualità dei dati** delle API pubbliche
3. **Rate limiting** può rallentare crawling massivi
4. **Alcuni artisti** potrebbero avere dati limitati
5. **Solo per uso educativo/ricerca**

## 🛠️ Troubleshooting

### Problemi Comuni

**Nessun album trovato:**
```bash
# Prova varianti del nome
python main.py --search "Beatles" --limit 10
python main.py "The Beatles"  # Usa il nome esatto
```

**Errori di connessione:**
```bash
# Modalità verbose per debug
python main.py "Artista" --verbose

# Controlla log
cat crawler.log
```

**Rate limit errors:**
- Il sistema gestisce automaticamente
- Configura rate più conservativo in `.env`

## 🤝 Contribuire

1. **Fork** del repository
2. **Crea branch** per feature: `git checkout -b feature/nome`
3. **Commit** modifiche: `git commit -m 'Aggiunge feature'`
4. **Push** branch: `git push origin feature/nome`
5. **Apri Pull Request**

### Aree di Miglioramento
- 🔌 **Nuovi provider** di dati musicali
- 🎨 **Frontend web** per il crawler
- 📊 **Visualizzazioni** avanzate
- 🌐 **API REST** wrapper
- 🚀 **Performance** ottimizzazioni

## 📄 Licenza

MIT License - Vedi [LICENSE](LICENSE) per dettagli completi.

**Importante**: Questo software è progettato per rispettare rigorosamente le leggi sul copyright. Gli utenti sono responsabili dell'uso appropriato.

---

## 💡 Ispirazione e Crediti

- 🎵 **MusicBrainz Project** - Database musicale open source
- 🔴 **Last.fm** - Statistiche e metadati musicali  
- 🐍 **Python Community** - Librerie fantastiche
- 📚 **Pydantic** - Validazione dati robusta
- ⚡ **aiohttp** - HTTP asincrono

**Happy Crawling! 🎵🚀**
