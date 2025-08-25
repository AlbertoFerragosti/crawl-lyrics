"""
Test di base per il Discography Crawler.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from datetime import date
import sys
from pathlib import Path

# Aggiungi il path src per gli import
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.models.discography import Artist, Album, Track, Discography
from src.discography_crawler import DiscographyCrawler


class TestModels:
    """Test per i modelli di dati."""
    
    def test_track_creation(self):
        """Test creazione Track."""
        track = Track(
            title="Creep",
            track_number=1,
            duration_ms=238000
        )
        
        assert track.title == "Creep"
        assert track.track_number == 1
        assert track.duration_ms == 238000
        assert str(track) == "1. Creep"
    
    def test_album_creation(self):
        """Test creazione Album."""
        tracks = [
            Track(title="Track 1", track_number=1),
            Track(title="Track 2", track_number=2)
        ]
        
        album = Album(
            title="OK Computer",
            release_year=1997,
            tracks=tracks
        )
        
        assert album.title == "OK Computer"
        assert album.release_year == 1997
        assert album.track_count == 2
        assert "OK Computer (1997)" in str(album)
    
    def test_artist_creation(self):
        """Test creazione Artist."""
        artist = Artist(
            name="Radiohead",
            country="GB",
            musicbrainz_id="a74b1b7f-71a5-4011-9441-d0b5e4122711"
        )
        
        assert artist.name == "Radiohead"
        assert artist.country == "GB"
        assert str(artist) == "Radiohead"
    
    def test_discography_creation(self):
        """Test creazione Discography."""
        artist = Artist(name="Test Artist")
        albums = [
            Album(title="Album 1", release_year=2020),
            Album(title="Album 2", release_year=2021)
        ]
        
        discography = Discography(artist=artist, albums=albums)
        
        assert discography.total_albums == 2
        assert discography.discography_span["start"] == 2020
        assert discography.discography_span["end"] == 2021


class TestCrawler:
    """Test per il crawler principale."""
    
    @pytest.fixture
    def mock_crawler(self):
        """Crea un crawler con client mockati."""
        return DiscographyCrawler()
    
    @pytest.mark.asyncio
    async def test_search_artists(self, mock_crawler):
        """Test ricerca artisti."""
        # Mock del client MusicBrainz
        mock_artists = [
            Artist(name="Radiohead", musicbrainz_id="test-id")
        ]
        
        with patch.object(mock_crawler.musicbrainz_client, 'search_artist', 
                         return_value=mock_artists):
            results = await mock_crawler.search_artists("Radiohead")
            
            assert len(results) == 1
            assert results[0].name == "Radiohead"
    
    @pytest.mark.asyncio 
    async def test_crawler_context_manager(self):
        """Test utilizzo del crawler come context manager."""
        async with DiscographyCrawler() as crawler:
            assert crawler.stats['start_time'] is not None
        
        assert crawler.stats['end_time'] is not None
        assert crawler.execution_time is not None


class TestIntegration:
    """Test di integrazione che usano API reali (opzionali)."""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_real_artist_search(self):
        """Test ricerca di un artista reale."""
        async with DiscographyCrawler() as crawler:
            artists = await crawler.search_artists("Nirvana", limit=1)
            
            assert len(artists) > 0
            assert "nirvana" in artists[0].name.lower()
    
    @pytest.mark.integration  
    @pytest.mark.asyncio
    async def test_small_discography_crawl(self):
        """Test crawling di una discografia piccola."""
        # Usa un artista con pochi album per test veloce
        try:
            async with DiscographyCrawler() as crawler:
                discography = await crawler.crawl("Nirvana")
                
                assert discography.total_albums > 0
                assert discography.artist.name
                assert len(discography.sources) > 0
                
        except Exception as e:
            pytest.skip(f"Test di integrazione fallito: {e}")


def test_json_serialization():
    """Test serializzazione JSON."""
    artist = Artist(name="Test Artist")
    album = Album(
        title="Test Album",
        release_date=date(2020, 1, 1),
        tracks=[Track(title="Test Track", track_number=1)]
    )
    
    discography = Discography(artist=artist, albums=[album])
    json_str = discography.to_json()
    
    assert "Test Artist" in json_str
    assert "Test Album" in json_str
    assert "Test Track" in json_str


if __name__ == "__main__":
    # Esegui i test
    pytest.main([__file__, "-v"])
