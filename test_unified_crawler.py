#!/usr/bin/env python3
"""
Test automatico per verificare il funzionamento del Discography Crawler unificato.
Questo script dimostra tutte le funzionalità senza input utente.
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(__file__))

# Import del modulo principale
from crawl_discography import DiscographyDownloader, GENIUS_CONFIG

def test_basic_functionality():
    """Test delle funzionalità base del downloader."""
    print("🧪 TEST AUTOMATICO - Discography Crawler")
    print("="*50)
    
    # Inizializza il downloader
    print("1️⃣ Inizializzazione downloader...")
    downloader = DiscographyDownloader(GENIUS_CONFIG['access_token'])
    print("✅ Downloader inizializzato correttamente")
    
    # Test ricerca artista
    print("\n2️⃣ Test ricerca artista...")
    test_artist = "Radiohead"
    
    try:
        # Test rapido con 1 canzone
        artist = downloader.genius.search_artist(test_artist, max_songs=1)
        if artist:
            print(f"✅ Artista trovato: {artist.name}")
        else:
            print(f"❌ Artista non trovato: {test_artist}")
            return False
    except Exception as e:
        print(f"❌ Errore nella ricerca: {e}")
        return False
    
    # Test generazione filename
    print("\n3️⃣ Test generazione filename...")
    filename = downloader.generate_output_filename(artist.name)
    print(f"✅ Filename generato: {filename}")
    
    # Verifica formato timestamp
    if filename.count('.') >= 2 and filename.endswith('.json'):
        print("✅ Formato filename corretto")
    else:
        print("❌ Formato filename errato")
        return False
    
    print("\n4️⃣ Test download limitato (3 canzoni)...")
    
    try:
        # Download di sole 3 canzoni per test rapido
        artist_full = downloader.download_complete_discography(artist.name, max_songs=3)
        
        if artist_full and len(artist_full.songs) > 0:
            print(f"✅ Download test completato: {len(artist_full.songs)} canzoni")
            
            # Test salvataggio
            print("\n5️⃣ Test salvataggio...")
            test_filename = f"test_{filename}"
            
            if downloader.save_discography(artist_full, test_filename):
                print("✅ Salvataggio test completato")
                
                # Verifica file creato
                if Path(test_filename).exists():
                    file_size = Path(test_filename).stat().st_size
                    print(f"✅ File verificato: {file_size} bytes")
                    
                    # Cleanup
                    try:
                        Path(test_filename).unlink()
                        print("✅ Cleanup completato")
                    except:
                        print("⚠️  Cleanup fallito (file potrebbe essere in uso)")
                    
                    return True
                else:
                    print("❌ File non creato")
                    return False
            else:
                print("❌ Salvataggio fallito")
                return False
        else:
            print("❌ Download test fallito")
            return False
            
    except Exception as e:
        print(f"❌ Errore durante test download: {e}")
        return False

def test_filename_generation():
    """Test specifico per la generazione dei filename."""
    print("\n🧪 TEST GENERAZIONE FILENAME")
    print("="*40)
    
    downloader = DiscographyDownloader(GENIUS_CONFIG['access_token'])
    
    test_cases = [
        "Radiohead",
        "The Beatles", 
        "Pink Floyd",
        "AC/DC",
        "Guns N' Roses",
        "Twenty One Pilots",
        "Måneskin"
    ]
    
    for artist in test_cases:
        filename = downloader.generate_output_filename(artist)
        print(f"📝 {artist:20} → {filename}")
    
    print("✅ Test generazione filename completato")

def show_demo_usage():
    """Mostra esempi di utilizzo del software."""
    print("\n🎯 ESEMPI DI UTILIZZO")
    print("="*40)
    
    print("💻 Avvio normale:")
    print("   python crawl_discography.py")
    print()
    
    print("🎤 Flusso tipico:")
    print("   1. Script chiede nome artista")
    print("   2. Conferma artista trovato")
    print("   3. Imposta numero max canzoni")
    print("   4. Conferma download")
    print("   5. Download automatico")
    print("   6. Salvataggio con timestamp")
    print()
    
    print("📁 File di output esempi:")
    downloader = DiscographyDownloader(GENIUS_CONFIG['access_token'])
    examples = ["Radiohead", "Pink Floyd", "The Beatles"]
    
    for artist in examples:
        filename = downloader.generate_output_filename(artist)
        print(f"   • {filename}")

def main():
    """Funzione principale del test."""
    print("🚀 AVVIO TEST AUTOMATICO")
    print("Verifica funzionamento Discography Crawler unificato")
    print()
    
    # Test funzionalità base
    if test_basic_functionality():
        print("\n🎉 TUTTI I TEST SUPERATI!")
        print("Il software è pronto per l'uso")
    else:
        print("\n❌ ALCUNI TEST FALLITI")
        print("Controlla la configurazione")
        return 1
    
    # Test aggiuntivi
    test_filename_generation()
    show_demo_usage()
    
    print("\n" + "="*60)
    print("🎵 CRAWLER PRONTO!")
    print("Esegui: python crawl_discography.py")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
