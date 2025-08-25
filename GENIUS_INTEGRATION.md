# Integrazione Genius API - Riepilogo

## 🎯 Implementazione Completata

L'integrazione con l'API Genius è stata implementata con successo nel progetto didattico crawl-lyrics. Ecco un riepilogo completo delle funzionalità aggiunte:

## 🔧 Componenti Implementati

### 1. Client Genius (`src/services/genius_client.py`)
- ✅ **Autenticazione completa** con client_id, client_secret e access_token
- ✅ **Rate limiting rispettoso** (500ms tra richieste, max 60/minuto)
- ✅ **Ricerca artisti** con match intelligente
- ✅ **Recupero canzoni** per artista con paginazione
- ✅ **Ricerca canzoni specifiche** per titolo e artista
- ✅ **Metadati completi** (popolarità, date, album, collaborazioni)
- ✅ **Gestione errori** robusta e logging dettagliato

### 2. Credenziali Integrate
```python
GENIUS_CONFIG = {
    'client_id': 'zPwicLU4TnfKE-O8YL7O8U6Rc40MGePoR5k8pTQG_LijOMWVnAbjCDBQT1Kgz22w',
    'client_secret': 'g1VtZNBTj4lVsElMkW8OankwxK7RqKNZOBGeZvijwLIMqEg5qBf3QIiR4tSPsxIctZOMs-HCzfQ50j9kHpHQuw',
    'access_token': '2myLsXND-Qngtcqve_5SnrSv5cYb1vg8A9062VkOqQIGg59XVxkNujtmSOID5lNB'
}
```

### 3. Integrazione nel Crawler Principale
- ✅ **Configurazione flessibile** (credenziali integrate o personalizzate)
- ✅ **Dati arricchiti** da Genius aggiunti ai metadati
- ✅ **Riferimenti etici ai testi** (NO testi completi)
- ✅ **Multi-fonte** (MusicBrainz + Last.fm + Genius)

### 4. Modelli Aggiornati
- ✅ **Campo metadata** aggiunto a `Discography`
- ✅ **Campi lyrics_reference** e `genius_url` per le tracce
- ✅ **Supporto per metadati Genius** nell'artista

## 🚀 Modalità di Utilizzo

### CLI - Comando Base
```bash
# Con credenziali integrate (pronto all'uso)
python main.py "Nirvana" --include-lyrics-refs

# Con token personalizzato
python main.py "Radiohead" --genius-token YOUR_TOKEN --include-lyrics-refs

# Disabilita credenziali integrate
python main.py "Queen" --no-genius-builtin
```

### Programmatico
```python
from src.discography_crawler import crawl_artist_discography

# Con Genius integrato
discography = await crawl_artist_discography(
    "Nirvana",
    use_genius_builtin=True,
    include_lyrics_references=True
)

# Accesso ai dati Genius
genius_data = discography.metadata['genius']
print(f"Canzoni trovate: {genius_data['total_songs_found']}")
```

### API Diretta
```python
from src.services.genius_client import search_genius_artist, GENIUS_CONFIG

artist_data = await search_genius_artist(
    "Radiohead",
    GENIUS_CONFIG['client_id'],
    GENIUS_CONFIG['client_secret'],
    GENIUS_CONFIG['access_token']
)
```

## 📊 Output Genius

### Dati Artista
```json
{
  "genius_id": 12712,
  "name": "Nirvana",
  "url": "https://genius.com/artists/Nirvana",
  "followers_count": 2230,
  "verified": false,
  "total_songs_found": 60,
  "songs": [
    {
      "title": "Smells Like Teen Spirit",
      "page_views": 3447318,
      "url": "https://genius.com/Nirvana-smells-like-teen-spirit-lyrics",
      "release_date": "September 10, 1991"
    }
  ]
}
```

### Riferimenti Testi Etici
```json
{
  "title": "Smells Like Teen Spirit",
  "lyrics_reference": {
    "official_lyrics_url": "https://genius.com/Nirvana-smells-like-teen-spirit-lyrics",
    "how_to_access": "Visita il link ufficiale per i testi completi",
    "legal_notice": "I testi sono protetti da copyright"
  }
}
```

## ✅ Test Effettuati

### 1. Test Configurazione
```bash
✅ Configurazione Genius: zPwicLU4TnfKE-O8YL7O...
```

### 2. Test Ricerca Artisti
```bash
✅ Trovati 3 artisti:
  1. Nirvana (1980s–1990s US grunge band) [US]
  2. Nirvana (60s band from the UK) [GB]  
  3. Approaching Nirvana [US]
```

### 3. Test Demo Completa
```bash
✅ Trovato: Nirvana
🔗 URL: https://genius.com/artists/Nirvana
👥 Follower: 2230
🎵 Canzoni trovate: 60

🎵 Canzoni più popolari:
  1. Smells Like Teen Spirit - 3,447,318 visualizzazioni
  2. Come as You Are - 2,136,780 visualizzazioni
  3. Heart-Shaped Box - 1,361,373 visualizzazioni
```

## 🔒 Rispetto del Copyright

### Cosa FORNISCE ✅
- Link ufficiali ai testi su Genius
- Metadati pubblici (titoli, artisti, date)
- Snippet minimi per identificazione (Fair Use)
- Informazioni su popolarità e visualizzazioni

### Cosa NON FORNISCE ❌
- Testi completi delle canzoni
- Contenuto protetto da copyright
- Redistribuzione di materiale coperto da diritti d'autore

### Disclaimer Integrato
```
🚨 IMPORTANTE DISCLAIMER LEGALE 🚨

I testi delle canzoni sono protetti da copyright. Questo sistema:

✅ FORNISCE: Link ufficiali ai testi
✅ FORNISCE: Metadati pubblici per identificazione  
✅ FORNISCE: Snippet minimi per Fair Use educativo

❌ NON FORNISCE: Testi completi protetti da copyright
❌ NON MEMORIZZA: Contenuto protetto da diritti d'autore
❌ NON REDISTRIBUISCE: Materiale sotto copyright
```

## 🎯 Vantaggi dell'Integrazione

1. **Dati Arricchiti**: Informazioni aggiuntive su popolarità e metadati
2. **Identificazione Accurata**: Match intelligente di artisti e canzoni
3. **Accesso Legale**: Link diretti ai testi ufficiali
4. **Multi-fonte**: Combinazione di MusicBrainz, Last.fm e Genius
5. **Educativo**: Perfetto per progetti didattici e di ricerca

## 📁 File Modificati/Creati

### Nuovi File
- `src/services/genius_client.py` - Client principale Genius
- `examples/genius_demo.py` - Demo completa dell'integrazione
- `tests/test_genius_integration.py` - Test per l'integrazione

### File Modificati
- `src/discography_crawler.py` - Integrazione nel crawler principale
- `src/models/discography.py` - Aggiunto campo metadata
- `main.py` - Nuove opzioni CLI per Genius
- `README.md` - Documentazione aggiornata

## 🚀 Prossimi Passi

L'integrazione è completa e pronta per l'uso. Possibili miglioramenti futuri:
- Cache dei risultati Genius
- Integrazione con altri servizi di metadati
- Analisi avanzate della popolarità
- Export in formati diversi (CSV, XML, etc.)

---

**Progetto**: crawl-lyrics  
**Scopo**: Didattico/Educativo  
**Licenza**: Rispetto rigoroso del copyright  
**Data**: 25 Agosto 2025
