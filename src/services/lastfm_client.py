"""
Client per l'API Last.fm.
Fornisce informazioni aggiuntive su artisti e album.
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any
import aiohttp
from urllib.parse import urlencode

# Configurazione logging
logger = logging.getLogger(__name__)


class LastFmClient:
    """Client per interagire con l'API Last.fm."""
    
    BASE_URL = "http://ws.audioscrobbler.com/2.0/"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inizializza il client Last.fm.
        
        Args:
            api_key: Chiave API Last.fm (opzionale, usa quella di default per test)
        """
        # Chiave API pubblica di test (sostituire con la propria in produzione)
        self.api_key = api_key or "demo_api_key"
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'DiscographyCrawler/1.0'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.session:
            await self.session.close()
    
    async def search_artist(self, artist_name: str) -> List[Dict[str, Any]]:
        """
        Cerca un artista su Last.fm.
        
        Args:
            artist_name: Nome dell'artista da cercare
            
        Returns:
            Lista di artisti trovati
        """
        if not self.session:
            logger.error("Sessione non inizializzata")
            return []
        
        params = {
            'method': 'artist.search',
            'artist': artist_name,
            'api_key': self.api_key,
            'format': 'json',
            'limit': 10
        }
        
        try:
            url = f"{self.BASE_URL}?{urlencode(params)}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    artists = data.get('results', {}).get('artistmatches', {}).get('artist', [])
                    
                    # Last.fm può restituire un dict per un singolo risultato
                    if isinstance(artists, dict):
                        artists = [artists]
                    
                    logger.info(f"Trovati {len(artists)} artisti su Last.fm per '{artist_name}'")
                    return artists
                else:
                    logger.warning(f"Last.fm API error: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Errore nella ricerca artista su Last.fm: {e}")
            return []
    
    async def get_artist_info(self, artist_name: str) -> Optional[Dict[str, Any]]:
        """
        Recupera informazioni dettagliate su un artista.
        
        Args:
            artist_name: Nome dell'artista
            
        Returns:
            Informazioni sull'artista o None
        """
        if not self.session:
            return None
        
        params = {
            'method': 'artist.getinfo',
            'artist': artist_name,
            'api_key': self.api_key,
            'format': 'json'
        }
        
        try:
            url = f"{self.BASE_URL}?{urlencode(params)}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('artist')
                else:
                    logger.warning(f"Last.fm getinfo error: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Errore nel recupero info artista da Last.fm: {e}")
            return None
    
    async def get_artist_albums(self, artist_name: str) -> List[Dict[str, Any]]:
        """
        Recupera la lista degli album di un artista.
        
        Args:
            artist_name: Nome dell'artista
            
        Returns:
            Lista degli album
        """
        if not self.session:
            return []
        
        params = {
            'method': 'artist.gettopalbums',
            'artist': artist_name,
            'api_key': self.api_key,
            'format': 'json',
            'limit': 50
        }
        
        try:
            url = f"{self.BASE_URL}?{urlencode(params)}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    albums = data.get('topalbums', {}).get('album', [])
                    
                    # Last.fm può restituire un dict per un singolo risultato
                    if isinstance(albums, dict):
                        albums = [albums]
                    
                    logger.info(f"Trovati {len(albums)} album su Last.fm per '{artist_name}'")
                    return albums
                else:
                    logger.warning(f"Last.fm gettopalbums error: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Errore nel recupero album da Last.fm: {e}")
            return []
    
    async def get_album_info(self, artist_name: str, album_name: str) -> Optional[Dict[str, Any]]:
        """
        Recupera informazioni dettagliate su un album.
        
        Args:
            artist_name: Nome dell'artista
            album_name: Nome dell'album
            
        Returns:
            Informazioni sull'album o None
        """
        if not self.session:
            return None
        
        params = {
            'method': 'album.getinfo',
            'artist': artist_name,
            'album': album_name,
            'api_key': self.api_key,
            'format': 'json'
        }
        
        try:
            url = f"{self.BASE_URL}?{urlencode(params)}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('album')
                else:
                    logger.warning(f"Last.fm album getinfo error: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Errore nel recupero info album da Last.fm: {e}")
            return None
    
    async def get_album_tracks(self, artist_name: str, album_name: str) -> List[Dict[str, Any]]:
        """
        Recupera le tracce di un album.
        
        Args:
            artist_name: Nome dell'artista
            album_name: Nome dell'album
            
        Returns:
            Lista delle tracce
        """
        album_info = await self.get_album_info(artist_name, album_name)
        if not album_info:
            return []
        
        tracks_data = album_info.get('tracks', {}).get('track', [])
        
        # Last.fm può restituire un dict per una singola traccia
        if isinstance(tracks_data, dict):
            tracks_data = [tracks_data]
        
        return tracks_data
    
    def extract_genre_tags(self, tags_data: List[Dict[str, Any]]) -> List[str]:
        """
        Estrae i generi dai tag di Last.fm.
        
        Args:
            tags_data: Dati dei tag da Last.fm
            
        Returns:
            Lista dei generi
        """
        genres = []
        for tag in tags_data:
            if isinstance(tag, dict) and 'name' in tag:
                genres.append(tag['name'])
        
        return genres[:5]  # Limita ai primi 5 generi
    
    def parse_lastfm_date(self, date_str: str) -> Optional[str]:
        """
        Converte una data Last.fm in formato ISO.
        
        Args:
            date_str: Stringa data da Last.fm
            
        Returns:
            Data in formato ISO o None
        """
        if not date_str or date_str == "0":
            return None
        
        try:
            # Last.fm spesso fornisce solo l'anno
            if len(date_str) == 4 and date_str.isdigit():
                return f"{date_str}-01-01"
            
            # Potrebbero esserci altri formati, gestisci qui
            return date_str
            
        except Exception as e:
            logger.warning(f"Impossibile parsare data Last.fm: {date_str}, errore: {e}")
            return None
