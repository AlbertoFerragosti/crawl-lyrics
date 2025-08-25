"""
Client per l'API Genius - Progetto didattico.
Recupera metadati musicali rispettando le policy di copyright.
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
import aiohttp
from urllib.parse import quote
import time
import json

# Configurazione logging
logger = logging.getLogger(__name__)


class GeniusClient:
    """
    Client per l'API Genius per scopi didattici e di ricerca.
    
    Funzionalità:
    - Ricerca artisti e canzoni
    - Recupero metadati pubblici
    - Link ai testi ufficiali (NON testi completi)
    - Informazioni su album e discografia
    """
    
    def __init__(self, client_id: str, client_secret: str, access_token: str):
        """
        Inizializza il client Genius.
        
        Args:
            client_id: Client ID dell'app Genius
            client_secret: Client Secret dell'app Genius  
            access_token: Access Token per l'API
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.base_url = "https://api.genius.com"
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Rate limiting per rispettare i limiti dell'API
        self.last_request_time = 0
        self.min_request_interval = 0.5  # 500ms tra richieste
        self.requests_per_minute = 60
        self.request_times: List[float] = []
        
    async def __aenter__(self):
        """Context manager entry."""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'User-Agent': 'CrawlLyrics/1.0 (Educational Project)',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.session:
            await self.session.close()
    
    async def _rate_limit(self):
        """Implementa rate limiting avanzato."""
        current_time = time.time()
        
        # Rimuovi richieste più vecchie di 1 minuto
        self.request_times = [t for t in self.request_times if current_time - t < 60]
        
        # Controlla se abbiamo superato il limite per minuto
        if len(self.request_times) >= self.requests_per_minute:
            sleep_time = 60 - (current_time - self.request_times[0])
            if sleep_time > 0:
                logger.info(f"Rate limit raggiunto, aspetto {sleep_time:.1f}s")
                await asyncio.sleep(sleep_time)
        
        # Intervallo minimo tra richieste
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            await asyncio.sleep(sleep_time)
        
        # Registra questa richiesta
        self.last_request_time = time.time()
        self.request_times.append(self.last_request_time)
    
    async def search_artist(self, artist_name: str) -> Optional[Dict[str, Any]]:
        """
        Cerca un artista su Genius.
        
        Args:
            artist_name: Nome dell'artista da cercare
            
        Returns:
            Informazioni sull'artista o None se non trovato
        """
        await self._rate_limit()
        
        try:
            params = {
                'q': artist_name,
                'per_page': 5
            }
            
            async with self.session.get(f"{self.base_url}/search", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    hits = data.get('response', {}).get('hits', [])
                    
                    # Cerca il miglior match per l'artista
                    for hit in hits:
                        result = hit.get('result', {})
                        primary_artist = result.get('primary_artist', {})
                        
                        if primary_artist.get('name', '').lower() == artist_name.lower():
                            return await self._get_artist_details(primary_artist.get('id'))
                    
                    # Se non trova match esatto, prende il primo risultato
                    if hits:
                        first_hit = hits[0].get('result', {})
                        primary_artist = first_hit.get('primary_artist', {})
                        if primary_artist.get('id'):
                            return await self._get_artist_details(primary_artist.get('id'))
                
                else:
                    logger.error(f"Errore API Genius: {response.status}")
                    
        except Exception as e:
            logger.error(f"Errore nella ricerca artista: {e}")
        
        return None
    
    async def _get_artist_details(self, artist_id: int) -> Optional[Dict[str, Any]]:
        """
        Recupera dettagli completi di un artista.
        
        Args:
            artist_id: ID Genius dell'artista
            
        Returns:
            Dettagli dell'artista
        """
        await self._rate_limit()
        
        try:
            async with self.session.get(f"{self.base_url}/artists/{artist_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    artist_data = data.get('response', {}).get('artist', {})
                    
                    return {
                        'genius_id': artist_data.get('id'),
                        'name': artist_data.get('name'),
                        'image_url': artist_data.get('image_url'),
                        'header_image_url': artist_data.get('header_image_url'),
                        'url': artist_data.get('url'),
                        'followers_count': artist_data.get('followers_count'),
                        'description': self._clean_description(artist_data.get('description', {})),
                        'verified': artist_data.get('is_verified'),
                        'alternate_names': artist_data.get('alternate_names', []),
                        'facebook_name': artist_data.get('facebook_name'),
                        'instagram_name': artist_data.get('instagram_name'),
                        'twitter_name': artist_data.get('twitter_name')
                    }
                    
        except Exception as e:
            logger.error(f"Errore nel recupero dettagli artista: {e}")
        
        return None
    
    async def get_artist_songs(self, artist_id: int, page: int = 1, per_page: int = 20) -> List[Dict[str, Any]]:
        """
        Recupera le canzoni di un artista.
        
        Args:
            artist_id: ID Genius dell'artista
            page: Numero di pagina
            per_page: Canzoni per pagina (max 50)
            
        Returns:
            Lista delle canzoni
        """
        await self._rate_limit()
        
        try:
            params = {
                'page': page,
                'per_page': min(per_page, 50),  # Genius limita a 50
                'sort': 'popularity'
            }
            
            async with self.session.get(f"{self.base_url}/artists/{artist_id}/songs", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    songs = data.get('response', {}).get('songs', [])
                    
                    return [self._format_song_data(song) for song in songs]
                    
        except Exception as e:
            logger.error(f"Errore nel recupero canzoni: {e}")
        
        return []
    
    async def search_song(self, title: str, artist_name: str) -> Optional[Dict[str, Any]]:
        """
        Cerca una canzone specifica.
        
        Args:
            title: Titolo della canzone
            artist_name: Nome dell'artista
            
        Returns:
            Informazioni sulla canzone
        """
        await self._rate_limit()
        
        try:
            query = f"{artist_name} {title}"
            params = {
                'q': query,
                'per_page': 10
            }
            
            async with self.session.get(f"{self.base_url}/search", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    hits = data.get('response', {}).get('hits', [])
                    
                    # Cerca il miglior match
                    for hit in hits:
                        result = hit.get('result', {})
                        song_title = result.get('title', '').lower()
                        song_artist = result.get('primary_artist', {}).get('name', '').lower()
                        
                        if (title.lower() in song_title or song_title in title.lower()) and \
                           (artist_name.lower() in song_artist or song_artist in artist_name.lower()):
                            return self._format_song_data(result)
                    
                    # Se non trova match preciso, prende il primo risultato
                    if hits:
                        return self._format_song_data(hits[0].get('result', {}))
                        
        except Exception as e:
            logger.error(f"Errore nella ricerca canzone: {e}")
        
        return None
    
    def _format_song_data(self, song_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formatta i dati di una canzone per l'output.
        
        Args:
            song_data: Dati raw dalla API Genius
            
        Returns:
            Dati formattati della canzone
        """
        return {
            'genius_id': song_data.get('id'),
            'title': song_data.get('title'),
            'title_with_featured': song_data.get('title_with_featured'),
            'artist': {
                'name': song_data.get('primary_artist', {}).get('name'),
                'id': song_data.get('primary_artist', {}).get('id'),
                'url': song_data.get('primary_artist', {}).get('url')
            },
            'featured_artists': [
                {
                    'name': artist.get('name'),
                    'id': artist.get('id')
                }
                for artist in song_data.get('featured_artists', [])
            ],
            'release_date': song_data.get('release_date_for_display'),
            'page_views': song_data.get('stats', {}).get('pageviews'),
            'pyongs_count': song_data.get('pyongs_count'),
            'song_art_image_url': song_data.get('song_art_image_url'),
            'url': song_data.get('url'),
            'album': self._format_album_data(song_data.get('album')) if song_data.get('album') else None,
            
            # Informazioni legali
            'lyrics_url': song_data.get('url'),  # Link ufficiale ai testi
            'copyright_notice': 'Testi protetti da copyright - visita lyrics_url per il contenuto completo'
        }
    
    def _format_album_data(self, album_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formatta i dati di un album.
        
        Args:
            album_data: Dati raw dell'album
            
        Returns:
            Dati formattati dell'album
        """
        if not album_data:
            return None
            
        return {
            'genius_id': album_data.get('id'),
            'name': album_data.get('name'),
            'full_title': album_data.get('full_title'),
            'cover_art_url': album_data.get('cover_art_url'),
            'release_date': album_data.get('release_date_for_display'),
            'url': album_data.get('url'),
            'artist': {
                'name': album_data.get('artist', {}).get('name'),
                'id': album_data.get('artist', {}).get('id')
            }
        }
    
    def _clean_description(self, description: Dict[str, Any]) -> str:
        """
        Pulisce la descrizione dell'artista da HTML e formattazione.
        
        Args:
            description: Descrizione raw
            
        Returns:
            Descrizione pulita
        """
        if isinstance(description, dict):
            return description.get('plain', '').strip()
        return str(description).strip()
    
    async def get_comprehensive_artist_data(self, artist_name: str) -> Optional[Dict[str, Any]]:
        """
        Recupera dati completi di un artista incluse le canzoni più popolari.
        
        Args:
            artist_name: Nome dell'artista
            
        Returns:
            Dati completi dell'artista
        """
        artist_data = await self.search_artist(artist_name)
        if not artist_data:
            return None
        
        # Recupera le canzoni più popolari (prime 3 pagine)
        all_songs = []
        for page in range(1, 4):  # Prime 3 pagine
            songs = await self.get_artist_songs(artist_data['genius_id'], page=page, per_page=20)
            all_songs.extend(songs)
            
            # Se la pagina ha meno di 20 canzoni, è l'ultima
            if len(songs) < 20:
                break
        
        artist_data['songs'] = all_songs
        artist_data['total_songs_found'] = len(all_songs)
        
        return artist_data


# Funzioni di utilità per l'integrazione
async def search_genius_artist(artist_name: str, client_id: str, client_secret: str, access_token: str) -> Optional[Dict]:
    """
    Funzione helper per cercare un artista su Genius.
    
    Args:
        artist_name: Nome dell'artista
        client_id: Client ID Genius
        client_secret: Client Secret Genius
        access_token: Access Token Genius
        
    Returns:
        Dati dell'artista o None
    """
    async with GeniusClient(client_id, client_secret, access_token) as client:
        return await client.get_comprehensive_artist_data(artist_name)


async def search_genius_song(title: str, artist: str, client_id: str, client_secret: str, access_token: str) -> Optional[Dict]:
    """
    Funzione helper per cercare una canzone su Genius.
    
    Args:
        title: Titolo della canzone
        artist: Nome dell'artista
        client_id: Client ID Genius
        client_secret: Client Secret Genius
        access_token: Access Token Genius
        
    Returns:
        Dati della canzone o None
    """
    async with GeniusClient(client_id, client_secret, access_token) as client:
        return await client.search_song(title, artist)


# Configurazione delle credenziali per uso nel progetto
GENIUS_CONFIG = {
    'client_id': 'zPwicLU4TnfKE-O8YL7O8U6Rc40MGePoR5k8pTQG_LijOMWVnAbjCDBQT1Kgz22w',
    'client_secret': 'g1VtZNBTj4lVsElMkW8OankwxK7RqKNZOBGeZvijwLIMqEg5qBf3QIiR4tSPsxIctZOMs-HCzfQ50j9kHpHQuw',
    'access_token': '2myLsXND-Qngtcqve_5SnrSv5cYb1vg8A9062VkOqQIGg59XVxkNujtmSOID5lNB'
}
