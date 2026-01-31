"""
Deezer API Client Module

Handles all interactions with the Deezer API including searching,
and retrieving track information with 30-second audio previews.
"""

from typing import List, Dict, Any, Optional
import requests
from src.base_music_client import BaseMusicClient


class DeezerClient(BaseMusicClient):
    """
    Client for interacting with Deezer's API.
    
    Provides methods to search for songs, fetch playlists, and retrieve
    artist information. No authentication required for basic usage!
    """
    
    BASE_URL = "https://api.deezer.com"
    
    def __init__(self):
        """
        Initialize the Deezer client.
        
        Note: Deezer's public API doesn't require authentication for
        basic search and preview functionality.
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MusicGuessingGame/1.0'
        })
    
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
            List[Dict[str, Any]]: List of normalized track objects with preview URLs
        """
        print(f"🎵 Searching Deezer for {genre} songs...")
        
        try:
            response = self.session.get(
                f"{self.BASE_URL}/search",
                params={'q': genre, 'limit': limit}
            )
            response.raise_for_status()
            data = response.json()
            
            # Filter songs with preview URLs and normalize format
            songs_with_previews = []
            for track in data.get('data', []):
                if self.validate_preview_url(track):
                    normalized = self.normalize_track_format(track)
                    songs_with_previews.append(normalized)
            
            print(f"✓ Found {len(songs_with_previews)} songs with previews")
            return songs_with_previews
            
        except requests.RequestException as e:
            print(f"Error searching Deezer: {e}")
            return []
    
    def get_songs_from_playlist(self, playlist_url: str) -> List[Dict[str, Any]]:
        """
        Get songs from a Deezer playlist URL.
        
        Args:
            playlist_url (str): Full Deezer playlist URL
                              Format: https://www.deezer.com/playlist/{id}
            
        Returns:
            List[Dict[str, Any]]: List of normalized track objects with preview URLs
            
        Raises:
            ValueError: If playlist URL is invalid
        """
        # Extract playlist ID from URL
        # Format: https://www.deezer.com/playlist/{id} or just the ID
        try:
            if 'deezer.com' in playlist_url:
                playlist_id = playlist_url.split('/')[-1].split('?')[0]
            else:
                playlist_id = playlist_url
        except (IndexError, AttributeError):
            raise ValueError(f"Invalid Deezer playlist URL: {playlist_url}")
        
        print(f"🎵 Loading Deezer playlist {playlist_id}...")
        
        try:
            response = self.session.get(f"{self.BASE_URL}/playlist/{playlist_id}")
            response.raise_for_status()
            data = response.json()
            
            songs_with_previews = []
            for track in data.get('tracks', {}).get('data', []):
                if self.validate_preview_url(track):
                    normalized = self.normalize_track_format(track)
                    songs_with_previews.append(normalized)
            
            print(f"✓ Found {len(songs_with_previews)} songs with previews")
            return songs_with_previews
            
        except requests.RequestException as e:
            print(f"Error loading Deezer playlist: {e}")
            return []
    
    def get_top_tracks(
        self, 
        artist_name: str, 
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get top tracks from a specific artist.
        
        Args:
            artist_name (str): Name of the artist to search for
            limit (int): Maximum number of tracks to return (default: 20)
            
        Returns:
            List[Dict[str, Any]]: List of normalized artist's top tracks with preview URLs
            
        Note:
            Returns empty list if artist not found.
        """
        print(f"🎵 Searching Deezer for {artist_name}'s songs...")
        
        try:
            # First, search for the artist
            response = self.session.get(
                f"{self.BASE_URL}/search/artist",
                params={'q': artist_name, 'limit': 1}
            )
            response.raise_for_status()
            data = response.json()
            
            if not data.get('data'):
                print(f"Artist '{artist_name}' not found on Deezer!")
                return []
            
            artist_id = data['data'][0]['id']
            
            # Get artist's top tracks
            response = self.session.get(
                f"{self.BASE_URL}/artist/{artist_id}/top",
                params={'limit': limit}
            )
            response.raise_for_status()
            tracks_data = response.json()
            
            songs_with_previews = []
            for track in tracks_data.get('data', []):
                if self.validate_preview_url(track):
                    normalized = self.normalize_track_format(track)
                    songs_with_previews.append(normalized)
            
            print(f"✓ Found {len(songs_with_previews)} songs with previews")
            return songs_with_previews
            
        except requests.RequestException as e:
            print(f"Error searching Deezer artist: {e}")
            return []
    
    @staticmethod
    def validate_preview_url(track: Dict[str, Any]) -> bool:
        """
        Check if a track has a valid preview URL.
        
        Args:
            track (Dict[str, Any]): Deezer track object
            
        Returns:
            bool: True if preview URL exists and is not empty
        """
        preview_url = track.get('preview')
        return preview_url is not None and preview_url != ""
    
    @staticmethod
    def normalize_track_format(track: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize Deezer track data to common format.
        
        Converts Deezer's track structure to match Spotify's format
        for consistency across the application.
        
        Args:
            track (Dict[str, Any]): Deezer track object
            
        Returns:
            Dict[str, Any]: Normalized track object in Spotify-like format
        """
        # Deezer provides artist info directly in track for search results
        # or as a nested object
        artist_name = "Unknown Artist"
        if 'artist' in track and isinstance(track['artist'], dict):
            artist_name = track['artist'].get('name', 'Unknown Artist')
        elif 'artist' in track:
            artist_name = str(track['artist'])
        
        # Handle album info
        album_name = "Unknown Album"
        release_date = "Unknown"
        if 'album' in track and isinstance(track['album'], dict):
            album_name = track['album'].get('title', 'Unknown Album')
            release_date = track['album'].get('release_date', 'Unknown')
        elif 'album' in track:
            album_name = str(track['album'])
        
        return {
            'id': str(track.get('id', 'unknown')),
            'name': track.get('title', 'Unknown Title'),
            'artists': [{'name': artist_name}],
            'album': {
                'name': album_name,
                'release_date': release_date
            },
            'preview_url': track.get('preview'),
            'provider': 'deezer'  # Tag to identify the source
        }
    
    def get_genre_songs(self, genre_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get songs from a specific Deezer genre.
        
        Deezer has predefined genres with IDs:
        - 0: All
        - 132: Pop
        - 116: Rap/Hip Hop
        - 152: Rock
        - 165: Alternative
        - 85: Dance
        - 113: Electronic
        - 466: Folk
        
        Args:
            genre_id (int): Deezer genre ID
            limit (int): Maximum number of songs to return
            
        Returns:
            List[Dict[str, Any]]: List of normalized track objects
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/genre/{genre_id}/artists",
                params={'limit': 10}  # Get top artists in genre
            )
            response.raise_for_status()
            data = response.json()
            
            all_tracks = []
            for artist in data.get('data', [])[:5]:  # Top 5 artists
                artist_id = artist.get('id')
                tracks_response = self.session.get(
                    f"{self.BASE_URL}/artist/{artist_id}/top",
                    params={'limit': 10}
                )
                if tracks_response.ok:
                    tracks = tracks_response.json().get('data', [])
                    for track in tracks:
                        if self.validate_preview_url(track) and len(all_tracks) < limit:
                            normalized = self.normalize_track_format(track)
                            all_tracks.append(normalized)
            
            return all_tracks
            
        except requests.RequestException as e:
            print(f"Error getting genre songs: {e}")
            return []
