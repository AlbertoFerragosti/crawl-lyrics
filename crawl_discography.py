#!/usr/bin/env python3
"""
Discography Crawler - Script unificato per il download di discografie complete
Versione rifatorizzata con un unico entry point per uso semplificato.

Funzionalità:
- Input interattivo dell'artista da terminale  
- Download completo della discografia con testi tramite Genius API
- Output in formato timestamp.nomeartista.json
- Gestione errori robusta e progress feedback
"""

import json
import time
import re
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from lyricsgenius import Genius

# Configurazione Genius API integrata
GENIUS_CONFIG = {
    'client_id': 'zPwicLU4TnfKE-O8YL7O8U6Rc40MGePoR5k8pTQG_LijOMWVnAbjCDBQT1Kgz22w',
    'client_secret': 'g1VtZNBTj4lVsElMkW8OankwxK7RqKNZOBGeZvijwLIMqEg5qBf3QIiR4tSPsxIctZOMs-HCzfQ50j9kHpHQuw',
    'access_token': '2myLsXND-Qngtcqve_5SnrSv5cYb1vg8A9062VkOqQIGg59XVxkNujtmSOID5lNB'
}

class DiscographyDownloader:
    """
    Classe principale per il download di discografie complete con testi.
    Utilizza LyricsGenius per accesso diretto ai contenuti musicali.
    """
    
    def __init__(self, access_token: str):
        """
        Inizializza il downloader con configurazione ottimizzata.
        
        Args:
            access_token: Token di accesso Genius API
        """
        self.genius = Genius(access_token)
        
        # Configurazione per uso responsabile e performance ottimali
        self.genius.timeout = 30
        self.genius.sleep_time = 0.5  # Pausa tra richieste per rispettare rate limits
        self.genius.verbose = False   # Disabilita output verboso della libreria
        self.genius.remove_section_headers = True
        self.genius.skip_non_songs = True
        self.genius.excluded_terms = ["(Remix)", "(Live)", "(Acoustic)", "(Demo)", "(Remaster)"]
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('crawler.log')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def search_artist_interactive(self) -> str:
        """
        Interfaccia interattiva per la ricerca dell'artista.
        
        Returns:
            Nome dell'artista scelto dall'utente
        """
        print("\n" + "="*60)
        print("🎵 DISCOGRAPHY CRAWLER - Download Completo Discografie")
        print("="*60)
        print("💡 Scarica la discografia completa di qualsiasi artista con testi!")
        print("🎯 Powered by Genius API per massima accuratezza")
        print()
        
        while True:
            artist_name = input("🎤 Inserisci il nome dell'artista: ").strip()
            
            if not artist_name:
                print("❌ Per favore inserisci un nome valido.")
                continue
            
            print(f"\n🔍 Cercando '{artist_name}' su Genius...")
            
            # Verifica che l'artista esista
            try:
                # Test rapido con 1 sola canzone per verificare esistenza
                test_artist = self.genius.search_artist(artist_name, max_songs=1)
                if test_artist:
                    print(f"✅ Trovato: {test_artist.name}")
                    
                    # Chiedi conferma se il nome è diverso
                    if test_artist.name.lower() != artist_name.lower():
                        confirm = input(f"🤔 Confermi '{test_artist.name}'? (s/n): ").lower()
                        if confirm not in ['s', 'si', 'sì', 'y', 'yes']:
                            continue
                    
                    return test_artist.name
                else:
                    print(f"❌ Artista '{artist_name}' non trovato.")
                    retry = input("🔄 Vuoi riprovare con un altro nome? (s/n): ").lower()
                    if retry not in ['s', 'si', 'sì', 'y', 'yes']:
                        print("👋 Arrivederci!")
                        sys.exit(0)
                    continue
                    
            except Exception as e:
                self.logger.error(f"Errore nella ricerca artista: {e}")
                print(f"❌ Errore nella ricerca: {e}")
                retry = input("🔄 Vuoi riprovare? (s/n): ").lower()
                if retry not in ['s', 'si', 'sì', 'y', 'yes']:
                    print("👋 Arrivederci!")
                    sys.exit(0)
    
    def download_complete_discography(self, artist_name: str, max_songs: int = 200) -> Optional[Any]:
        """
        Scarica la discografia completa di un artista con tutti i testi.
        
        Args:
            artist_name: Nome dell'artista
            max_songs: Numero massimo di canzoni da scaricare (default: 200)
            
        Returns:
            Oggetto Artist con la discografia completa o None se errore
        """
        try:
            print(f"\n🎵 Inizio download discografia di '{artist_name}'")
            print(f"📊 Limite massimo: {max_songs} canzoni")
            print("⏱️  Questo potrebbe richiedere alcuni minuti...")
            print()
            
            # Scarica la discografia completa
            self.logger.info(f"Inizio download discografia per {artist_name}")
            
            artist = self.genius.search_artist(
                artist_name, 
                max_songs=max_songs,
                sort="popularity"  # Ordina per popolarità per avere prima i brani migliori
            )
            
            if artist:
                print(f"✅ Download completato!")
                print(f"👤 Artista: {artist.name}")
                print(f"🎵 Canzoni scaricate: {len(artist.songs)}")
                
                # Mostra preview delle prime canzoni
                print(f"\n📋 Prime 10 canzoni trovate:")
                for i, song in enumerate(artist.songs[:10], 1):
                    print(f"  {i:2d}. {song.title}")
                
                if len(artist.songs) > 10:
                    print(f"     ... e altre {len(artist.songs) - 10} canzoni")
                
                self.logger.info(f"Download completato: {len(artist.songs)} canzoni per {artist_name}")
                return artist
            else:
                print(f"❌ Impossibile scaricare la discografia di '{artist_name}'")
                return None
                
        except Exception as e:
            self.logger.error(f"Errore durante download discografia {artist_name}: {e}")
            print(f"❌ Errore durante il download: {e}")
            return None
    
    def generate_output_filename(self, artist_name: str) -> str:
        """
        Genera il nome del file di output con timestamp.
        
        Args:
            artist_name: Nome dell'artista
            
        Returns:
            Nome del file nel formato timestamp.nomeartista.json
        """
        # Genera timestamp nel formato YYYYMMDD_HHMMSS
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Pulisci il nome dell'artista per renderlo safe per filename
        safe_name = re.sub(r'[^\w\s-]', '', artist_name)  # Rimuovi caratteri speciali
        safe_name = re.sub(r'[-\s]+', '_', safe_name)     # Sostituisci spazi e trattini con underscore
        safe_name = safe_name.lower().strip('_')          # Lowercase e rimuovi underscore iniziali/finali
        
        return f"{timestamp}.{safe_name}.json"
    
    def save_discography(self, artist, filename: str) -> bool:
        """
        Salva la discografia nel file specificato.
        
        Args:
            artist: Oggetto Artist di LyricsGenius
            filename: Nome del file di output
            
        Returns:
            True se il salvataggio è riuscito, False altrimenti
        """
        try:
            print(f"\n💾 Salvataggio in corso...")
            print(f"📁 File: {filename}")
            
            # Salva usando il metodo nativo di LyricsGenius
            artist.save_lyrics(filename=filename, overwrite=True)
            
            # Verifica che il file sia stato creato e ottieni le dimensioni
            file_path = Path(filename)
            if file_path.exists():
                file_size = file_path.stat().st_size
                file_size_mb = file_size / (1024 * 1024)
                
                print(f"✅ Discografia salvata con successo!")
                print(f"📄 File: {file_path.absolute()}")
                print(f"📊 Dimensione: {file_size_mb:.2f} MB")
                
                self.logger.info(f"File salvato: {filename} ({file_size_mb:.2f} MB)")
                return True
            else:
                print(f"❌ Errore: file {filename} non creato")
                return False
                
        except Exception as e:
            self.logger.error(f"Errore durante salvataggio {filename}: {e}")
            print(f"❌ Errore durante il salvataggio: {e}")
            return False
    
    def show_download_summary(self, artist, filename: str):
        """
        Mostra un riepilogo del download completato.
        
        Args:
            artist: Oggetto Artist scaricato
            filename: Nome del file salvato
        """
        print(f"\n" + "="*60)
        print("🎉 DOWNLOAD COMPLETATO!")
        print("="*60)
        print(f"👤 Artista: {artist.name}")
        print(f"🎵 Canzoni: {len(artist.songs)}")
        print(f"📁 File: {filename}")
        
        # Calcola alcune statistiche interessanti
        if artist.songs:
            # Trova la canzone più popolare (se disponibile)
            try:
                most_popular = max(artist.songs, key=lambda s: getattr(s, 'pyongs_count', 0) or 0)
                print(f"⭐ Canzone più popolare: {most_popular.title}")
            except:
                pass
            
            # Trova l'anno più vecchio e più recente (se disponibile)
            years = []
            for song in artist.songs:
                if hasattr(song, 'year') and song.year:
                    years.append(song.year)
            
            if years:
                print(f"📅 Periodo: {min(years)} - {max(years)}")
        
        print(f"\n💡 Il file contiene:")
        print(f"   • Testi completi di tutte le canzoni")
        print(f"   • Metadati dettagliati (date, popolarità, ecc.)")
        print(f"   • Informazioni sull'artista")
        print(f"   • Link alle fonti originali")
        print()
        print("🎯 Usa il file JSON per analisi, ricerche, o altri progetti!")
        print("="*60)


def main():
    """
    Funzione principale - Entry point unico del programma.
    """
    try:
        # Inizializza il downloader con le credenziali integrate
        downloader = DiscographyDownloader(GENIUS_CONFIG['access_token'])
        
        # Interfaccia interattiva per scegliere l'artista
        artist_name = downloader.search_artist_interactive()
        
        # Chiedi conferma per procedere
        print(f"\n🚀 Pronto a scaricare la discografia completa di '{artist_name}'")
        max_songs = input("📊 Numero massimo di canzoni (default 200, premi INVIO): ").strip()
        
        # Valida input numero massimo canzoni
        try:
            max_songs = int(max_songs) if max_songs else 200
            if max_songs <= 0:
                max_songs = 200
                print(f"⚠️  Valore non valido, uso default: {max_songs}")
        except ValueError:
            max_songs = 200
            print(f"⚠️  Valore non valido, uso default: {max_songs}")
        
        # Conferma finale
        confirm = input(f"✅ Confermi il download? (s/n): ").lower()
        if confirm not in ['s', 'si', 'sì', 'y', 'yes']:
            print("❌ Download annullato dall'utente.")
            return
        
        # Scarica la discografia completa
        artist = downloader.download_complete_discography(artist_name, max_songs)
        
        if artist:
            # Genera nome file con timestamp
            filename = downloader.generate_output_filename(artist.name)
            
            # Salva su disco
            if downloader.save_discography(artist, filename):
                # Mostra riepilogo finale
                downloader.show_download_summary(artist, filename)
            else:
                print("❌ Errore durante il salvataggio del file.")
                sys.exit(1)
        else:
            print("❌ Download fallito. Impossibile procedere.")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Download interrotto dall'utente.")
        print("👋 Arrivederci!")
        sys.exit(0)
    
    except Exception as e:
        logging.error(f"Errore critico nel main: {e}")
        print(f"\n❌ Errore critico: {e}")
        print("\n💡 Suggerimenti:")
        print("  • Verifica la connessione internet")
        print("  • Riprova con un nome artista diverso")
        print("  • Controlla il file crawler.log per dettagli")
        sys.exit(1)


if __name__ == "__main__":
    main()
