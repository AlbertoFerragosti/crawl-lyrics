"""
Esempio di utilizzo ETICO dei riferimenti ai testi.
Dimostra come ottenere metadati legali senza violare copyright.
"""

import asyncio
import json
import logging
from pathlib import Path
import sys

# Aggiungi il path src per gli import
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.discography_crawler import crawl_artist_discography
from src.services.lyrics_metadata_client import LYRICS_DISCLAIMER

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def demo_ethical_lyrics_references():
    """
    Demo dell'integrazione ETICA dei riferimenti ai testi.
    
    IMPORTANTE: Questo demo mostra come ottenere RIFERIMENTI ai testi
    senza violare copyright. NON estrae testi completi.
    """
    
    print("🚨 DISCLAIMER IMPORTANTE 🚨")
    print(LYRICS_DISCLAIMER)
    print("\n" + "="*60)
    
    # Simula token (in realtà useresti il tuo token vero)
    fake_genius_token = "demo_token_placeholder"
    
    # Per la demo, usiamo solo MusicBrainz (funziona senza token)
    artist_name = "Nirvana"
    
    print(f"🎵 Demo Riferimenti Etici ai Testi")
    print(f"🎯 Artista: {artist_name}")
    print(f"⚠️  NOTA: Demo senza token reale - struttura dati di esempio")
    print("-" * 50)
    
    try:
        # Crawling base senza lyrics (sempre funzionante)
        print("📀 Fase 1: Crawling discografia base...")
        discography = await crawl_artist_discography(
            artist_name,
            include_lyrics_references=False  # Disabilitato per demo
        )
        
        print(f"✅ Trovati {discography.total_albums} album")
        print(f"🎵 Trovate {discography.total_tracks} tracce")
        
        # Mostra come sarebbe la struttura CON riferimenti testi
        print(f"\n📋 Esempio struttura CON riferimenti etici:")
        
        if discography.albums and discography.albums[0].tracks:
            first_track = discography.albums[0].tracks[0]
            
            # Esempio di come apparirebbe un riferimento etico
            example_lyrics_reference = {
                "title": first_track.title,
                "artist": discography.artist.name,
                "lyrics_available": True,
                "official_lyrics_url": f"https://genius.com/songs/{first_track.title.lower().replace(' ', '-')}",
                "how_to_access": "Visita il link ufficiale per i testi completi",
                "legal_notice": "I testi sono protetti da copyright. Questo sistema fornisce solo link di riferimento.",
                "identification_help": f"Canzone: {first_track.title}",
                "disclaimer": "Per uso educativo e di ricerca. Rispetta sempre i diritti d'autore."
            }
            
            print(json.dumps(example_lyrics_reference, indent=2, ensure_ascii=False))
        
        print(f"\n📊 Come funzionerebbe con token Genius REALE:")
        print(f"  1. ✅ Cerca metadati canzone su Genius")
        print(f"  2. ✅ Estrae SOLO link ufficiale ai testi")
        print(f"  3. ✅ Aggiunge snippet minimo per identificazione (Fair Use)")
        print(f"  4. ❌ NON estrae mai testi completi")
        print(f"  5. ✅ Include disclaimer copyright rigorosi")
        
        print(f"\n🔗 Per abilitare riferimenti testi:")
        print(f"  1. Ottieni token gratuito da https://genius.com/api-clients")
        print(f"  2. Usa: python main.py \"{artist_name}\" --genius-token TOKEN --include-lyrics-refs")
        print(f"  3. Il sistema aggiungerà SOLO riferimenti legali")
        
        # Salva esempio
        output_dir = Path("examples/output")
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Aggiungi esempio di riferimento alla prima traccia per demo
        if discography.albums and discography.albums[0].tracks:
            demo_track = discography.albums[0].tracks[0]
            demo_track.lyrics_reference = example_lyrics_reference
            demo_track.genius_url = example_lyrics_reference["official_lyrics_url"]
        
        example_file = output_dir / "ethical_lyrics_demo.json"
        discography.save_to_file(str(example_file))
        
        print(f"\n💾 Esempio salvato in: {example_file}")
        
        print(f"\n✅ Demo completato!")
        print(f"🎯 Ricorda: Il sistema rispetta SEMPRE il copyright")
        print(f"📚 Solo riferimenti legali, mai contenuto protetto")
        
    except Exception as e:
        logger.error(f"Errore durante la demo: {e}")
        print(f"\n❌ Errore: {e}")


async def show_legal_compliance():
    """Mostra come il sistema rispetta le leggi sul copyright."""
    
    print("\n" + "="*60)
    print("⚖️  COMPLIANCE LEGALE - COME RISPETTIAMO IL COPYRIGHT")
    print("="*60)
    
    compliance_info = {
        "✅ COSA FACCIAMO": [
            "Forniamo SOLO link ufficiali ai testi",
            "Estraiamo metadati pubblici (titolo, artista, anno)",
            "Includiamo snippet minimi per identificazione (Fair Use)",
            "Aggiungiamo disclaimer copyright completi",
            "Rate limiting per rispettare i termini API",
            "Uso solo per scopi educativi/ricerca"
        ],
        "❌ COSA NON FACCIAMO MAI": [
            "Non estraiamo testi completi delle canzoni",
            "Non memorizziamo contenuto protetto da copyright",
            "Non redistribuiamo materiale sotto copyright",
            "Non aggiriamo sistemi di protezione",
            "Non violiamo termini di servizio",
            "Non facilitiamo uso commerciale non autorizzato"
        ],
        "🛡️ PROTEZIONI IMPLEMENTATE": [
            "Client che estrae SOLO metadati pubblici",
            "Limiti automatici su lunghezza snippet",
            "Disclaimer legali in ogni risposta",
            "Rate limiting etico per rispettare API",
            "Documentazione chiara sui limiti legali",
            "Focus su link ufficiali vs contenuto diretto"
        ]
    }
    
    for section, items in compliance_info.items():
        print(f"\n{section}:")
        for item in items:
            print(f"  • {item}")
    
    print(f"\n📖 FONTI LEGALI UTILIZZATE:")
    print(f"  • MusicBrainz: Database open source")
    print(f"  • Last.fm: API pubblica con termini chiari")
    print(f"  • Genius: API ufficiale per metadati (NO testi)")
    
    print(f"\n⚖️  BASE LEGALE:")
    print(f"  • Fair Use: Solo identificazione e ricerca")
    print(f"  • Linking: Collegamenti a contenuto originale")
    print(f"  • Metadata: Informazioni pubbliche non protette")
    print(f"  • Educational: Scopo educativo e di ricerca")


if __name__ == "__main__":
    print("🎵 DEMO ETICO - RIFERIMENTI AI TESTI")
    print("RISPETTO RIGOROSO DEL COPYRIGHT")
    print("="*50)
    
    asyncio.run(demo_ethical_lyrics_references())
    asyncio.run(show_legal_compliance())
    
    print(f"\n👋 Demo completato!")
    print(f"📚 Il sistema è progettato per rispettare sempre il copyright")
    print(f"🎯 Per testi completi, usa sempre i link ufficiali forniti")
