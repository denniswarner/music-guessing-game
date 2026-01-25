"""
Songs API Routes

Endpoints for searching and retrieving songs from Spotify.
"""

from fastapi import APIRouter, HTTPException
from typing import List
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.spotify_client import SpotifyClient
from app.models import Track, SongSearchRequest, ErrorResponse
from app.game_manager import session_manager

router = APIRouter()


@router.post("/search", response_model=List[Track])
async def search_songs(request: SongSearchRequest):
    """
    Search for songs based on mode and query.
    
    Args:
        request: Search parameters including credentials, mode, and query
        
    Returns:
        List[Track]: List of available tracks
        
    Raises:
        HTTPException: If search fails or no songs found
    """
    try:
        # Initialize Spotify client
        spotify_client = SpotifyClient(
            request.credentials.client_id,
            request.credentials.client_secret
        )
        
        # Search based on mode
        if request.mode == "genre":
            songs = spotify_client.get_songs_by_genre(request.query)
        elif request.mode == "playlist":
            songs = spotify_client.get_songs_from_playlist(request.query)
        elif request.mode == "artist":
            songs = spotify_client.get_top_tracks(request.query)
        else:
            raise HTTPException(status_code=400, detail="Invalid search mode")
        
        if not songs:
            raise HTTPException(
                status_code=404,
                detail=f"No songs with preview URLs found for '{request.query}'"
            )
        
        # Convert to Track models
        tracks = [session_manager.convert_track_to_model(song) for song in songs]
        
        return tracks
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/preview/{track_id}")
async def get_preview_url(track_id: str):
    """
    Get preview URL for a specific track.
    
    Args:
        track_id: Spotify track ID
        
    Returns:
        dict: Preview URL information
    """
    # Note: In production, you'd fetch this from Spotify
    # For now, this is handled client-side
    return {"track_id": track_id}
