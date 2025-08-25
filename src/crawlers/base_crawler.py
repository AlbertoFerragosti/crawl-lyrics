"""
Classe base per i crawler.
Fornisce funzionalità comuni per rate limiting e gestione errori.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import time

# Configurazione logging
logger = logging.getLogger(__name__)


class RateLimiter:
    """Gestisce il rate limiting per le richieste API."""
    
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        """
        Inizializza il rate limiter.
        
        Args:
            max_requests: Numero massimo di richieste nel time window
            time_window: Finestra temporale in secondi
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquista il permesso per una richiesta."""
        async with self._lock:
            now = time.time()
            
            # Rimuovi richieste vecchie
            self.requests = [req_time for req_time in self.requests 
                           if now - req_time < self.time_window]
            
            # Se abbiamo raggiunto il limite, aspetta
            if len(self.requests) >= self.max_requests:
                oldest_request = min(self.requests)
                sleep_time = self.time_window - (now - oldest_request)
                if sleep_time > 0:
                    logger.info(f"Rate limit raggiunto, aspetto {sleep_time:.2f} secondi")
                    await asyncio.sleep(sleep_time)
                    return await self.acquire()
            
            # Registra la richiesta
            self.requests.append(now)


class RetryManager:
    """Gestisce la logica di retry per le richieste fallite."""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        """
        Inizializza il retry manager.
        
        Args:
            max_retries: Numero massimo di tentativi
            base_delay: Delay base tra i tentativi
            max_delay: Delay massimo tra i tentativi
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    async def execute_with_retry(self, func, *args, **kwargs):
        """
        Esegue una funzione con retry automatico.
        
        Args:
            func: Funzione da eseguire
            *args: Argomenti posizionali
            **kwargs: Argomenti nominali
            
        Returns:
            Risultato della funzione
            
        Raises:
            Exception: L'ultima eccezione dopo tutti i tentativi falliti
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    logger.warning(f"Tentativo {attempt + 1} fallito: {e}. Riprovo tra {delay}s")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Tutti i {self.max_retries + 1} tentativi falliti")
        
        raise last_exception


class BaseCrawler(ABC):
    """Classe base per tutti i crawler."""
    
    def __init__(self, 
                 rate_limit_requests: int = 10,
                 rate_limit_window: int = 60,
                 max_retries: int = 3):
        """
        Inizializza il crawler base.
        
        Args:
            rate_limit_requests: Richieste massime per finestra temporale
            rate_limit_window: Finestra temporale in secondi
            max_retries: Numero massimo di retry
        """
        self.rate_limiter = RateLimiter(rate_limit_requests, rate_limit_window)
        self.retry_manager = RetryManager(max_retries)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Statistiche
        self.stats = {
            'requests_made': 0,
            'requests_successful': 0,
            'requests_failed': 0,
            'total_retry_attempts': 0,
            'start_time': None,
            'end_time': None
        }
    
    async def make_request(self, func, *args, **kwargs):
        """
        Esegue una richiesta con rate limiting e retry.
        
        Args:
            func: Funzione da eseguire
            *args: Argomenti posizionali
            **kwargs: Argomenti nominali
            
        Returns:
            Risultato della funzione
        """
        await self.rate_limiter.acquire()
        
        try:
            self.stats['requests_made'] += 1
            
            result = await self.retry_manager.execute_with_retry(func, *args, **kwargs)
            
            self.stats['requests_successful'] += 1
            return result
            
        except Exception as e:
            self.stats['requests_failed'] += 1
            self.logger.error(f"Richiesta fallita definitivamente: {e}")
            raise
    
    def start_timing(self):
        """Inizia il timing delle operazioni."""
        self.stats['start_time'] = datetime.now()
    
    def end_timing(self):
        """Termina il timing delle operazioni."""
        self.stats['end_time'] = datetime.now()
    
    @property
    def execution_time(self) -> Optional[timedelta]:
        """Restituisce il tempo di esecuzione."""
        if self.stats['start_time'] and self.stats['end_time']:
            return self.stats['end_time'] - self.stats['start_time']
        return None
    
    def get_stats_summary(self) -> Dict[str, Any]:
        """Restituisce un riassunto delle statistiche."""
        return {
            'requests_made': self.stats['requests_made'],
            'requests_successful': self.stats['requests_successful'],
            'requests_failed': self.stats['requests_failed'],
            'success_rate': (
                self.stats['requests_successful'] / self.stats['requests_made'] 
                if self.stats['requests_made'] > 0 else 0
            ),
            'execution_time_seconds': (
                self.execution_time.total_seconds() 
                if self.execution_time else None
            ),
            'requests_per_second': (
                self.stats['requests_made'] / self.execution_time.total_seconds()
                if self.execution_time and self.execution_time.total_seconds() > 0 else 0
            )
        }
    
    @abstractmethod
    async def crawl(self, *args, **kwargs):
        """Metodo principale di crawling - deve essere implementato dalle sottoclassi."""
        pass
    
    async def __aenter__(self):
        """Context manager entry."""
        self.start_timing()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.end_timing()
        
        # Log delle statistiche finali
        stats = self.get_stats_summary()
        self.logger.info(f"Crawling completato: {stats}")


class CrawlerError(Exception):
    """Eccezione base per i crawler."""
    pass


class RateLimitError(CrawlerError):
    """Eccezione per errori di rate limiting."""
    pass


class DataParsingError(CrawlerError):
    """Eccezione per errori di parsing dei dati."""
    pass


class APIError(CrawlerError):
    """Eccezione per errori dell'API."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code
