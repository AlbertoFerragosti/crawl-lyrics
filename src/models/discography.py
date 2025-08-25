"""
Modelli di dati per la discografia musicale.
Utilizza Pydantic per validazione e serializzazione robusta.
"""

from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
import json


class Track(BaseModel):
    """Modello per una singola traccia musicale."""
    
    title: str = Field(..., description="Titolo della traccia")
    track_number: int = Field(..., ge=1, description="Numero della traccia nell'album")
    duration_ms: Optional[int] = Field(None, description="Durata in millisecondi")
    isrc: Optional[str] = Field(None, description="International Standard Recording Code")
    
    # Metadati aggiuntivi (NO testi completi per copyright)
    preview_available: bool = Field(default=False, description="Se è disponibile un'anteprima")
    explicit: bool = Field(default=False, description="Contenuto esplicito")
    
    # Riferimenti ETICI ai testi (NO testi completi)
    lyrics_reference: Optional[Dict[str, Any]] = Field(None, description="Riferimento legale ai testi")
    genius_url: Optional[str] = Field(None, description="Link ufficiale Genius per i testi")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }

    def __str__(self) -> str:
        return f"{self.track_number}. {self.title}"


class Album(BaseModel):
    """Modello per un album musicale."""
    
    title: str = Field(..., description="Titolo dell'album")
    release_date: Optional[date] = Field(None, description="Data di rilascio")
    release_year: Optional[int] = Field(None, description="Anno di rilascio")
    album_type: str = Field(default="album", description="Tipo di album (album, single, EP, etc.)")
    label: Optional[str] = Field(None, description="Casa discografica")
    catalog_number: Optional[str] = Field(None, description="Numero di catalogo")
    tracks: List[Track] = Field(default_factory=list, description="Lista delle tracce")
    
    # Identificatori
    musicbrainz_id: Optional[str] = Field(None, description="ID MusicBrainz")
    spotify_id: Optional[str] = Field(None, description="ID Spotify")
    lastfm_id: Optional[str] = Field(None, description="ID Last.fm")
    
    # Metadati aggiuntivi
    genre: Optional[List[str]] = Field(default_factory=list, description="Generi musicali")
    country: Optional[str] = Field(None, description="Paese di origine")
    
    @validator('release_year', pre=True, always=True)
    def extract_year_from_date(cls, v, values):
        """Estrae l'anno dalla data di rilascio se non specificato."""
        if v is None and 'release_date' in values and values['release_date']:
            return values['release_date'].year
        return v
    
    @property
    def track_count(self) -> int:
        """Numero totale di tracce nell'album."""
        return len(self.tracks)
    
    @property
    def total_duration_ms(self) -> int:
        """Durata totale dell'album in millisecondi."""
        return sum(track.duration_ms or 0 for track in self.tracks)
    
    def __str__(self) -> str:
        year_str = f" ({self.release_year})" if self.release_year else ""
        return f"{self.title}{year_str}"


class Artist(BaseModel):
    """Modello per un artista musicale."""
    
    name: str = Field(..., description="Nome dell'artista")
    sort_name: Optional[str] = Field(None, description="Nome per ordinamento")
    disambiguation: Optional[str] = Field(None, description="Disambiguazione")
    
    # Identificatori
    musicbrainz_id: Optional[str] = Field(None, description="ID MusicBrainz")
    spotify_id: Optional[str] = Field(None, description="ID Spotify")
    lastfm_id: Optional[str] = Field(None, description="ID Last.fm")
    
    # Metadati
    country: Optional[str] = Field(None, description="Paese di origine")
    begin_date: Optional[date] = Field(None, description="Data di inizio attività")
    end_date: Optional[date] = Field(None, description="Data di fine attività")
    artist_type: Optional[str] = Field(None, description="Tipo di artista (person, group, etc.)")
    gender: Optional[str] = Field(None, description="Genere (per persone)")
    
    def __str__(self) -> str:
        return self.name


class Discography(BaseModel):
    """Modello completo per la discografia di un artista."""
    
    artist: Artist = Field(..., description="Informazioni sull'artista")
    albums: List[Album] = Field(default_factory=list, description="Lista degli album")
    
    # Metadati di crawling
    crawled_at: datetime = Field(default_factory=datetime.now, description="Timestamp del crawling")
    sources: List[str] = Field(default_factory=list, description="Fonti dei dati")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadati aggiuntivi da fonti esterne")
    
    @property
    def total_albums(self) -> int:
        """Numero totale di album."""
        return len(self.albums)
    
    @property
    def total_tracks(self) -> int:
        """Numero totale di tracce in tutta la discografia."""
        return sum(album.track_count for album in self.albums)
    
    @property
    def discography_span(self) -> Dict[str, Optional[int]]:
        """Periodo di attività della discografia."""
        years = [album.release_year for album in self.albums if album.release_year]
        if not years:
            return {"start": None, "end": None}
        
        return {
            "start": min(years),
            "end": max(years)
        }
    
    def get_albums_by_year(self) -> Dict[int, List[Album]]:
        """Raggruppa gli album per anno."""
        albums_by_year = {}
        for album in self.albums:
            if album.release_year:
                if album.release_year not in albums_by_year:
                    albums_by_year[album.release_year] = []
                albums_by_year[album.release_year].append(album)
        return albums_by_year
    
    def get_albums_by_type(self) -> Dict[str, List[Album]]:
        """Raggruppa gli album per tipo."""
        albums_by_type = {}
        for album in self.albums:
            album_type = album.album_type or "unknown"
            if album_type not in albums_by_type:
                albums_by_type[album_type] = []
            albums_by_type[album_type].append(album)
        return albums_by_type
    
    def to_json(self, indent: int = 2) -> str:
        """Converte la discografia in JSON formattato."""
        return json.dumps(
            self.dict(),
            indent=indent,
            default=str,
            ensure_ascii=False
        )
    
    def save_to_file(self, filepath: str) -> None:
        """Salva la discografia in un file JSON."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }


class CrawlStatus(BaseModel):
    """Modello per il tracking dello stato del crawling."""
    
    artist_name: str
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    status: str = Field(default="in_progress")  # in_progress, completed, failed
    albums_found: int = Field(default=0)
    tracks_found: int = Field(default=0)
    errors: List[str] = Field(default_factory=list)
    sources_used: List[str] = Field(default_factory=list)
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """Durata del crawling in secondi."""
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
    
    def mark_completed(self):
        """Marca il crawling come completato."""
        self.status = "completed"
        self.completed_at = datetime.now()
    
    def mark_failed(self, error: str):
        """Marca il crawling come fallito."""
        self.status = "failed"
        self.completed_at = datetime.now()
        self.errors.append(error)
    
    def add_error(self, error: str):
        """Aggiunge un errore alla lista."""
        self.errors.append(error)
