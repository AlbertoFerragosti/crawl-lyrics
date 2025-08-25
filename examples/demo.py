"""
Demo per mostrare la struttura completa del sistema.
Crea dati di esempio per dimostrare il formato di output.
"""

import asyncio
import json
from datetime import date, datetime
from pathlib import Path
import sys

# Aggiungi il path src per gli import
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.discography import Artist, Album, Track, Discography


def create_demo_discography() -> Discography:
    """Crea una discografia di esempio per dimostrare la struttura dei dati."""
    
    # Artista di esempio
    artist = Artist(
        name="Demo Band",
        sort_name="Demo Band, The",
        country="IT",
        musicbrainz_id="demo-123-456",
        begin_date=date(1990, 1, 1),
        artist_type="Group"
    )
    
    # Album 1
    album1_tracks = [
        Track(
            title="Intro",
            track_number=1,
            duration_ms=45000  # 45 secondi
        ),
        Track(
            title="Prima Canzone",
            track_number=2,
            duration_ms=240000,  # 4 minuti
            explicit=False
        ),
        Track(
            title="Ballata Romantica",
            track_number=3,
            duration_ms=300000,  # 5 minuti
            explicit=False
        ),
        Track(
            title="Rock Pesante",
            track_number=4,
            duration_ms=180000,  # 3 minuti
            explicit=True
        )
    ]
    
    album1 = Album(
        title="Primo Album",
        release_date=date(1995, 6, 15),
        album_type="album",
        label="Demo Records",
        tracks=album1_tracks,
        genre=["Rock", "Alternative", "Italian"],
        country="IT"
    )
    
    # Album 2
    album2_tracks = [
        Track(title="Singolo Hit", track_number=1, duration_ms=210000),
        Track(title="B-Side", track_number=2, duration_ms=195000)
    ]
    
    album2 = Album(
        title="Singolo Famoso",
        release_date=date(1997, 3, 10),
        album_type="single",
        label="Demo Records",
        tracks=album2_tracks,
        genre=["Pop Rock", "Italian"]
    )
    
    # Album 3 - EP
    album3_tracks = [
        Track(title="Acustica 1", track_number=1, duration_ms=280000),
        Track(title="Acustica 2", track_number=2, duration_ms=320000),
        Track(title="Acustica 3", track_number=3, duration_ms=260000),
        Track(title="Remix Elettronico", track_number=4, duration_ms=340000)
    ]
    
    album3 = Album(
        title="Sessions Acustiche",
        release_date=date(1999, 11, 5),
        album_type="ep",
        label="Indie Label",
        tracks=album3_tracks,
        genre=["Acoustic", "Alternative", "Electronic"]
    )
    
    # Album 4 - Album principale
    album4_tracks = [
        Track(title="Apertura", track_number=1, duration_ms=60000),
        Track(title="Evoluzione", track_number=2, duration_ms=275000),
        Track(title="Riflessioni", track_number=3, duration_ms=310000),
        Track(title="Energia", track_number=4, duration_ms=220000),
        Track(title="Intermezzo", track_number=5, duration_ms=150000),
        Track(title="Rinascita", track_number=6, duration_ms=290000),
        Track(title="Viaggio", track_number=7, duration_ms=380000),
        Track(title="Finale", track_number=8, duration_ms=420000)
    ]
    
    album4 = Album(
        title="Capolavoro",
        release_date=date(2001, 9, 21),
        album_type="album",
        label="Major Label",
        tracks=album4_tracks,
        genre=["Progressive Rock", "Art Rock", "Italian"],
        country="IT"
    )
    
    # Discografia completa
    discography = Discography(
        artist=artist,
        albums=[album1, album2, album3, album4],
        sources=["Demo Data", "Manual Creation"]
    )
    
    return discography


def print_discography_summary(discography: Discography):
    """Stampa un riassunto della discografia."""
    
    print("🎵 DEMO DISCOGRAPHY CRAWLER - STRUTTURA DATI")
    print("=" * 60)
    
    print(f"👤 Artista: {discography.artist.name}")
    print(f"🌍 Paese: {discography.artist.country}")
    print(f"📅 Periodo attività: {discography.artist.begin_date}")
    print(f"🆔 MusicBrainz ID: {discography.artist.musicbrainz_id}")
    
    print(f"\n📊 STATISTICHE DISCOGRAFIA")
    print(f"📀 Album totali: {discography.total_albums}")
    print(f"🎵 Tracce totali: {discography.total_tracks}")
    
    span = discography.discography_span
    if span["start"]:
        print(f"📅 Periodo discografia: {span['start']}-{span['end']}")
    
    print(f"🔗 Fonti: {', '.join(discography.sources)}")
    
    # Album per tipo
    by_type = discography.get_albums_by_type()
    print(f"\n📁 ALBUM PER TIPO:")
    for album_type, albums in by_type.items():
        print(f"  • {album_type.title()}: {len(albums)} album")
    
    # Album per anno
    by_year = discography.get_albums_by_year()
    print(f"\n📅 ALBUM PER ANNO:")
    for year in sorted(by_year.keys()):
        albums = by_year[year]
        print(f"  • {year}: {len(albums)} album")
    
    print(f"\n📋 DETTAGLIO ALBUM:")
    for i, album in enumerate(discography.albums, 1):
        duration_min = album.total_duration_ms // 60000 if album.total_duration_ms else 0
        genre_str = ", ".join(album.genre[:3]) if album.genre else "N/A"
        
        print(f"  {i}. {album.title} ({album.release_year})")
        print(f"     Tipo: {album.album_type} | Tracce: {album.track_count} | "
              f"Durata: ~{duration_min} min")
        print(f"     Generi: {genre_str}")
        print(f"     Label: {album.label}")
        
        # Mostra alcune tracce
        print(f"     Tracce:")
        for track in album.tracks[:3]:  # Prime 3 tracce
            duration_sec = track.duration_ms // 1000 if track.duration_ms else 0
            minutes = duration_sec // 60
            seconds = duration_sec % 60
            explicit_mark = " 🔞" if track.explicit else ""
            print(f"       {track.track_number}. {track.title} ({minutes}:{seconds:02d}){explicit_mark}")
        
        if len(album.tracks) > 3:
            print(f"       ... e altre {len(album.tracks) - 3} tracce")
        print()


def main():
    """Funzione principale del demo."""
    
    # Crea discografia di esempio
    demo_discography = create_demo_discography()
    
    # Stampa riassunto
    print_discography_summary(demo_discography)
    
    # Salva in JSON
    output_dir = Path("examples/output")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    json_file = output_dir / "demo_discography.json"
    demo_discography.save_to_file(str(json_file))
    
    print(f"💾 Demo salvato in: {json_file.absolute()}")
    
    # Mostra JSON formattato
    print(f"\n📄 ESEMPIO OUTPUT JSON (limitato):")
    print("-" * 50)
    
    # Crea versione limitata per esempio
    limited_disco = demo_discography.copy(deep=True)
    limited_disco.albums = limited_disco.albums[:2]  # Solo primi 2 album
    
    # Limita le tracce per ogni album
    for album in limited_disco.albums:
        album.tracks = album.tracks[:2]  # Solo prime 2 tracce
    
    print(limited_disco.to_json(indent=2))
    
    print(f"\n✅ Demo completato!")
    print(f"📝 Il file completo è disponibile in: {json_file}")
    
    print(f"\n🚀 PROSSIMI PASSI:")
    print(f"  1. Ottieni una API key di Last.fm (gratuita) per dati arricchiti")
    print(f"  2. Usa: python main.py \"Nome Artista\" --lastfm-key TUA_CHIAVE")
    print(f"  3. Il sistema rispetta i copyright - NON estrae testi completi")
    print(f"  4. Perfetto per metadati, statistiche e analisi musicali")


if __name__ == "__main__":
    main()
