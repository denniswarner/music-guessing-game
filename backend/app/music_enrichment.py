"""
Local Music Enrichment

Smart metadata enrichment without requiring external APIs.
Uses artist/track name patterns and release year to suggest categories.
"""

from typing import Dict, Optional
import re


class LocalMusicEnricher:
    """
    Enrich song metadata using local knowledge and patterns.
    No external API required!
    """
    
    # Artist -> Genre mapping (expand as needed)
    ARTIST_GENRES = {
        # Rock
        'queen': 'Rock',
        'led zeppelin': 'Rock',
        'the beatles': 'Rock',
        'the rolling stones': 'Rock',
        'pink floyd': 'Rock',
        'u2': 'Rock',
        'foo fighters': 'Rock',
        
        # Pop
        'madonna': 'Pop',
        'michael jackson': 'Pop',
        'britney spears': 'Pop',
        'taylor swift': 'Pop',
        'ariana grande': 'Pop',
        'ed sheeran': 'Pop',
        
        # Hip Hop
        'drake': 'Hip Hop',
        'kendrick lamar': 'Hip Hop',
        'kanye west': 'Hip Hop',
        'jay-z': 'Hip Hop',
        'eminem': 'Hip Hop',
        'tupac': 'Hip Hop',
        'notorious b.i.g.': 'Hip Hop',
        
        # R&B
        'beyonce': 'R&B',
        'usher': 'R&B',
        'alicia keys': 'R&B',
        'john legend': 'R&B',
        'marvin gaye': 'R&B',
        'stevie wonder': 'R&B',
        
        # Electronic
        'daft punk': 'Electronic',
        'deadmau5': 'Electronic',
        'calvin harris': 'Electronic',
        'the chainsmokers': 'Electronic',
        'avicii': 'Electronic',
        
        # Country
        'johnny cash': 'Country',
        'dolly parton': 'Country',
        'garth brooks': 'Country',
        'shania twain': 'Country',
        'luke bryan': 'Country',
        
        # Jazz
        'miles davis': 'Jazz',
        'john coltrane': 'Jazz',
        'ella fitzgerald': 'Jazz',
        'louis armstrong': 'Jazz',
        'duke ellington': 'Jazz',
        
        # Ska/Reggae
        'the english beat': 'Pop',  # 2-Tone Ska band, but Pop is closer than Reggae
        'the beat': 'Pop',
        'the specials': 'Pop',
        'madness': 'Pop',
        'bob marley': 'Reggae',
        'peter tosh': 'Reggae',
    }
    
    # Genre keywords in artist names
    GENRE_KEYWORDS = {
        'rock': ['rock', 'metal', 'punk'],
        'pop': ['pop', 'boy band', 'girl group'],
        'hip hop': ['hip hop', 'rapper', 'mc'],
        'electronic': ['electronic', 'techno', 'house', 'edm', 'dj'],
        'country': ['country', 'bluegrass'],
        'jazz': ['jazz', 'swing', 'big band'],
        'classical': ['orchestra', 'philharmonic', 'symphony', 'quartet'],
        'r&b': ['r&b', 'soul', 'funk'],
    }
    
    # Track name -> Mood mapping
    # Note: Only match if context makes sense - some songs have misleading titles!
    MOOD_KEYWORDS = {
        'upbeat': ['party', 'celebrate', 'dance', 'fun', 'yeah', 'tonight', 'shake'],
        'happy': ['happy', 'joy', 'smile', 'sunshine', 'good time', 'great'],
        'sad': ['goodbye', 'miss you', 'broken', 'empty', 'lost you'],
        'romantic': ['love', 'heart', 'baby', 'kiss', 'beautiful', 'forever', 'you and me'],
        'energetic': ['power', 'energy', 'fire', 'electric', 'wild', 'crazy', 'go'],
        'chill': ['easy', 'slow', 'mellow', 'calm', 'peace', 'relax', 'breeze'],
        'party': ['party', 'club', 'night out', 'weekend', 'get down'],
        'melancholic': ['rain', 'dark', 'cold', 'alone'],
    }
    
    # Songs that are actually upbeat despite sad-sounding titles
    UPBEAT_EXCEPTIONS = [
        'tears of a clown',  # The English Beat - upbeat ska
        'dancing on my own',  # Upbeat despite being about loneliness
        'everybody hurts',    # R.E.M. - actually uplifting
    ]
    
    def enrich_song_metadata(
        self, 
        artist: str, 
        track: str, 
        release_year: Optional[int] = None
    ) -> Dict[str, Optional[str]]:
        """
        Enrich song with metadata using local patterns.
        
        Args:
            artist: Artist name
            track: Track name
            release_year: Optional release year
            
        Returns:
            Dictionary with genre, mood, style suggestions
        """
        artist_lower = artist.lower()
        track_lower = track.lower()
        
        # Extract genre
        genre = self._extract_genre(artist_lower)
        
        # Extract mood
        mood = self._extract_mood(track_lower, artist_lower)
        
        # Extract style
        style = self._extract_style(release_year, genre)
        
        # Generate descriptive tags
        tags = []
        if genre:
            tags.append(genre.lower())
        if mood:
            tags.append(mood.lower())
        if style:
            tags.append(style.lower())
        if release_year:
            decade = (release_year // 10) * 10
            tags.append(f"{decade}s")
        
        return {
            'genre': genre,
            'mood': mood,
            'style': style,
            'tags': tags[:5]
        }
    
    def _extract_genre(self, artist_lower: str) -> Optional[str]:
        """Extract genre from artist name."""
        # Check exact match
        if artist_lower in self.ARTIST_GENRES:
            return self.ARTIST_GENRES[artist_lower]
        
        # Check for keywords
        for genre, keywords in self.GENRE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in artist_lower:
                    return genre.title()
        
        return None
    
    def _extract_mood(self, track_lower: str, artist_lower: str) -> Optional[str]:
        """Extract mood from track name."""
        # Check for upbeat exceptions first (songs that sound upbeat despite sad titles)
        for exception in self.UPBEAT_EXCEPTIONS:
            if exception in track_lower:
                return 'Upbeat'
        
        # Then check other mood keywords
        for mood, keywords in self.MOOD_KEYWORDS.items():
            for keyword in keywords:
                if keyword in track_lower:
                    return mood.title()
        
        return None
    
    def _extract_style(
        self, 
        release_year: Optional[int], 
        genre: Optional[str]
    ) -> Optional[str]:
        """Extract style from release year and genre."""
        if not release_year:
            return None
        
        # Year-based style
        if release_year < 1970:
            return 'Classic'
        elif release_year < 1990:
            return 'Classic'
        elif release_year < 2010:
            return 'Modern'
        else:
            return 'Contemporary'


# Global instance
local_enricher = LocalMusicEnricher()
