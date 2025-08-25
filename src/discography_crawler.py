"""
Crawler principale per la discografia degli artisti.
Orchestra i vari servizi per creare una discografia completa.
"""

import asyncio
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

from .models.discography import Artist, Album, Track, Discography, CrawlStatus
from .services.musicbrainz_client import MusicBrainzClient
from .services.lastfm_client import LastFmClient
from .crawlers.base_crawler import BaseCrawler, CrawlerError

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiscographyCrawler(BaseCrawler):
    """Crawler principale per la discografia degli artisti musicali."""
    
    def __init__(self, 
                 lastfm_api_key: Optional[str] = None,
                 rate_limit_requests: int = 5,
                 rate_limit_window: int = 60,
                 max_retries: int = 3):
        """
        Inizializza il crawler per la discografia.
        
        Args:
            lastfm_api_key: Chiave API Last.fm (opzionale)
            rate_limit_requests: Richieste massime per finestra temporale
            rate_limit_window: Finestra temporale in secondi
            max_retries: Numero massimo di retry
        """
        super().__init__(rate_limit_requests, rate_limit_window, max_retries)
        
        self.musicbrainz_client = MusicBrainzClient()
        self.lastfm_api_key = lastfm_api_key
        self.status: Optional[CrawlStatus] = None
    
    async def get_artist_discography(self, artist_name: str) -> Discography:
        """
        Recupera la discografia completa di un artista.
        
        Args:
            artist_name: Nome dell'artista
            
        Returns:
            Discografia completa dell'artista
            
        Raises:
            CrawlerError: Se il crawling fallisce
        """
        self.status = CrawlStatus(artist_name=artist_name)
        
        try:
            self.logger.info(f"Inizio crawling per artista: {artist_name}")
            
            # 1. Cerca l'artista su MusicBrainz
            artists = await self.make_request(
                self.musicbrainz_client.search_artist, 
                artist_name
            )
            
            if not artists:
                raise CrawlerError(f"Artista '{artist_name}' non trovato")
            
            # Prendi il primo risultato (più rilevante)
            primary_artist = artists[0]
            self.logger.info(f"Trovato artista: {primary_artist.name} (ID: {primary_artist.musicbrainz_id})")
            
            # 2. Recupera la discografia da MusicBrainz
            mb_albums = await self.make_request(
                self.musicbrainz_client.get_artist_discography,
                primary_artist.musicbrainz_id
            )
            
            self.status.albums_found = len(mb_albums)
            self.logger.info(f"Trovati {len(mb_albums)} album su MusicBrainz")
            
            # 3. Arricchisci con dati da Last.fm (se disponibile)
            enhanced_albums = await self._enhance_with_lastfm(primary_artist, mb_albums)
            
            # 4. Conta le tracce totali
            total_tracks = sum(len(album.tracks) for album in enhanced_albums)
            self.status.tracks_found = total_tracks
            
            # 5. Crea la discografia finale
            discography = Discography(
                artist=primary_artist,
                albums=enhanced_albums,
                sources=["MusicBrainz"]
            )
            
            if self.lastfm_api_key:
                discography.sources.append("Last.fm")
            
            self.status.mark_completed()
            self.logger.info(f"Crawling completato: {total_tracks} tracce in {len(enhanced_albums)} album")
            
            return discography
            
        except Exception as e:
            if self.status:
                self.status.mark_failed(str(e))
            self.logger.error(f"Errore durante il crawling: {e}")
            raise CrawlerError(f"Fallimento nel crawling per '{artist_name}': {e}")
    
    async def _enhance_with_lastfm(self, artist: Artist, albums: List[Album]) -> List[Album]:
        """
        Arricchisce gli album con informazioni da Last.fm.
        
        Args:
            artist: Artista di riferimento
            albums: Lista degli album da arricchire
            
        Returns:
            Lista degli album arricchiti
        """
        if not self.lastfm_api_key:
            self.logger.info("API Key Last.fm non fornita, salto l'arricchimento")
            return albums
        
        enhanced_albums = []
        
        async with LastFmClient(self.lastfm_api_key) as lastfm:
            for album in albums:
                try:
                    # Recupera info aggiuntive da Last.fm
                    lastfm_album = await self.make_request(
                        lastfm.get_album_info,
                        artist.name,
                        album.title
                    )
                    
                    if lastfm_album:
                        # Arricchisci con informazioni da Last.fm
                        enhanced_album = await self._merge_album_data(album, lastfm_album)
                        enhanced_albums.append(enhanced_album)
                        
                        # Piccola pausa per essere gentili con l'API
                        await asyncio.sleep(0.1)
                    else:
                        # Mantieni l'album originale se Last.fm non ha info
                        enhanced_albums.append(album)
                        
                except Exception as e:
                    self.logger.warning(f"Errore nell'arricchimento album '{album.title}': {e}")
                    enhanced_albums.append(album)
        
        return enhanced_albums
    
    async def _merge_album_data(self, mb_album: Album, lastfm_data: Dict[str, Any]) -> Album:
        """
        Unisce i dati MusicBrainz con quelli di Last.fm.
        
        Args:
            mb_album: Album da MusicBrainz
            lastfm_data: Dati da Last.fm
            
        Returns:
            Album arricchito
        """
        # Copia l'album esistente
        enhanced_album = mb_album.copy(deep=True)
        
        # Arricchisci con generi da Last.fm
        if 'tags' in lastfm_data and 'tag' in lastfm_data['tags']:
            tags = lastfm_data['tags']['tag']
            if isinstance(tags, list):
                enhanced_album.genre = [tag.get('name', '') for tag in tags[:5]]
            elif isinstance(tags, dict):
                enhanced_album.genre = [tags.get('name', '')]
        
        # Aggiungi informazioni sulla label se disponibili
        if not enhanced_album.label and 'label' in lastfm_data:
            enhanced_album.label = lastfm_data['label']
        
        # Arricchisci le tracce se Last.fm ha informazioni migliori
        if 'tracks' in lastfm_data and 'track' in lastfm_data['tracks']:
            lastfm_tracks = lastfm_data['tracks']['track']
            if isinstance(lastfm_tracks, list):
                enhanced_album.tracks = await self._enhance_tracks(
                    enhanced_album.tracks, 
                    lastfm_tracks
                )
        
        return enhanced_album
    
    async def _enhance_tracks(self, mb_tracks: List[Track], lastfm_tracks: List[Dict]) -> List[Track]:
        """
        Arricchisce le tracce con dati da Last.fm.
        
        Args:
            mb_tracks: Tracce da MusicBrainz
            lastfm_tracks: Tracce da Last.fm
            
        Returns:
            Lista delle tracce arricchite
        """
        enhanced_tracks = []
        
        for i, mb_track in enumerate(mb_tracks):
            enhanced_track = mb_track.copy(deep=True)
            
            # Cerca la traccia corrispondente in Last.fm
            if i < len(lastfm_tracks):
                lastfm_track = lastfm_tracks[i]
                
                # Converti durata se disponibile
                if 'duration' in lastfm_track and not enhanced_track.duration_ms:
                    try:
                        # Last.fm fornisce durata in secondi (string)
                        duration_seconds = int(lastfm_track['duration'])
                        enhanced_track.duration_ms = duration_seconds * 1000
                    except (ValueError, TypeError):
                        pass
            
            enhanced_tracks.append(enhanced_track)
        
        return enhanced_tracks
    
    async def search_artists(self, query: str, limit: int = 10) -> List[Artist]:
        """
        Cerca artisti per nome.
        
        Args:
            query: Query di ricerca
            limit: Numero massimo di risultati
            
        Returns:
            Lista degli artisti trovati
        """
        try:
            artists = await self.make_request(
                self.musicbrainz_client.search_artist,
                query
            )
            
            return artists[:limit]
            
        except Exception as e:
            self.logger.error(f"Errore nella ricerca artisti: {e}")
            return []
    
    async def get_crawl_status(self) -> Optional[CrawlStatus]:
        """
        Restituisce lo stato corrente del crawling.
        
        Returns:
            Stato del crawling o None
        """
        return self.status
    
    async def crawl(self, artist_name: str) -> Discography:
        """
        Implementazione del metodo astratto della classe base.
        
        Args:
            artist_name: Nome dell'artista
            
        Returns:
            Discografia dell'artista
        """
        return await self.get_artist_discography(artist_name)


# Funzione di utilità per uso semplificato
async def crawl_artist_discography(artist_name: str, 
                                 lastfm_api_key: Optional[str] = None) -> Discography:
    """
    Funzione di utilità per il crawling rapido di una discografia.
    
    Args:
        artist_name: Nome dell'artista
        lastfm_api_key: Chiave API Last.fm (opzionale)
        
    Returns:
        Discografia dell'artista
    """
    async with DiscographyCrawler(lastfm_api_key=lastfm_api_key) as crawler:
        return await crawler.crawl(artist_name)
