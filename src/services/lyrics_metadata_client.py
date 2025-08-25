"""
ESTENSIONE ETICA per Lyrics Metadata (NON testi completi).
Fornisce link e snippet minimi per identificazione, rispettando copyright.
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
import aiohttp
from urllib.parse import quote
import time

# Configurazione logging
logger = logging.getLogger(__name__)


class LyricsMetadataClient:
    """
    Client ETICO per metadati dei testi.
    
    IMPORTANTE: Questo client NON estrae testi completi per rispetto del copyright.
    Fornisce solo:
    - Link ai testi originali
    - Snippet minimi per identificazione (Fair Use)
    - Metadati pubblici
    """
    
    def __init__(self, genius_token: Optional[str] = None):
        """
        Inizializza il client per metadati etici.
        
        Args:
            genius_token: Token API Genius (opzionale)
        """
        self.genius_token = genius_token
        self.base_url = "https://api.genius.com"
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Rate limiting etico
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 secondo tra richieste
        
    async def __aenter__(self):
        """Context manager entry."""
        headers = {
            'User-Agent': 'DiscographyCrawler/1.0 (Educational Research)',
            'Accept': 'application/json'
        }
        
        if self.genius_token:
            headers['Authorization'] = f'Bearer {self.genius_token}'
        
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
        """Implementa rate limiting etico."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    async def search_song_metadata(self, title: str, artist: str) -> Optional[Dict[str, Any]]:
        """
        Cerca metadati di una canzone (NON testi completi).
        
        Args:
            title: Titolo della canzone
            artist: Nome dell'artista
            
        Returns:
            Metadati della canzone o None
        """
        if not self.session or not self.genius_token:
            logger.warning("Token Genius non fornito - funzionalità limitata")
            return None
        
        await self._rate_limit()
        
        try:
            query = f"{artist} {title}"
            params = {
                'q': query,
                'per_page': 1  # Solo il primo risultato
            }
            
            async with self.session.get(f"{self.base_url}/search", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    hits = data.get('response', {}).get('hits', [])
                    
                    if hits:
                        song_data = hits[0].get('result', {})
                        return await self._extract_safe_metadata(song_data)
                    
                else:
                    logger.warning(f"Genius API error: {response.status}")
                    
        except Exception as e:
            logger.error(f"Errore nella ricerca metadati: {e}")
        
        return None
    
    async def _extract_safe_metadata(self, song_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estrae solo metadati sicuri (NO testi completi).
        
        Args:
            song_data: Dati raw dalla API Genius
            
        Returns:
            Metadati sicuri per copyright
        """
        # SOLO metadati pubblici - NO testi completi
        safe_metadata = {
            'genius_id': song_data.get('id'),
            'title': song_data.get('title'),
            'artist_name': song_data.get('primary_artist', {}).get('name'),
            'release_date': song_data.get('release_date_for_display'),
            'page_views': song_data.get('stats', {}).get('pageviews'),
            
            # Link ufficiale (LEGALE)
            'genius_url': song_data.get('url'),
            
            # Metadati album se disponibili
            'album': song_data.get('album', {}).get('name') if song_data.get('album') else None,
            
            # Featured artists
            'featured_artists': [
                artist.get('name') for artist in song_data.get('featured_artists', [])
            ],
            
            # IMPORTANTE: Disclaimer copyright
            'copyright_notice': 'Testi protetti da copyright - visita genius_url per il contenuto completo',
            'fair_use_notice': 'Solo metadati per identificazione - uso educativo/ricerca'
        }
        
        # Aggiungi un MINIMO snippet per identificazione (Fair Use)
        # MASSIMO 10-15 parole per non violare copyright
        snippet = await self._get_identification_snippet(song_data)
        if snippet:
            safe_metadata['identification_snippet'] = snippet
            safe_metadata['snippet_disclaimer'] = 'Snippet minimale solo per identificazione (Fair Use)'
        
        return safe_metadata
    
    async def _get_identification_snippet(self, song_data: Dict[str, Any]) -> Optional[str]:
        """
        Estrae un snippet MINIMO per identificazione (Fair Use).
        
        IMPORTANTE: Solo prime 2-3 parole per non violare copyright.
        """
        try:
            # Se disponibile description o excerpt pubblico
            description = song_data.get('description', {})
            if isinstance(description, dict) and 'plain' in description:
                text = description['plain']
                words = text.split()[:3]  # MASSIMO 3 parole
                if len(words) >= 2:
                    return ' '.join(words) + '...'
            
            # Fallback: solo titolo della canzone (già pubblico)
            return f"Canzone: {song_data.get('title', 'N/A')}"
            
        except Exception as e:
            logger.warning(f"Errore nell'estrazione snippet: {e}")
            return None
    
    def create_legal_lyrics_reference(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un riferimento LEGALE ai testi.
        
        Args:
            metadata: Metadati della canzone
            
        Returns:
            Riferimento legale con link ufficiale
        """
        return {
            'title': metadata.get('title'),
            'artist': metadata.get('artist_name'),
            'lyrics_available': metadata.get('genius_url') is not None,
            'official_lyrics_url': metadata.get('genius_url'),
            'how_to_access': 'Visita il link ufficiale per i testi completi',
            'legal_notice': 'I testi sono protetti da copyright. Questo sistema fornisce solo link di riferimento.',
            'identification_help': metadata.get('identification_snippet'),
            'disclaimer': 'Per uso educativo e di ricerca. Rispetta sempre i diritti d\'autore.'
        }


# Esempio di uso ETICO
async def get_song_reference(title: str, artist: str, genius_token: str) -> Optional[Dict]:
    """
    Esempio di utilizzo ETICO per ottenere riferimenti ai testi.
    
    Args:
        title: Titolo canzone
        artist: Nome artista
        genius_token: Token API Genius
        
    Returns:
        Riferimento legale ai testi
    """
    async with LyricsMetadataClient(genius_token) as client:
        metadata = await client.search_song_metadata(title, artist)
        
        if metadata:
            return client.create_legal_lyrics_reference(metadata)
        
        return None


# Template di disclaimer per l'integrazione
LYRICS_DISCLAIMER = """
🚨 IMPORTANTE DISCLAIMER LEGALE 🚨

I testi delle canzoni sono protetti da copyright. Questo sistema:

✅ FORNISCE: Link ufficiali ai testi
✅ FORNISCE: Metadati pubblici per identificazione  
✅ FORNISCE: Snippet minimi per Fair Use educativo

❌ NON FORNISCE: Testi completi protetti da copyright
❌ NON MEMORIZZA: Contenuto protetto da diritti d'autore
❌ NON REDISTRIBUISCE: Materiale sotto copyright

Per accedere ai testi completi, utilizzare sempre i link ufficiali forniti.
Uso solo per scopi educativi e di ricerca.
""".strip()
