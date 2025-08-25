"""
Esempio di utilizzo del Discography Crawler.
Dimostra come utilizzare il sistema per recuperare la discografia di un artista.
"""

import asyncio
import json
import logging
from pathlib import Path
import sys

# Aggiungi il path src per gli import
sys.path.append(str(Path(__file__).parent.parent / "src"))

from discography_crawler import DiscographyCrawler, crawl_artist_discography

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Esempio principale di utilizzo del crawler."""
    
    # Lista di artisti di esempio
    test_artists = [
        "Radiohead",
        "The Beatles", 
        "Pink Floyd",
        "Led Zeppelin"
    ]
    
    print("🎵 Discography Crawler - Esempio di Utilizzo")
    print("=" * 50)
    
    # Scegli un artista
    artist_name = input(f"Inserisci il nome di un artista (o premi Enter per '{test_artists[0]}'): ").strip()
    if not artist_name:
        artist_name = test_artists[0]
    
    print(f"\n🔍 Inizio crawling per: {artist_name}")
    print("-" * 30)
    
    try:
        # Metodo 1: Utilizzo della funzione di utilità
        print("Metodo 1: Funzione di utilità")
        discography = await crawl_artist_discography(artist_name)
        
        print(f"✅ Crawling completato!")
        print(f"📀 Album trovati: {discography.total_albums}")
        print(f"🎵 Tracce totali: {discography.total_tracks}")
        
        if discography.discography_span["start"]:
            span = discography.discography_span
            print(f"📅 Periodo: {span['start']} - {span['end']}")
        
        print(f"🔗 Fonti: {', '.join(discography.sources)}")
        
        # Mostra alcuni album
        print(f"\n📋 Prime 5 album:")
        for i, album in enumerate(discography.albums[:5]):
            year = f" ({album.release_year})" if album.release_year else ""
            print(f"  {i+1}. {album.title}{year} - {len(album.tracks)} tracce")
        
        # Salva il risultato
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        filename = f"{artist_name.replace(' ', '_').lower()}_discography.json"
        output_path = output_dir / filename
        
        discography.save_to_file(str(output_path))
        print(f"\n💾 Discografia salvata in: {output_path}")
        
        # Mostra un esempio di tracce di un album
        if discography.albums and discography.albums[0].tracks:
            first_album = discography.albums[0]
            print(f"\n🎼 Tracce di '{first_album.title}':")
            for track in first_album.tracks[:5]:  # Prime 5 tracce
                duration = ""
                if track.duration_ms:
                    minutes = track.duration_ms // 60000
                    seconds = (track.duration_ms % 60000) // 1000
                    duration = f" ({minutes}:{seconds:02d})"
                print(f"  {track.track_number}. {track.title}{duration}")
        
        # Metodo 2: Utilizzo avanzato con crawler personalizzato
        print(f"\n" + "=" * 50)
        print("Metodo 2: Crawler avanzato con statistiche")
        
        async with DiscographyCrawler() as crawler:
            # Cerca possibili varianti dell'artista
            search_results = await crawler.search_artists(artist_name, limit=3)
            
            if len(search_results) > 1:
                print(f"\n🔍 Trovati {len(search_results)} artisti simili:")
                for i, artist in enumerate(search_results):
                    disambiguation = f" ({artist.disambiguation})" if artist.disambiguation else ""
                    print(f"  {i+1}. {artist.name}{disambiguation}")
            
            # Mostra statistiche del crawling
            status = await crawler.get_crawl_status()
            if status:
                print(f"\n📊 Statistiche crawling:")
                print(f"  ⏱️  Durata: {status.duration_seconds:.2f}s" if status.duration_seconds else "  ⏱️  Durata: N/A")
                print(f"  📀 Album trovati: {status.albums_found}")
                print(f"  🎵 Tracce trovate: {status.tracks_found}")
                print(f"  ✅ Stato: {status.status}")
                
                if status.errors:
                    print(f"  ⚠️  Errori: {len(status.errors)}")
        
        # Analisi della discografia
        print(f"\n" + "=" * 50)
        print("📈 Analisi della Discografia")
        
        albums_by_year = discography.get_albums_by_year()
        albums_by_type = discography.get_albums_by_type()
        
        print(f"\n📅 Album per anno:")
        for year in sorted(albums_by_year.keys()):
            albums = albums_by_year[year]
            print(f"  {year}: {len(albums)} album")
        
        print(f"\n📁 Album per tipo:")
        for album_type, albums in albums_by_type.items():
            print(f"  {album_type.title()}: {len(albums)} album")
        
        print(f"\n🎉 Esempio completato con successo!")
        
    except Exception as e:
        logger.error(f"Errore durante l'esempio: {e}")
        print(f"\n❌ Errore: {e}")
        print("\n💡 Suggerimenti:")
        print("  - Verifica la connessione internet")
        print("  - Prova con un nome artista più specifico")
        print("  - Controlla i log per dettagli")


async def example_json_output():
    """Esempio che mostra la struttura JSON di output."""
    print("\n" + "=" * 50)
    print("📄 Esempio di Output JSON")
    print("=" * 50)
    
    try:
        # Crawling rapido
        discography = await crawl_artist_discography("Nirvana")
        
        # Mostra JSON formattato (solo primi 2 album per brevità)
        limited_discography = discography.copy(deep=True)
        limited_discography.albums = limited_discography.albums[:2]
        
        # Limita anche le tracce per ogni album
        for album in limited_discography.albums:
            album.tracks = album.tracks[:3]
        
        json_output = limited_discography.to_json(indent=2)
        print(json_output)
        
    except Exception as e:
        print(f"Errore nell'esempio JSON: {e}")


if __name__ == "__main__":
    # Esegui l'esempio principale
    asyncio.run(main())
    
    # Esempio aggiuntivo per il JSON (opzionale)
    show_json = input("\n🤔 Vuoi vedere un esempio di output JSON? (s/n): ").lower().strip()
    if show_json in ['s', 'si', 'y', 'yes']:
        asyncio.run(example_json_output())
