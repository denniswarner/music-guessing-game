"""
Spotify API Client Module

Handles all interactions with the Spotify API including authentication,
searching, and retrieving track information.
"""

from typing import List, Dict, Any, Optional
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    """
    Client for interacting with Spotify's API.
    
    Handles authentication and provides methods to search for songs,
    fetch playlists, and retrieve artist information.
    """
    
    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize the Spotify client with API credentials.
        
        Args:
            client_id (str): Spotify API Client ID
            client_secret (str): Spotify API Client Secret
            
        Raises:
            spotipy.SpotifyException: If authentication fails
        """
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager
        )
    
    def get_songs_by_genre(
        self, 
        genre: str, 
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search for songs by genre or keyword.
        
        Args:
            genre (str): Genre or search term (e.g., 'rock', '90s', 'jazz')
            limit (int): Maximum number of songs to return (default: 50)
            
        Returns:
            List[Dict[str, Any]]: List of track objects with preview URLs
        """
        print(f"🎵 Searching for {genre} songs...")
        results = self.sp.search(q=f'genre:{genre}', type='track', limit=limit)
        
        # Filter songs that have preview URLs
        songs_with_previews = [
            track for track in results['tracks']['items']
            if track['preview_url'] is not None
        ]
        
        return songs_with_previews
    
    def get_songs_from_playlist(self, playlist_url: str) -> List[Dict[str, Any]]:
        """
        Get songs from a Spotify playlist URL.
        
        Args:
            playlist_url (str): Full Spotify playlist URL
            
        Returns:
            List[Dict[str, Any]]: List of track objects with preview URLs
            
        Raises:
            ValueError: If playlist URL is invalid
        """
        # Extract playlist ID from URL
        # Format: https://open.spotify.com/playlist/{id}?...
        try:
            playlist_id = playlist_url.split('/')[-1].split('?')[0]
        except (IndexError, AttributeError):
            raise ValueError(f"Invalid playlist URL: {playlist_url}")
        
        print(f"🎵 Loading playlist...")
        results = self.sp.playlist_tracks(playlist_id)
        
        songs_with_previews = [
            track['track'] for track in results['items']
            if track['track'] and track['track']['preview_url'] is not None
        ]
        
        return songs_with_previews
    
    def get_top_tracks(
        self, 
        artist_name: str, 
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get top tracks from a specific artist.
        
        Args:
            artist_name (str): Name of the artist to search for
            limit (int): Unused, kept for API consistency
            
        Returns:
            List[Dict[str, Any]]: List of artist's top tracks with preview URLs
            
        Note:
            Returns empty list if artist not found.
        """
        print(f"🎵 Searching for {artist_name}'s songs...")
        results = self.sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
        
        if not results['artists']['items']:
            print(f"Artist '{artist_name}' not found!")
            return []
        
        artist_id = results['artists']['items'][0]['id']
        top_tracks = self.sp.artist_top_tracks(artist_id)
        
        songs_with_previews = [
            track for track in top_tracks['tracks']
            if track['preview_url'] is not None
        ]
        
        return songs_with_previews
    
    @staticmethod
    def validate_preview_url(track: Dict[str, Any]) -> bool:
        """
        Check if a track has a valid preview URL.
        
        Args:
            track (Dict[str, Any]): Spotify track object
            
        Returns:
            bool: True if preview URL exists and is not None
        """
        return track.get('preview_url') is not None
