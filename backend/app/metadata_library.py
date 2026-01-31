"""
Metadata Library Manager

Manages user's personal song metadata database.
Learns from manual entries and provides intelligent suggestions.
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from collections import Counter


class MetadataLibrary:
    """
    User's personal song metadata library.
    
    Stores metadata for songs that have been manually categorized,
    enabling auto-population and consistency across lists.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize metadata library.
        
        Args:
            data_dir: Directory to store library data
        """
        self.data_dir = data_dir
        self.library_path = os.path.join(data_dir, "metadata_library.json")
        self.library = self._load_library()
    
    def _load_library(self) -> Dict[str, Any]:
        """Load library from disk or create new one."""
        if os.path.exists(self.library_path):
            try:
                with open(self.library_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading metadata library: {e}")
                return self._create_empty_library()
        else:
            return self._create_empty_library()
    
    def _create_empty_library(self) -> Dict[str, Any]:
        """Create empty library structure."""
        return {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "songs": {},
            "statistics": {
                "total_songs": 0,
                "total_artists": 0,
                "last_updated": datetime.now().isoformat()
            }
        }
    
    def _save_library(self):
        """Save library to disk."""
        try:
            # Ensure directory exists
            os.makedirs(self.data_dir, exist_ok=True)
            
            # Update statistics
            self._update_statistics()
            
            # Save to file
            with open(self.library_path, 'w', encoding='utf-8') as f:
                json.dump(self.library, f, indent=2, ensure_ascii=False)
                
            print(f"Metadata library saved: {len(self.library['songs'])} songs")
            
        except Exception as e:
            print(f"Error saving metadata library: {e}")
            raise
    
    def _update_statistics(self):
        """Update library statistics."""
        songs = self.library.get('songs', {})
        artists = set(song.get('artist', '').lower() for song in songs.values())
        
        self.library['statistics'] = {
            "total_songs": len(songs),
            "total_artists": len(artists),
            "last_updated": datetime.now().isoformat()
        }
    
    def _make_song_key(self, song_id: str, provider: str) -> str:
        """Create unique key for song."""
        return f"{provider}_{song_id}"
    
    def get_song_metadata(self, song_id: str, provider: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a song if it exists in library.
        
        Args:
            song_id: Song ID from provider
            provider: Music provider (deezer, spotify, etc.)
            
        Returns:
            Song metadata if found, None otherwise
        """
        key = self._make_song_key(song_id, provider)
        return self.library.get('songs', {}).get(key)
    
    def save_song_metadata(
        self,
        song_id: str,
        provider: str,
        name: str,
        artist: str,
        album: Optional[str],
        release_date: Optional[str],
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Save song metadata to library.
        
        Args:
            song_id: Song ID from provider
            provider: Music provider
            name: Song name
            artist: Artist name
            album: Album name
            release_date: Release date
            metadata: User-provided metadata (genre, mood, style, etc.)
            
        Returns:
            Saved song entry
        """
        key = self._make_song_key(song_id, provider)
        
        # Check if song already exists
        existing = self.library['songs'].get(key)
        
        song_entry = {
            'id': song_id,
            'provider': provider,
            'name': name,
            'artist': artist,
            'album': album,
            'release_date': release_date,
            'metadata': {
                'decade': metadata.get('decade'),
                'genre': metadata.get('genre'),
                'style': metadata.get('style'),
                'mood': metadata.get('mood'),
                'difficulty': metadata.get('difficulty'),
                'notes': metadata.get('notes', '')
            },
            'added_date': existing.get('added_date') if existing else datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'times_used': existing.get('times_used', 0) + 1 if existing else 1
        }
        
        self.library['songs'][key] = song_entry
        self._save_library()
        
        return song_entry
    
    def search_by_artist(self, artist_name: str) -> List[Dict[str, Any]]:
        """
        Find all songs by an artist in the library.
        
        Args:
            artist_name: Artist name to search for
            
        Returns:
            List of songs by this artist
        """
        artist_lower = artist_name.lower()
        matching_songs = []
        
        for song in self.library.get('songs', {}).values():
            if song.get('artist', '').lower() == artist_lower:
                matching_songs.append(song)
        
        return matching_songs
    
    def get_artist_suggestions(self, artist_name: str) -> Dict[str, Any]:
        """
        Get metadata suggestions based on user's history with this artist.
        
        Args:
            artist_name: Artist name
            
        Returns:
            Suggested metadata based on most common values
        """
        songs = self.search_by_artist(artist_name)
        
        if not songs:
            return {
                'found': False,
                'count': 0
            }
        
        # Collect metadata from all songs by this artist
        genres = [s['metadata'].get('genre') for s in songs if s['metadata'].get('genre')]
        styles = [s['metadata'].get('style') for s in songs if s['metadata'].get('style')]
        moods = [s['metadata'].get('mood') for s in songs if s['metadata'].get('mood')]
        
        # Find most common values
        genre_counts = Counter(genres)
        style_counts = Counter(styles)
        mood_counts = Counter(moods)
        
        return {
            'found': True,
            'count': len(songs),
            'songs': songs,
            'suggestions': {
                'genre': genre_counts.most_common(1)[0][0] if genre_counts else None,
                'style': style_counts.most_common(1)[0][0] if style_counts else None,
                'mood': mood_counts.most_common(1)[0][0] if mood_counts else None,
            },
            'genre_distribution': dict(genre_counts),
            'style_distribution': dict(style_counts),
            'mood_distribution': dict(mood_counts)
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive library statistics.
        
        Returns:
            Dictionary with library statistics
        """
        songs = self.library.get('songs', {})
        
        if not songs:
            return {
                'total_songs': 0,
                'total_artists': 0,
                'genres': {},
                'styles': {},
                'moods': {},
                'decades': {},
                'top_artists': []
            }
        
        # Collect metadata
        artists = [s.get('artist') for s in songs.values()]
        genres = [s['metadata'].get('genre') for s in songs.values() if s['metadata'].get('genre')]
        styles = [s['metadata'].get('style') for s in songs.values() if s['metadata'].get('style')]
        moods = [s['metadata'].get('mood') for s in songs.values() if s['metadata'].get('mood')]
        decades = [s['metadata'].get('decade') for s in songs.values() if s['metadata'].get('decade')]
        
        # Count occurrences
        artist_counts = Counter(artists)
        genre_counts = Counter(genres)
        style_counts = Counter(styles)
        mood_counts = Counter(moods)
        decade_counts = Counter(decades)
        
        return {
            'total_songs': len(songs),
            'total_artists': len(set(artists)),
            'genres': dict(genre_counts),
            'styles': dict(style_counts),
            'moods': dict(mood_counts),
            'decades': dict(decade_counts),
            'top_artists': [
                {'artist': artist, 'count': count}
                for artist, count in artist_counts.most_common(10)
            ],
            'most_common_genre': genre_counts.most_common(1)[0] if genre_counts else None,
            'most_common_decade': decade_counts.most_common(1)[0] if decade_counts else None,
            'last_updated': self.library.get('statistics', {}).get('last_updated')
        }
    
    def get_all_songs(self) -> List[Dict[str, Any]]:
        """Get all songs in the library."""
        return list(self.library.get('songs', {}).values())
    
    def export_library(self) -> Dict[str, Any]:
        """Export entire library."""
        return self.library
    
    def import_library(self, data: Dict[str, Any]) -> int:
        """
        Import library data (merge with existing).
        
        Args:
            data: Library data to import
            
        Returns:
            Number of songs imported
        """
        imported_count = 0
        
        for key, song in data.get('songs', {}).items():
            # Only import if not already present or if newer
            existing = self.library['songs'].get(key)
            
            if not existing or song.get('last_updated', '') > existing.get('last_updated', ''):
                self.library['songs'][key] = song
                imported_count += 1
        
        self._save_library()
        return imported_count


# Global instance
metadata_library = MetadataLibrary()
