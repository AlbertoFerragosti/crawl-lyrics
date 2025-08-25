"""
Client per l'API MusicBrainz.
Fornisce accesso ai metadati musicali open source.
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import musicbrainzngs as mb
from ..models.discography import Artist, Album, Track

# Configurazione logging
logger = logging.getLogger(__name__)


class MusicBrainzClient:
    """Client per interagire con l'API MusicBrainz."""
    
    def __init__(self, user_agent: str = "DiscographyCrawler/1.0"):
        """
        Inizializza il client MusicBrainz.
        
        Args:
            user_agent: User agent per le richieste API
        """
        self.user_agent = user_agent
        self._setup_client()
    
    def _setup_client(self):
        """Configura il client MusicBrainz."""
        mb.set_useragent(
            app="DiscographyCrawler",
            version="1.0",
            contact="https://github.com/yourusername/crawl-lyrics"
        )
        mb.set_rate_limit(limit_or_interval=1.0, new_requests=1)
    
    async def search_artist(self, artist_name: str) -> List[Artist]:
        """
        Cerca un artista per nome.
        
        Args:
            artist_name: Nome dell'artista da cercare
            
        Returns:
            Lista di artisti trovati
        """
        try:
            # MusicBrainz è sincrono, lo avvolgiamo in un executor
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: mb.search_artists(artist=artist_name, limit=10)
            )
            
            artists = []
            for artist_data in result.get('artist-list', []):
                artist = self._parse_artist(artist_data)
                artists.append(artist)
            
            logger.info(f"Trovati {len(artists)} artisti per '{artist_name}'")
            return artists
            
        except Exception as e:
            logger.error(f"Errore nella ricerca artista '{artist_name}': {e}")
            return []
    
    async def get_artist_discography(self, artist_id: str) -> List[Album]:
        """
        Recupera la discografia completa di un artista.
        
        Args:
            artist_id: ID MusicBrainz dell'artista
            
        Returns:
            Lista degli album dell'artista
        """
        try:
            loop = asyncio.get_event_loop()
            
            # Recupera tutti i release group (album)
            result = await loop.run_in_executor(
                None,
                lambda: mb.browse_release_groups(
                    artist=artist_id,
                    limit=100
                )
            )
            
            albums = []
            for rg_data in result.get('release-group-list', []):
                album = await self._parse_release_group(rg_data)
                if album:
                    albums.append(album)
            
            # Ordina per data di rilascio
            albums.sort(key=lambda x: x.release_year or 0)
            
            logger.info(f"Trovati {len(albums)} album per artista {artist_id}")
            return albums
            
        except Exception as e:
            logger.error(f"Errore nel recupero discografia per {artist_id}: {e}")
            return []
    
    async def get_album_tracks(self, release_id: str) -> List[Track]:
        """
        Recupera le tracce di un album specifico.
        
        Args:
            release_id: ID MusicBrainz del release
            
        Returns:
            Lista delle tracce dell'album
        """
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: mb.get_release_by_id(
                    release_id,
                    includes=['recordings', 'media']
                )
            )
            
            tracks = []
            release_data = result.get('release', {})
            
            for medium in release_data.get('medium-list', []):
                for track_data in medium.get('track-list', []):
                    track = self._parse_track(track_data)
                    tracks.append(track)
            
            return tracks
            
        except Exception as e:
            logger.error(f"Errore nel recupero tracce per release {release_id}: {e}")
            return []
    
    def _parse_artist(self, artist_data: Dict[str, Any]) -> Artist:
        """Converte i dati MusicBrainz in un oggetto Artist."""
        return Artist(
            name=artist_data.get('name', ''),
            sort_name=artist_data.get('sort-name'),
            disambiguation=artist_data.get('disambiguation'),
            musicbrainz_id=artist_data.get('id'),
            country=artist_data.get('country'),
            begin_date=self._parse_date(artist_data.get('life-span', {}).get('begin')),
            end_date=self._parse_date(artist_data.get('life-span', {}).get('end')),
            artist_type=artist_data.get('type'),
            gender=artist_data.get('gender')
        )
    
    async def _parse_release_group(self, rg_data: Dict[str, Any]) -> Optional[Album]:
        """Converte i dati MusicBrainz in un oggetto Album."""
        try:
            # Trova il release principale (di solito il primo)
            releases = rg_data.get('release-list', [])
            if not releases:
                return None
            
            primary_release = releases[0]
            release_id = primary_release.get('id')
            
            # Recupera le tracce per questo release
            tracks = await self.get_album_tracks(release_id) if release_id else []
            
            return Album(
                title=rg_data.get('title', ''),
                release_date=self._parse_date(primary_release.get('date')),
                album_type=rg_data.get('primary-type', 'album').lower(),
                musicbrainz_id=rg_data.get('id'),
                tracks=tracks
            )
            
        except Exception as e:
            logger.error(f"Errore nel parsing release group: {e}")
            return None
    
    def _parse_track(self, track_data: Dict[str, Any]) -> Track:
        """Converte i dati MusicBrainz in un oggetto Track."""
        recording = track_data.get('recording', {})
        
        # Converti durata da ms a int
        duration_ms = None
        if track_data.get('length'):
            try:
                duration_ms = int(track_data['length'])
            except (ValueError, TypeError):
                pass
        
        return Track(
            title=recording.get('title', track_data.get('title', '')),
            track_number=int(track_data.get('position', 1)),
            duration_ms=duration_ms,
            isrc=None  # MusicBrainz non sempre fornisce ISRC nei browse
        )
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[date]:
        """Converte una stringa data MusicBrainz in un oggetto date."""
        if not date_str:
            return None
        
        try:
            # MusicBrainz può fornire date parziali (solo anno, anno-mese)
            date_parts = date_str.split('-')
            
            if len(date_parts) == 1:  # Solo anno
                return date(int(date_parts[0]), 1, 1)
            elif len(date_parts) == 2:  # Anno-mese
                return date(int(date_parts[0]), int(date_parts[1]), 1)
            elif len(date_parts) == 3:  # Data completa
                return date(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
                
        except (ValueError, IndexError):
            logger.warning(f"Impossibile parsare la data: {date_str}")
        
        return None
    
    async def get_artist_by_id(self, artist_id: str) -> Optional[Artist]:
        """
        Recupera i dettagli di un artista tramite ID.
        
        Args:
            artist_id: ID MusicBrainz dell'artista
            
        Returns:
            Oggetto Artist o None se non trovato
        """
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: mb.get_artist_by_id(artist_id)
            )
            
            artist_data = result.get('artist', {})
            return self._parse_artist(artist_data)
            
        except Exception as e:
            logger.error(f"Errore nel recupero artista {artist_id}: {e}")
            return None
