# 🎵 Discography Crawler - Versione Unificata

## 📝 Descrizione

Questo è lo script unificato e rifatorizzato per il download completo di discografie musicali con testi. Il software è stato semplificato in un **unico entry point** che permette di:

- 🎤 **Input interattivo**: Chiede all'utente il nome dell'artista da terminale
- 🎵 **Download completo**: Scarica l'intera discografia con tutti i testi tramite Genius API
- 📁 **Output timestampato**: Salva tutto in un file `timestamp.nomeartista.json`
- ✅ **Interfaccia user-friendly**: Guida l'utente passo-passo con feedback visivo

## 🚀 Utilizzo

### Avvio rapido
```bash
python crawl_discography.py
```

### Flusso interattivo
1. **Input artista**: Lo script chiede il nome dell'artista
2. **Conferma ricerca**: Verifica che l'artista sia stato trovato correttamente
3. **Configurazione download**: Permette di impostare il numero massimo di canzoni
4. **Conferma finale**: Chiede conferma prima di iniziare il download
5. **Download progress**: Mostra il progresso del download
6. **Salvataggio**: Salva automaticamente con nome timestampato

### Esempio di utilizzo
```
============================================================
🎵 DISCOGRAPHY CRAWLER - Download Completo Discografie
============================================================
💡 Scarica la discografia completa di qualsiasi artista con testi!
🎯 Powered by Genius API per massima accuratezza

🎤 Inserisci il nome dell'artista: Radiohead

🔍 Cercando 'Radiohead' su Genius...
✅ Trovato: Radiohead

🚀 Pronto a scaricare la discografia completa di 'Radiohead'
📊 Numero massimo di canzoni (default 200, premi INVIO): 50
✅ Confermi il download? (s/n): s

🎵 Inizio download discografia di 'Radiohead'
📊 Limite massimo: 50 canzoni
⏱️  Questo potrebbe richiedere alcuni minuti...

✅ Download completato!
👤 Artista: Radiohead
🎵 Canzoni scaricate: 50

📋 Prime 10 canzoni trovate:
   1. Creep
   2. Karma Police
   3. No Surprises
   4. Paranoid Android
   5. High and Dry
   6. Just
   7. Fake Plastic Trees
   8. Street Spirit (Fade Out)
   9. 15 Step
  10. Weird Fishes/Arpeggi
     ... e altre 40 canzoni

💾 Salvataggio in corso...
📁 File: 20250825_143022.radiohead.json

✅ Discografia salvata con successo!
📄 File: C:\bitfortex\dev-projects\crawl-lyrics\20250825_143022.radiohead.json
📊 Dimensione: 2.45 MB

============================================================
🎉 DOWNLOAD COMPLETATO!
============================================================
👤 Artista: Radiohead
🎵 Canzoni: 50
📁 File: 20250825_143022.radiohead.json
⭐ Canzone più popolare: Creep
📅 Periodo: 1992 - 2016

💡 Il file contiene:
   • Testi completi di tutte le canzoni
   • Metadati dettagliati (date, popolarità, ecc.)
   • Informazioni sull'artista
   • Link alle fonti originali

🎯 Usa il file JSON per analisi, ricerche, o altri progetti!
============================================================
```

## 📁 Output File Format

Il file di output segue il formato: `YYYYMMDD_HHMMSS.nomeartista.json`

Esempi:
- `20250825_143022.radiohead.json`
- `20250825_144530.pink_floyd.json`
- `20250825_150045.the_beatles.json`

## 🔧 Caratteristiche Tecniche

### API Integration
- **Genius API**: Utilizza credenziali integrate per accesso immediato
- **LyricsGenius Library**: Sfrutta la libreria ufficiale per massima compatibilità
- **Rate Limiting**: Rispetta automaticamente i limiti di richiesta (0.5s tra chiamate)

### Gestione Errori
- ✅ Verifica connessione internet
- ✅ Validazione input utente
- ✅ Gestione artisti non trovati
- ✅ Retry automatico su errori temporanei
- ✅ Logging dettagliato in `crawler.log`

### Performance Features
- 🚀 **Configurazione ottimizzata**: Timeout e parametri bilanciati
- 🎯 **Ordinamento intelligente**: Download per popolarità per avere prima i brani migliori
- 🔍 **Filtri automatici**: Esclude remix, live, demo automaticamente
- 💾 **Salvataggio efficiente**: Usa il formato nativo di LyricsGenius

## 🛠️ Requisiti

### Dipendenze Python
```bash
pip install lyricsgenius>=3.0.1
```

### Sistema
- Python 3.7+
- Connessione internet attiva
- Spazio su disco (i file possono essere 1-10MB a seconda dell'artista)

## 🎯 Vantaggi della Rifatorizzazione

### Prima (codebase complessa)
- ❌ Multipli file e moduli
- ❌ Configurazione complessa
- ❌ CLI con molte opzioni
- ❌ Dipendenze da multiple API
- ❌ Setup complicato

### Ora (script unificato)
- ✅ **Un solo file**: `crawl_discography.py`
- ✅ **Zero configurazione**: Credenziali integrate
- ✅ **Interfaccia semplice**: Solo input interattivo
- ✅ **Focus Genius**: Una sola API, massima affidabilità
- ✅ **Plug & Play**: Basta un comando

## 🔒 Note Legali

- 📚 **Uso didattico**: Lo script è pensato per scopi educativi e di ricerca
- 🔗 **Link ufficiali**: Include sempre riferimenti alle fonti originali
- ⚖️ **Rispetto copyright**: Segue le policy di Genius per l'accesso ai contenuti
- 🎯 **Fair Use**: Utilizzo responsabile delle API pubbliche

## 🚨 Troubleshooting

### Errore "ModuleNotFoundError: No module named 'lyricsgenius'"
```bash
pip install lyricsgenius
```

### Errore di rete
- Verifica connessione internet
- Riprova dopo alcuni minuti
- Controlla il file `crawler.log` per dettagli

### Artista non trovato
- Prova varianti del nome (es. "The Beatles" vs "Beatles")
- Controlla la grafia
- Usa nomi in inglese quando possibile

### File non salvato
- Verifica permessi di scrittura nella directory
- Assicurati di avere spazio su disco
- Controlla il log per errori specifici

## 📞 Supporto

Per problemi o domande, controlla:
1. Il file `crawler.log` per errori dettagliati
2. La connessione internet
3. I requisiti di sistema

---

**🎵 Buon download delle tue discografie preferite!**
