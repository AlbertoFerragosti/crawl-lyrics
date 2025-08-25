"""
Test per l'integrazione con Genius API.
"""

import asyncio
import pytest
import sys
from pathlib import Path

# Aggiungi il path src per gli import
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.services.genius_client import GeniusClient, GENIUS_CONFIG, search_genius_artist, search_genius_song


class TestGeniusIntegration:
    """Test per l'integrazione Genius."""
    
    @pytest.mark.asyncio
    async def test_genius_config(self):
        """Test configurazione Genius."""
        assert 'client_id' in GENIUS_CONFIG
        assert 'client_secret' in GENIUS_CONFIG
        assert 'access_token' in GENIUS_CONFIG
        assert GENIUS_CONFIG['client_id'].startswith('zPwicLU4')
    
    @pytest.mark.asyncio
    async def test_genius_client_creation(self):
        """Test creazione client Genius."""
        async with GeniusClient(
            GENIUS_CONFIG['client_id'],
            GENIUS_CONFIG['client_secret'],
            GENIUS_CONFIG['access_token']
        ) as client:
            assert client is not None
            assert client.session is not None
    
    @pytest.mark.asyncio
    async def test_search_artist(self):
        """Test ricerca artista su Genius."""
        artist_data = await search_genius_artist(
            "Nirvana",
            GENIUS_CONFIG['client_id'],
            GENIUS_CONFIG['client_secret'],
            GENIUS_CONFIG['access_token']
        )
        
        if artist_data:  # Se l'API è disponibile
            assert 'name' in artist_data
            assert 'genius_id' in artist_data
            assert 'url' in artist_data
            assert 'songs' in artist_data
            assert isinstance(artist_data['songs'], list)
        else:
            pytest.skip("Genius API non disponibile o rate limited")
    
    @pytest.mark.asyncio
    async def test_search_song(self):
        """Test ricerca canzone su Genius."""
        song_data = await search_genius_song(
            "Smells Like Teen Spirit",
            "Nirvana",
            GENIUS_CONFIG['client_id'],
            GENIUS_CONFIG['client_secret'],
            GENIUS_CONFIG['access_token']
        )
        
        if song_data:  # Se l'API è disponibile
            assert 'title' in song_data
            assert 'artist' in song_data
            assert 'lyrics_url' in song_data
            assert 'copyright_notice' in song_data
        else:
            pytest.skip("Genius API non disponibile o rate limited")
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """Test rate limiting."""
        async with GeniusClient(
            GENIUS_CONFIG['client_id'],
            GENIUS_CONFIG['client_secret'],
            GENIUS_CONFIG['access_token']
        ) as client:
            
            # Test che il rate limiting funzioni
            import time
            start_time = time.time()
            
            # Fai due richieste consecutive
            await client.search_artist("Test Artist 1")
            await client.search_artist("Test Artist 2")
            
            elapsed = time.time() - start_time
            # Dovrebbe essere almeno 0.5 secondi (rate limit interval)
            assert elapsed >= 0.4  # Piccolo margine per timing


async def test_manual_genius_search():
    """Test manuale per verificare che l'integrazione funzioni."""
    print("🔍 Test manuale Genius...")
    
    try:
        # Test ricerca artista
        artist_data = await search_genius_artist(
            "Radiohead",
            GENIUS_CONFIG['client_id'],
            GENIUS_CONFIG['client_secret'],
            GENIUS_CONFIG['access_token']
        )
        
        if artist_data:
            print(f"✅ Artista trovato: {artist_data['name']}")
            print(f"   Canzoni: {artist_data['total_songs_found']}")
            print(f"   URL: {artist_data['url']}")
            
            # Test ricerca canzone
            song_data = await search_genius_song(
                "Creep",
                "Radiohead",
                GENIUS_CONFIG['client_id'],
                GENIUS_CONFIG['client_secret'],
                GENIUS_CONFIG['access_token']
            )
            
            if song_data:
                print(f"✅ Canzone trovata: {song_data['title']}")
                print(f"   Artista: {song_data['artist']['name']}")
                print(f"   Link testi: {song_data['lyrics_url']}")
                print(f"   Visualizzazioni: {song_data['page_views']:,}")
            else:
                print("❌ Canzone non trovata")
        else:
            print("❌ Artista non trovato")
            
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Esegui test manuale
    asyncio.run(test_manual_genius_search())
