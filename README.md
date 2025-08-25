# Music Discography Crawler

Un sistema Python professionale per recuperare informazioni sulla discografia degli artisti musicali utilizzando API pubbliche e web scraping etico.

## ⚠️ Disclaimer Copyright

Questo progetto rispetta rigorosamente le leggi sul copyright:
- ✅ Recupera solo **metadati pubblici** (titoli, anni, nomi album)  
- ❌ **NON estrae testi completi** delle canzoni
- ✅ Utilizza **API pubbliche legittime** (MusicBrainz, Last.fm, Genius)
- ✅ Implementa **rate limiting** per rispettare i servizi
- ✅ **Solo per scopi educativi/ricerca**

## 🎯 Nuove Funzionalità - Integrazione Genius

🎵 **Genius API integrata** per metadati arricchiti:
- ✅ Informazioni complete su artisti e canzoni
- ✅ Link ufficiali ai testi (NO testi completi)
- ✅ Metadati pubblici (popolarità, date di rilascio)
- ✅ Credenziali integrate per uso immediato
- ✅ Opzione per token personalizzati

## 🚀 Quick Start

```bash
# Installazione
pip install -r requirements.txt

# Cerca un artista
python main.py --search "Radiohead"

# Crawling con Genius integrato
python main.py "Radiohead" --include-lyrics-refs

# Crawling discografia completa con tutte le fonti
python main.py "Pink Floyd" --lastfm-key YOUR_API_KEY --include-lyrics-refs --pretty

# Con token Genius personalizzato
python main.py "Nirvana" --genius-token YOUR_TOKEN --include-lyrics-refs
```

## ✨ Caratteristiche

- 🎵 **Discografia completa** per qualsiasi artista
- 📀 **Metadati dettagliati** su album e tracce
- 📅 **Date di pubblicazione** e informazioni cronologiche
- 🎤 **Dati Genius integrati** (popolarità, link testi, metadati)
- 🔗 **Riferimenti etici ai testi** (NO testi completi)
- 🚀 **Architettura asincrona** e scalabile
- 🛡️ **Rate limiting** e gestione errori robusta
- 📊 **Output JSON strutturato** per analisi
- 🔍 **Ricerca intelligente** artisti
- 📈 **Statistiche automatiche** della discografia
- 🎯 **Multi-fonte**: MusicBrainz + Last.fm + Genius

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

## 🎤 Integrazione Genius API

### Credenziali Integrate
Il progetto include credenziali Genius preconfigurate per uso didattico:
- ✅ **Pronto all'uso** - nessuna configurazione richiesta
- ✅ **Rate limiting rispettoso** - 60 richieste/minuto
- ✅ **Solo metadati pubblici** - rispetta copyright

### Funzionalità Genius
```bash
# Usa Genius con credenziali integrate
python main.py "Nirvana" --include-lyrics-refs

# Con token personalizzato
python main.py "Radiohead" --genius-token YOUR_TOKEN --include-lyrics-refs

# Disabilita Genius integrato
python main.py "Queen" --no-genius-builtin
```

### Dati Recuperati da Genius
- 🎵 **Metadati canzoni**: popolarità, visualizzazioni, date
- 🔗 **Link ufficiali** ai testi (NO testi completi)
- 👤 **Info artista**: follower, verifiche, social media
- 📊 **Statistiche**: canzoni più popolari, collaborazioni
- 🎯 **Identificazione accurata** di tracce e album

### Esempio Output con Genius
```json
{
  "artist": {
    "name": "Nirvana",
    "sources": ["MusicBrainz", "Genius"]
  },
  "metadata": {
    "genius": {
      "name": "Nirvana",
      "followers_count": 1500000,
      "verified": true,
      "total_songs_found": 120,
      "url": "https://genius.com/artists/Nirvana"
    }
  },
  "albums": [
    {
      "title": "Nevermind",
      "tracks": [
        {
          "title": "Smells Like Teen Spirit",
          "lyrics_reference": {
            "official_lyrics_url": "https://genius.com/Nirvana-smells-like-teen-spirit-lyrics",
            "how_to_access": "Visita il link ufficiale per i testi completi",
            "legal_notice": "I testi sono protetti da copyright"
          }
        }
      ]
    }
  ]
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

# Crawling base (solo MusicBrainz)
python main.py "The Beatles"

# Con Genius integrato
python main.py "Nirvana" --include-lyrics-refs

# Crawling completo (tutte le fonti)
python main.py "Pink Floyd" --lastfm-key YOUR_API_KEY --include-lyrics-refs --pretty

# Con token Genius personalizzato
python main.py "Radiohead" --genius-token YOUR_TOKEN --include-lyrics-refs

# Output personalizzato
python main.py "Queen" --output queen_complete.json --pretty --verbose

# Modalità silenziosa
python main.py "AC/DC" --quiet
```

### Uso Programmatico

```python
import asyncio
from src.discography_crawler import crawl_artist_discography

async def main():
    # Crawling con Genius integrato
    discography = await crawl_artist_discography(
        "Radiohead",
        use_genius_builtin=True,
        include_lyrics_references=True
    )
    
    print(f"Artista: {discography.artist.name}")
    print(f"Album: {discography.total_albums}")
    print(f"Tracce: {discography.total_tracks}")
    print(f"Fonti: {', '.join(discography.sources)}")
    
    # Controlla metadati Genius
    if hasattr(discography, 'metadata') and 'genius' in discography.metadata:
        genius_data = discography.metadata['genius']
        print(f"Genius: {genius_data['total_songs_found']} canzoni")
    
    # Trova tracce con riferimenti ai testi
    tracks_with_lyrics = []
    for album in discography.albums:
        for track in album.tracks:
            if hasattr(track, 'lyrics_reference'):
                tracks_with_lyrics.append(track)
    
    print(f"Tracce con riferimenti testi: {len(tracks_with_lyrics)}")
    
    # Salva risultati
    discography.save_to_file("radiohead_genius.json")

asyncio.run(main())
```

### Demo Genius
```bash
# Esegui demo completa
python examples/genius_demo.py
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
