"""
Script principale per l'esecuzione del crawler dalla command line.
Fornisce un'interfaccia CLI user-friendly.
"""

import asyncio
import argparse
import logging
import json
import sys
from pathlib import Path
from typing import Optional
import os

# Aggiungi il path src per gli import
sys.path.append(str(Path(__file__).parent / "src"))

from src.discography_crawler import DiscographyCrawler, crawl_artist_discography

def setup_logging(log_level: str = "INFO"):
    """Configura il sistema di logging."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('crawler.log')
        ]
    )

def load_env():
    """Carica le variabili di ambiente dal file .env se presente."""
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

async def main():
    """Funzione principale CLI."""
    parser = argparse.ArgumentParser(
        description="🎵 Discography Crawler - Recupera la discografia completa di un artista",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di utilizzo:
  python main.py "Radiohead"
  python main.py "Pink Floyd" --output pink_floyd.json
  python main.py "The Beatles" --lastfm-key YOUR_API_KEY --verbose
  python main.py --search "Led Zeppelin"
        """
    )
    
    parser.add_argument(
        'artist',
        nargs='?',
        help='Nome dell\'artista di cui recuperare la discografia'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='File di output per salvare la discografia (default: ARTIST_discography.json)'
    )
    
    parser.add_argument(
        '--lastfm-key',
        help='Chiave API Last.fm per arricchire i dati'
    )
    
    parser.add_argument(
        '--genius-token',
        help='Token API Genius personalizzato per riferimenti ETICI ai testi (NO testi completi)'
    )
    
    parser.add_argument(
        '--no-genius-builtin',
        action='store_true',
        help='Disabilita l\'uso delle credenziali Genius integrate'
    )
    
    parser.add_argument(
        '--include-lyrics-refs',
        action='store_true',
        help='Include riferimenti etici ai testi (richiede accesso a Genius)'
    )
    
    parser.add_argument(
        '--search', '-s',
        help='Cerca artisti che corrispondono al nome fornito'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Numero massimo di risultati di ricerca (default: 10)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Output dettagliato'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Output minimale'
    )
    
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Output JSON formattato leggibile'
    )
    
    args = parser.parse_args()
    
    # Carica variabili di ambiente
    load_env()
    
    # Configura logging
    if args.quiet:
        log_level = "ERROR"
    elif args.verbose:
        log_level = "DEBUG"
    else:
        log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    setup_logging(log_level)
    logger = logging.getLogger(__name__)
    
    # API Key Last.fm e Genius
    lastfm_key = args.lastfm_key or os.getenv('LASTFM_API_KEY')
    genius_token = args.genius_token or os.getenv('GENIUS_TOKEN')
    use_genius_builtin = not args.no_genius_builtin
    
    # Determina se Genius è disponibile
    has_genius = use_genius_builtin or genius_token is not None
    
    # Warning se lyrics sono richieste ma token non disponibile
    if args.include_lyrics_refs and not has_genius:
        print("⚠️  Riferimenti testi richiesti ma accesso Genius non disponibile")
        print("   Opzioni:")
        print("   - Usa --genius-token TOKEN o imposta GENIUS_TOKEN in .env")
        print("   - Assicurati che le credenziali integrate siano abilitate (default)")
        return
    
    try:
        # Modalità ricerca
        if args.search:
            print(f"🔍 Ricerca artisti per: {args.search}")
            async with DiscographyCrawler(
                lastfm_api_key=lastfm_key, 
                genius_token=genius_token,
                use_genius_builtin=use_genius_builtin
            ) as crawler:
                artists = await crawler.search_artists(args.search, args.limit)
                
                if not artists:
                    print("❌ Nessun artista trovato")
                    return
                
                print(f"\n✅ Trovati {len(artists)} artisti:")
                for i, artist in enumerate(artists, 1):
                    disambiguation = f" ({artist.disambiguation})" if artist.disambiguation else ""
                    country = f" [{artist.country}]" if artist.country else ""
                    print(f"  {i}. {artist.name}{disambiguation}{country}")
                    if artist.musicbrainz_id:
                        print(f"     ID: {artist.musicbrainz_id}")
                    
            return
        
        # Modalità crawling
        if not args.artist:
            parser.print_help()
            return
        
        if not args.quiet:
            print(f"🎵 Discography Crawler")
            print(f"🎯 Artista: {args.artist}")
            
            # Info sulle fonti
            sources = ["MusicBrainz"]
            if lastfm_key:
                sources.append("Last.fm")
            if has_genius:
                sources.append("Genius")
            print(f"📡 Fonti attive: {', '.join(sources)}")
            
            if args.include_lyrics_refs and has_genius:
                print(f"🔗 Riferimenti testi: ABILITATI (solo metadati etici)")
            print("-" * 50)
        
        # Esegui il crawling
        discography = await crawl_artist_discography(
            args.artist, 
            lastfm_key, 
            genius_token,
            use_genius_builtin,
            args.include_lyrics_refs
        )
        
        if not args.quiet:
            print(f"✅ Crawling completato!")
            print(f"👤 Artista: {discography.artist.name}")
            print(f"📀 Album: {discography.total_albums}")
            print(f"🎵 Tracce: {discography.total_tracks}")
            
            if discography.discography_span["start"]:
                span = discography.discography_span
                print(f"📅 Periodo: {span['start']}-{span['end']}")
            
            print(f"🔗 Fonti: {', '.join(discography.sources)}")
        
        # Determina il file di output
        if args.output:
            output_file = Path(args.output)
        else:
            safe_name = args.artist.replace(' ', '_').replace('/', '_').lower()
            output_file = Path(f"{safe_name}_discography.json")
        
        # Crea directory se necessaria
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Salva il file
        if args.pretty:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(
                    discography.dict(),
                    f,
                    indent=2,
                    default=str,
                    ensure_ascii=False
                )
        else:
            discography.save_to_file(str(output_file))
        
        if not args.quiet:
            print(f"💾 Salvato in: {output_file.absolute()}")
            
            # Mostra preview degli album
            print(f"\n📋 Album trovati:")
            for i, album in enumerate(discography.albums[:10], 1):  # Prime 10
                year = f" ({album.release_year})" if album.release_year else ""
                tracks_count = f" - {len(album.tracks)} tracce" if album.tracks else ""
                print(f"  {i:2d}. {album.title}{year}{tracks_count}")
            
            if len(discography.albums) > 10:
                print(f"     ... e altri {len(discography.albums) - 10} album")
        
        logger.info(f"Crawling completato per {args.artist}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Crawling interrotto dall'utente")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Errore durante il crawling: {e}")
        if not args.quiet:
            print(f"\n❌ Errore: {e}")
            print("\n💡 Suggerimenti:")
            print("  - Verifica la connessione internet")
            print("  - Prova con un nome artista più specifico")
            print("  - Usa --verbose per maggiori dettagli")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Arrivederci!")
        sys.exit(0)
