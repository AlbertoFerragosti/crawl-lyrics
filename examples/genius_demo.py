"""
Esempio di utilizzo del crawler con integrazione Genius.
Dimostra come recuperare discografie arricchite con dati da Genius.
"""

import asyncio
import json
from pathlib import Path
import sys

# Aggiungi il path src per gli import
import os
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.discography_crawler import crawl_artist_discography
from src.services.genius_client import search_genius_artist, search_genius_song, GENIUS_CONFIG


async def demo_genius_search():
    """Dimostra la ricerca diretta su Genius."""
    print("🔍 Demo: Ricerca diretta su Genius")
    print("=" * 50)
    
    # Cerca un artista su Genius
    artist_name = "Nirvana"
    print(f"🎯 Cercando '{artist_name}' su Genius...")
    
    genius_data = await search_genius_artist(
        artist_name,
        GENIUS_CONFIG['client_id'],
        GENIUS_CONFIG['client_secret'],
        GENIUS_CONFIG['access_token']
    )
    
    if genius_data:
        print(f"✅ Trovato: {genius_data['name']}")
        print(f"🔗 URL: {genius_data['url']}")
        print(f"👥 Follower: {genius_data['followers_count']}")
        print(f"🎵 Canzoni trovate: {genius_data['total_songs_found']}")
        
        # Mostra alcune canzoni popolari
        print(f"\n🎵 Canzoni più popolari:")
        for i, song in enumerate(genius_data['songs'][:5], 1):
            views = song['page_views'] or 0
            print(f"  {i}. {song['title']} - {views:,} visualizzazioni")
            print(f"     🔗 {song['url']}")
        
        return genius_data
    else:
        print("❌ Artista non trovato su Genius")
        return None


async def demo_song_search():
    """Dimostra la ricerca di una canzone specifica."""
    print("\n🔍 Demo: Ricerca canzone specifica")
    print("=" * 50)
    
    # Cerca una canzone specifica
    title = "Smells Like Teen Spirit"
    artist = "Nirvana"
    
    print(f"🎯 Cercando '{title}' di {artist}...")
    
    song_data = await search_genius_song(
        title,
        artist,
        GENIUS_CONFIG['client_id'],
        GENIUS_CONFIG['client_secret'],
        GENIUS_CONFIG['access_token']
    )
    
    if song_data:
        print(f"✅ Trovata: {song_data['title']}")
        print(f"🎤 Artista: {song_data['artist']['name']}")
        print(f"👀 Visualizzazioni: {song_data['page_views']:,}")
        print(f"🔗 Testi: {song_data['lyrics_url']}")
        
        if song_data['album']:
            print(f"💿 Album: {song_data['album']['name']}")
        
        if song_data['featured_artists']:
            featured = [a['name'] for a in song_data['featured_artists']]
            print(f"🤝 Featuring: {', '.join(featured)}")
            
        return song_data
    else:
        print("❌ Canzone non trovata")
        return None


async def demo_integrated_crawling():
    """Dimostra il crawling integrato con Genius."""
    print("\n🔍 Demo: Crawling integrato con Genius")
    print("=" * 50)
    
    artist_name = "Nirvana"
    print(f"🎯 Crawling completo per: {artist_name}")
    print("📡 Fonti: MusicBrainz + Genius")
    
    # Crawling con integrazione Genius
    discography = await crawl_artist_discography(
        artist_name,
        use_genius_builtin=True,  # Usa le credenziali integrate
        include_lyrics_references=True  # Include riferimenti ai testi
    )
    
    print(f"\n✅ Crawling completato!")
    print(f"👤 Artista: {discography.artist.name}")
    print(f"📀 Album: {discography.total_albums}")
    print(f"🎵 Tracce: {discography.total_tracks}")
    print(f"🔗 Fonti: {', '.join(discography.sources)}")
    
    # Mostra metadati Genius se disponibili
    if hasattr(discography, 'metadata') and 'genius' in discography.metadata:
        genius_meta = discography.metadata['genius']
        print(f"\n🎵 Dati Genius:")
        print(f"   - Canzoni Genius: {genius_meta['total_songs_found']}")
        print(f"   - Follower: {genius_meta['followers_count']}")
        print(f"   - Verificato: {genius_meta['verified']}")
    
    # Mostra alcuni album con riferimenti ai testi
    print(f"\n📀 Album con riferimenti testi:")
    for album in discography.albums[:3]:  # Prime 3
        tracks_with_lyrics = [
            track for track in album.tracks 
            if hasattr(track, 'lyrics_reference')
        ]
        
        if tracks_with_lyrics:
            print(f"   📀 {album.title} ({album.release_year})")
            print(f"      🔗 {len(tracks_with_lyrics)}/{len(album.tracks)} tracce con riferimenti")
            
            # Mostra il primo riferimento come esempio
            if tracks_with_lyrics:
                track = tracks_with_lyrics[0]
                if hasattr(track, 'lyrics_reference'):
                    ref = track.lyrics_reference
                    print(f"      📝 Es: '{track.title}' → {ref['official_lyrics_url']}")
    
    return discography


async def demo_save_results():
    """Salva i risultati per analisi futura."""
    print("\n💾 Demo: Salvataggio risultati")
    print("=" * 50)
    
    # Crawling con tutti i dati
    discography = await crawl_artist_discography(
        "Radiohead",
        use_genius_builtin=True,
        include_lyrics_references=True
    )
    
    # Salva in formato JSON dettagliato
    output_file = Path("examples/output/radiohead_genius_demo.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(
            discography.dict(),
            f,
            indent=2,
            default=str,
            ensure_ascii=False
        )
    
    print(f"✅ Risultati salvati in: {output_file}")
    print(f"📊 Statistiche:")
    print(f"   - Album: {discography.total_albums}")
    print(f"   - Tracce: {discography.total_tracks}")
    print(f"   - Fonti: {', '.join(discography.sources)}")
    
    return output_file


async def main():
    """Esegue tutte le demo."""
    print("🎵 Demo Genius Integration")
    print("Progetto didattico - crawl-lyrics")
    print("=" * 50)
    
    try:
        # Demo 1: Ricerca diretta artista
        genius_artist = await demo_genius_search()
        
        # Demo 2: Ricerca canzone specifica
        genius_song = await demo_song_search()
        
        # Demo 3: Crawling integrato
        discography = await demo_integrated_crawling()
        
        # Demo 4: Salvataggio risultati
        saved_file = await demo_save_results()
        
        print(f"\n🎉 Tutte le demo completate!")
        print(f"\n💡 Per usare l'integrazione Genius:")
        print(f"   python main.py \"Nome Artista\" --include-lyrics-refs")
        print(f"   python main.py \"Nome Artista\" --no-genius-builtin --genius-token YOUR_TOKEN")
        
    except Exception as e:
        print(f"\n❌ Errore durante le demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
