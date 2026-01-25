"""
Game Session Manager

Manages active game sessions with in-memory storage.
"""

import uuid
from typing import Dict, Optional
from datetime import datetime, timedelta

import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.spotify_client import SpotifyClient
from src.game_engine import GameEngine
from app.models import Track, Artist, Album


class GameSessionData:
    """Data for an active game session."""
    
    def __init__(
        self, 
        session_id: str, 
        spotify_client: SpotifyClient,
        game_engine: GameEngine,
        songs: list,
        total_rounds: int
    ):
        self.session_id = session_id
        self.spotify_client = spotify_client
        self.game_engine = game_engine
        self.songs = songs
        self.total_rounds = total_rounds
        self.current_round = 0
        self.current_song = None
        self.first_guess_made = False
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
    
    def update_activity(self):
        """Update last activity timestamp."""
        self.last_activity = datetime.now()
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """Check if session has expired."""
        return datetime.now() - self.last_activity > timedelta(minutes=timeout_minutes)


class GameSessionManager:
    """Manages all active game sessions."""
    
    def __init__(self):
        self.sessions: Dict[str, GameSessionData] = {}
    
    def create_session(
        self,
        client_id: str,
        client_secret: str,
        songs: list,
        total_rounds: int
    ) -> str:
        """
        Create a new game session.
        
        Args:
            client_id: Spotify API client ID
            client_secret: Spotify API client secret
            songs: List of songs for the game
            total_rounds: Number of rounds to play
            
        Returns:
            str: Session ID
        """
        session_id = str(uuid.uuid4())
        
        # Initialize components
        spotify_client = SpotifyClient(client_id, client_secret)
        game_engine = GameEngine()
        
        # Create session
        session = GameSessionData(
            session_id=session_id,
            spotify_client=spotify_client,
            game_engine=game_engine,
            songs=songs[:total_rounds],
            total_rounds=total_rounds
        )
        
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> Optional[GameSessionData]:
        """Get session by ID."""
        session = self.sessions.get(session_id)
        if session:
            session.update_activity()
        return session
    
    def delete_session(self, session_id: str):
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def cleanup_expired_sessions(self, timeout_minutes: int = 30):
        """Remove expired sessions."""
        expired = [
            sid for sid, session in self.sessions.items()
            if session.is_expired(timeout_minutes)
        ]
        for sid in expired:
            del self.sessions[sid]
    
    def convert_track_to_model(self, track: dict) -> Track:
        """Convert Spotify track dict to Pydantic model."""
        return Track(
            id=track.get('id', ''),
            name=track['name'],
            artists=[Artist(name=a['name']) for a in track['artists']],
            album=Album(
                name=track['album']['name'],
                release_date=track['album']['release_date']
            ),
            preview_url=track.get('preview_url')
        )


# Global session manager instance
session_manager = GameSessionManager()
