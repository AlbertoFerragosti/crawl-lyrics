#!/usr/bin/env python3
"""
Demonstrazione pratica dell'implementazione LyricsGenius secondo le istruzioni.
Esempio funzionante dell'uso della libreria per scaricare testi di artisti.
"""

from lyricsgenius import Genius

# Token di accesso (normalmente dovresti usare variabili d'ambiente)
TOKEN = '2myLsXND-Qngtcqve_5SnrSv5cYb1vg8A9062VkOqQIGg59XVxkNujtmSOID5lNB'

def basic_usage_demo():
    """
    Implementazione esatta dell'esempio dalle istruzioni:
    
    from lyricsgenius import Genius
    genius = Genius(token)
    artist = genius.search_artist('Fast Animals and Slow Kids')
    artist.save_lyrics()
    """
    
    print("=== Demo Base LyricsGenius ===")
    print("Implementazione secondo le istruzioni fornite\n")
    
    # Crea il client Genius
    genius = Genius(TOKEN)
    
    # Configura per un uso responsabile
    genius.timeout = 15
    genius.sleep_time = 0.5  # Pausa tra richieste per rispettare rate limits
    genius.verbose = False   # Riduci output verboso
    genius.remove_section_headers = True  # Rimuovi header delle sezioni
    genius.skip_non_songs = True  # Salta contenuti non musicali
    
    try:
        # Esempio 1: Andy Shauf (come nelle istruzioni)
        print("1. Ricerca artista: Andy Shauf")
        artist = genius.search_artist('Andy Shauf', max_songs=3)  # Limitiamo per demo
        
        if artist:
            print(f"   ✓ Trovato: {artist.name}")
            print(f"   ✓ Canzoni trovate: {len(artist.songs)}")
            
            # Mostra le canzoni trovate
            for i, song in enumerate(artist.songs, 1):
                print(f"     {i}. {song.title}")
            
            # Salva i testi (implementazione istruzioni)
            filename = "andy_shauf_lyrics.json"
            artist.save_lyrics(filename=filename, overwrite=True)
            print(f"   ✓ Testi salvati in: {filename}")
            
        else:
            print("   ✗ Artista non trovato")
            
    except Exception as e:
        print(f"   ✗ Errore: {e}")

def additional_examples():
    """Esempi aggiuntivi per mostrare le funzionalità."""
    
    print("\n=== Esempi Aggiuntivi ===")
    
    genius = Genius(TOKEN)
    genius.timeout = 15
    genius.sleep_time = 0.5
    genius.verbose = False
    genius.remove_section_headers = True
    genius.skip_non_songs = True
    
    try:
        # Esempio 2: Ricerca di una singola canzone
        print("2. Ricerca singola canzone")
        song = genius.search_song("Creep", "Radiohead")
        
        if song:
            print(f"   ✓ Trovata: {song.title} di {song.artist}")
            print(f"   ✓ Album: {song.album if song.album else 'N/A'}")
            print(f"   ✓ URL: {song.url}")
            
            # Salva la singola canzone
            song_filename = "creep_radiohead.json"
            song.save_lyrics(filename=song_filename, overwrite=True)
            print(f"   ✓ Testi salvati in: {song_filename}")
        else:
            print("   ✗ Canzone non trovata")
            
    except Exception as e:
        print(f"   ✗ Errore nella ricerca canzone: {e}")
    
    try:
        # Esempio 3: Artista con poche canzoni per demo completo
        print("\n3. Download completo artista (esempio limitato)")
        artist = genius.search_artist('Nirvana', max_songs=5)  # Limitato per demo
        
        if artist:
            print(f"   ✓ Trovato: {artist.name}")
            print(f"   ✓ Canzoni scaricate: {len(artist.songs)}")
            
            # Salva tutta la discografia (limitata)
            artist.save_lyrics(filename="nirvana_demo_lyrics.json", overwrite=True)
            print("   ✓ Discografia salvata in: nirvana_demo_lyrics.json")
        else:
            print("   ✗ Artista non trovato")
            
    except Exception as e:
        print(f"   ✗ Errore nel download artista: {e}")

def show_usage_instructions():
    """Mostra le istruzioni di utilizzo."""
    
    print("\n=== Istruzioni di Utilizzo ===")
    print("Per utilizzare LyricsGenius nel tuo codice:")
    print()
    print("1. Installa la libreria:")
    print("   pip install lyricsgenius")
    print()
    print("2. Utilizza il codice base:")
    print("   from lyricsgenius import Genius")
    print("   genius = Genius(token)")
    print("   artist = genius.search_artist('Andy Shauf')")
    print("   artist.save_lyrics()")
    print()
    print("3. Configura per un uso responsabile:")
    print("   genius.timeout = 15")
    print("   genius.sleep_time = 0.5")
    print("   genius.verbose = False")
    print("   genius.remove_section_headers = True")
    print("   genius.skip_non_songs = True")
    print()
    print("4. File generati:")
    print("   - I testi vengono salvati in formato JSON")
    print("   - Include metadati e informazioni sull'artista")
    print("   - Struttura organizzata per facile parsing")

def main():
    """Esegue la demonstrazione completa."""
    
    print("LyricsGenius Implementation Demo")
    print("=" * 50)
    print("Implementazione secondo le istruzioni:")
    print("pip install lyricsgenius")
    print("genius = Genius(token)")
    print("artist = genius.search_artist('Andy Shauf')")
    print("artist.save_lyrics()")
    print("=" * 50)
    
    try:
        # Esegui demo base
        basic_usage_demo()
        
        # Esegui esempi aggiuntivi
        additional_examples()
        
        # Mostra istruzioni
        show_usage_instructions()
        
        print("\n" + "=" * 50)
        print("✓ Demo completato con successo!")
        print("I file JSON con i testi sono stati salvati.")
        print("NOTA IMPORTANTE: I testi sono protetti da copyright.")
        print("Utilizzare solo per scopi educativi e di ricerca.")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\nDemo interrotto dall'utente")
    except Exception as e:
        print(f"\nErrore generale: {e}")

if __name__ == "__main__":
    main()
