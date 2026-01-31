"""
MusicBrainz API Client

Enriches song metadata with genre, mood, and style information from MusicBrainz.
No API key required! Free and open source music database.
"""

import requests
from typing import Dict, List, Optional
import time


class MusicBrainzClient:
    """
    Client for MusicBrainz API to get rich music metadata.
    
    No API key required! Completely free and open.
    https://musicbrainz.org/doc/MusicBrainz_API
    """
    
    BASE_URL = "https://musicbrainz.org/ws/2"
    
    # User agent is required by MusicBrainz
    USER_AGENT = "MusicGuessingGame/1.0 (https://github.com/yourusername/music-game)"
    
    def __init__(self):
        """Initialize MusicBrainz client. No API key needed!"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.USER_AGENT,
            'Accept': 'application/json'
        })
        self.last_request_time = 0
        self.rate_limit_delay = 1.0  # MusicBrainz requires 1 request per second
    
    def _rate_limit(self):
        """Enforce MusicBrainz rate limit of 1 request per second."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: dict) -> Optional[dict]:
        """Make a request to MusicBrainz API."""
        self._rate_limit()
        
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"MusicBrainz API error: {e}")
            return None
    
    def search_recording(self, artist: str, track: str) -> Optional[Dict]:
        """
        Search for a recording (track) on MusicBrainz.
        
        Args:
            artist: Artist name
            track: Track name
            
        Returns:
            Recording info or None if not found
        """
        # Build search query
        query = f'recording:"{track}" AND artist:"{artist}"'
        
        data = self._make_request('recording', {
            'query': query,
            'fmt': 'json',
            'limit': 1
        })
        
        if data and 'recordings' in data and len(data['recordings']) > 0:
            return data['recordings'][0]
        return None
    
    def get_artist_info(self, artist_name: str) -> Optional[Dict]:
        """
        Search for an artist on MusicBrainz.
        
        Args:
            artist_name: Artist name
            
        Returns:
            Artist info or None if not found
        """
        data = self._make_request('artist', {
            'query': f'artist:"{artist_name}"',
            'fmt': 'json',
            'limit': 1
        })
        
        if data and 'artists' in data and len(data['artists']) > 0:
            artist = data['artists'][0]
            artist_id = artist.get('id')
            
            if artist_id:
                # Get full artist details with tags and genres
                artist_details = self._make_request(f'artist/{artist_id}', {
                    'inc': 'tags+genres',
                    'fmt': 'json'
                })
                return artist_details
        
        return None
    
    def extract_tags_from_artist(self, artist_data: Optional[Dict]) -> List[str]:
        """
        Extract tags and genres from artist data.
        
        Args:
            artist_data: Artist data from MusicBrainz
            
        Returns:
            List of tag/genre names
        """
        tags = []
        
        if not artist_data:
            return tags
        
        # Get genres (more reliable than tags)
        if 'genres' in artist_data and artist_data['genres']:
            genres = artist_data['genres']
            sorted_genres = sorted(genres, key=lambda x: x.get('count', 0), reverse=True)
            tags.extend([g['name'] for g in sorted_genres[:5]])
        
        # Get tags
        if 'tags' in artist_data and artist_data['tags']:
            tag_list = artist_data['tags']
            sorted_tags = sorted(tag_list, key=lambda x: x.get('count', 0), reverse=True)
            tags.extend([t['name'] for t in sorted_tags[:5]])
        
        return tags[:10]  # Return top 10 combined
    
    def enrich_song_metadata(self, artist: str, track: str, release_year: Optional[int] = None) -> Dict[str, Optional[str]]:
        """
        Enrich song with metadata from MusicBrainz.
        
        Uses artist genres/tags since MusicBrainz has better artist-level metadata.
        
        Args:
            artist: Artist name
            track: Track name
            release_year: Optional release year for better decade detection
            
        Returns:
            Dictionary with genre, mood, style suggestions
        """
        try:
            # Get artist information (has better genre/tag data)
            artist_data = self.get_artist_info(artist)
            
            if not artist_data:
                print(f"Artist not found: {artist}")
                return self._fallback_metadata(release_year)
            
            # Extract tags/genres from artist
            tags = self.extract_tags_from_artist(artist_data)
            tags_lower = [tag.lower().replace('_', ' ') for tag in tags]
            
            # Map tags to our categories
            genre = self._extract_genre(tags_lower)
            mood = self._extract_mood(tags_lower)
            style = self._extract_style(tags_lower, release_year)
            
            return {
                'genre': genre,
                'mood': mood,
                'style': style,
                'tags': tags[:5]  # Return top 5 tags for reference
            }
            
        except Exception as e:
            print(f"MusicBrainz enrichment error: {e}")
            return self._fallback_metadata(release_year)
    
    def _fallback_metadata(self, release_year: Optional[int] = None) -> Dict[str, Optional[str]]:
        """Return fallback metadata when MusicBrainz doesn't have data."""
        style = None
        if release_year:
            if release_year < 1980:
                style = 'Classic'
            elif release_year < 2010:
                style = 'Modern'
            else:
                style = 'Contemporary'
        
        return {
            'genre': None,
            'mood': None,
            'style': style,
            'tags': []
        }
    
    def _extract_genre(self, tags: List[str]) -> Optional[str]:
        """Extract genre from MusicBrainz tags."""
        # Map MusicBrainz tags to our genre categories
        genre_map = {
            'rock': 'Rock',
            'pop': 'Pop',
            'hip hop': 'Hip Hop',
            'hip-hop': 'Hip Hop',
            'rap': 'Hip Hop',
            'rnb': 'R&B',
            'r&b': 'R&B',
            'jazz': 'Jazz',
            'country': 'Country',
            'electronic': 'Electronic',
            'edm': 'Electronic',
            'dance': 'Electronic',
            'classical': 'Classical',
            'blues': 'Blues',
            'metal': 'Metal',
            'heavy metal': 'Metal',
            'folk': 'Folk',
            'reggae': 'Reggae',
            'latin': 'Latin',
            'soul': 'Soul',
            'funk': 'Funk',
            'disco': 'Disco',
            'punk': 'Punk',
            'indie': 'Indie',
            'alternative': 'Alternative',
            'alternative rock': 'Alternative'
        }
        
        for tag in tags:
            if tag in genre_map:
                return genre_map[tag]
        
        return None
    
    def _extract_mood(self, tags: List[str]) -> Optional[str]:
        """Extract mood from MusicBrainz tags."""
        # Map MusicBrainz tags to our mood categories
        mood_map = {
            'upbeat': 'Upbeat',
            'happy': 'Happy',
            'energetic': 'Energetic',
            'party': 'Party',
            'chill': 'Chill',
            'chillout': 'Chill',
            'relaxing': 'Relaxing',
            'mellow': 'Mellow',
            'sad': 'Sad',
            'melancholy': 'Melancholic',
            'melancholic': 'Melancholic',
            'romantic': 'Romantic',
            'love': 'Romantic',
            'intense': 'Intense',
            'aggressive': 'Intense',
            'motivational': 'Motivational',
            'inspirational': 'Motivational'
        }
        
        for tag in tags:
            if tag in mood_map:
                return mood_map[tag]
        
        return None
    
    def _extract_style(self, tags: List[str], release_year: Optional[int] = None) -> Optional[str]:
        """Extract style from MusicBrainz tags and release year."""
        # Check tags first
        style_map = {
            'classic': 'Classic',
            'oldies': 'Classic',
            'vintage': 'Classic',
            'modern': 'Modern',
            'contemporary': 'Contemporary',
            'alternative': 'Alternative',
            'mainstream': 'Mainstream',
            'indie': 'Underground',
            'underground': 'Underground',
            'experimental': 'Experimental',
            'traditional': 'Traditional'
        }
        
        for tag in tags:
            if tag in style_map:
                return style_map[tag]
        
        # Fall back to year-based logic
        if release_year:
            if release_year < 1980:
                return 'Classic'
            elif release_year < 2010:
                return 'Modern'
            else:
                return 'Contemporary'
        
        return None


# Global instance
musicbrainz_client = MusicBrainzClient()
