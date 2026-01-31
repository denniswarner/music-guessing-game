"""
Custom Song List Models

Data models for admin-created custom song lists with categorization.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CustomSong(BaseModel):
    """A song in a custom list with metadata."""
    id: str = Field(description="Unique song ID (from provider)")
    name: str = Field(description="Song title")
    artist: str = Field(description="Artist name")
    album: Optional[str] = Field(default=None, description="Album name")
    preview_url: Optional[str] = Field(default=None, description="Audio preview URL")
    
    # Categorization fields
    decade: Optional[str] = Field(default=None, description="e.g., '1980s', '1990s', '2000s'")
    genre: Optional[str] = Field(default=None, description="e.g., 'Rock', 'Pop', 'Jazz'")
    style: Optional[str] = Field(default=None, description="e.g., 'Classic', 'Modern', 'Alternative'")
    mood: Optional[str] = Field(default=None, description="e.g., 'Upbeat', 'Mellow', 'Energetic'")
    difficulty: Optional[str] = Field(default="medium", description="easy, medium, hard")
    
    # Provider info
    provider: str = Field(default="custom", description="Music provider source")
    
    # Additional metadata
    notes: Optional[str] = Field(default=None, description="Admin notes about this song")


class CustomSongList(BaseModel):
    """A curated list of songs for specific audiences."""
    id: str = Field(description="Unique list ID")
    name: str = Field(description="List name (e.g., '80s Rock Night')")
    description: Optional[str] = Field(default=None, description="Description of the list")
    
    # Categorization
    target_audience: Optional[str] = Field(default=None, description="e.g., 'Corporate Event', 'Birthday Party'")
    primary_decade: Optional[str] = Field(default=None, description="Primary decade focus")
    primary_genre: Optional[str] = Field(default=None, description="Primary genre focus")
    
    # Songs in this list
    songs: List[CustomSong] = Field(default_factory=list, description="Songs in this list")
    
    # Metadata
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    created_by: Optional[str] = Field(default="admin", description="Creator username")
    is_active: bool = Field(default=True, description="Whether this list is available for games")
    
    # Usage stats
    times_played: int = Field(default=0, description="How many times this list has been used")


class CreateCustomListRequest(BaseModel):
    """Request to create a new custom song list."""
    name: str
    description: Optional[str] = None
    target_audience: Optional[str] = None
    primary_decade: Optional[str] = None
    primary_genre: Optional[str] = None


class AddSongToListRequest(BaseModel):
    """Request to add a song to a custom list."""
    list_id: str
    song: CustomSong


class SearchSongRequest(BaseModel):
    """Request to search for songs to add to a list."""
    provider: str = Field(description="spotify, deezer, or demo")
    query: str = Field(description="Search query")
    mode: str = Field(default="genre", description="genre, artist, or playlist")


class FilterCustomListRequest(BaseModel):
    """Request to filter songs from a custom list."""
    list_id: str
    decade: Optional[str] = None
    genre: Optional[str] = None
    style: Optional[str] = None
    mood: Optional[str] = None
    difficulty: Optional[str] = None
    limit: Optional[int] = Field(default=None, description="Max songs to return")


class CustomListSummary(BaseModel):
    """Summary of a custom list (without full song details)."""
    id: str
    name: str
    description: Optional[str]
    target_audience: Optional[str]
    primary_decade: Optional[str]
    primary_genre: Optional[str]
    song_count: int
    created_at: str
    updated_at: str
    times_played: int
    is_active: bool
