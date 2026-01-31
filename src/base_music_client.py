"""
Base Music Provider Client

Abstract base class that defines the interface for all music provider clients.
This ensures consistency across different music service integrations.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseMusicClient(ABC):
    """
    Abstract base class for music provider clients.
    
    All music provider implementations (Spotify, Deezer, etc.) should inherit
    from this class and implement all abstract methods.
    """
    
    @abstractmethod
    def get_songs_by_genre(self, genre: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for songs by genre or keyword.
        
        Args:
            genre (str): Genre or search term (e.g., 'rock', '90s', 'jazz')
            limit (int): Maximum number of songs to return (default: 50)
            
        Returns:
            List[Dict[str, Any]]: List of track objects with preview URLs
        """
        pass
    
    @abstractmethod
    def get_songs_from_playlist(self, playlist_url: str) -> List[Dict[str, Any]]:
        """
        Get songs from a playlist URL.
        
        Args:
            playlist_url (str): Full playlist URL
            
        Returns:
            List[Dict[str, Any]]: List of track objects with preview URLs
            
        Raises:
            ValueError: If playlist URL is invalid
        """
        pass
    
    @abstractmethod
    def get_top_tracks(self, artist_name: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get top tracks from a specific artist.
        
        Args:
            artist_name (str): Name of the artist to search for
            limit (int): Maximum number of tracks to return (default: 20)
            
        Returns:
            List[Dict[str, Any]]: List of artist's top tracks with preview URLs
        """
        pass
    
    @staticmethod
    @abstractmethod
    def validate_preview_url(track: Dict[str, Any]) -> bool:
        """
        Check if a track has a valid preview URL.
        
        Args:
            track (Dict[str, Any]): Track object
            
        Returns:
            bool: True if preview URL exists and is valid
        """
        pass
    
    @staticmethod
    @abstractmethod
    def normalize_track_format(track: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize track data to a common format.
        
        This ensures all providers return data in the same structure,
        making it easier for the game engine to process tracks.
        
        Expected output format:
        {
            'id': str,
            'name': str,
            'artists': [{'name': str}],
            'album': {'name': str, 'release_date': str},
            'preview_url': str
        }
        
        Args:
            track (Dict[str, Any]): Provider-specific track object
            
        Returns:
            Dict[str, Any]: Normalized track object
        """
        pass
