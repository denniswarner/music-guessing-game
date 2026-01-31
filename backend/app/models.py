"""
Pydantic models for API request/response validation.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class MusicProviderCredentials(BaseModel):
    """Music provider API credentials (if needed)."""
    client_id: str = Field(default="", min_length=0)
    client_secret: str = Field(default="", min_length=0)


# Keep for backwards compatibility
SpotifyCredentials = MusicProviderCredentials


class GameStartRequest(BaseModel):
    """Request to start a new game."""
    provider: Literal["spotify", "deezer", "demo", "custom"] = Field(default="demo")
    credentials: MusicProviderCredentials = Field(default_factory=MusicProviderCredentials)
    mode: Literal["genre", "playlist", "artist", "demo", "custom"]
    query: str = Field(default="", min_length=0)
    num_rounds: int = Field(default=10, ge=1, le=50)
    demo_mode: bool = Field(default=False)
    
    # For custom mode
    custom_list_id: Optional[str] = Field(default=None, description="ID of custom song list")
    custom_filters: Optional[dict] = Field(default=None, description="Filters for custom list (decade, genre, style, mood, difficulty)")


class Artist(BaseModel):
    """Artist information."""
    name: str


class Album(BaseModel):
    """Album information."""
    name: str
    release_date: str


class Track(BaseModel):
    """Track/song information."""
    id: str
    name: str
    artists: List[Artist]
    album: Album
    preview_url: Optional[str] = None


class GameSession(BaseModel):
    """Game session information."""
    session_id: str
    total_rounds: int
    current_round: int
    score: float
    songs: List[Track]


class GuessRequest(BaseModel):
    """Player's guess submission."""
    session_id: str
    guess: str
    round_number: int


class GuessResponse(BaseModel):
    """Result of a guess."""
    correct: bool
    points_earned: float
    correct_answer: Optional[str] = None
    artist_hint: Optional[str] = None
    total_score: float
    is_final_guess: bool = False


class GameStats(BaseModel):
    """Final game statistics."""
    total_rounds: int
    score: float
    percentage: float
    rank: str


class SongSearchRequest(BaseModel):
    """Request to search for songs."""
    provider: Literal["spotify", "deezer", "demo", "custom"] = Field(default="demo")
    credentials: MusicProviderCredentials = Field(default_factory=MusicProviderCredentials)
    mode: Literal["genre", "playlist", "artist", "demo", "custom"]
    query: str
    demo_mode: bool = Field(default=False)


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None
