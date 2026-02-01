"""
Admin API Routes

API endpoints for managing custom song lists (admin features).
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
import random

from app.custom_lists_models import (
    CustomSongList, CustomSong, CustomListSummary,
    CreateCustomListRequest, AddSongToListRequest,
    SearchSongRequest, FilterCustomListRequest,
    GuestSubmissionRequest
)
from app.custom_list_manager import custom_list_manager
from app.metadata_library import metadata_library
from app.music_enrichment import local_enricher
from src.spotify_client import SpotifyClient
from src.deezer_client import DeezerClient

router = APIRouter()


@router.get("/lists", response_model=List[CustomListSummary])
async def list_all_custom_lists(active_only: bool = False):
    """
    Get all custom song lists (summaries).
    
    Args:
        active_only: Only return active lists
        
    Returns:
        List of custom list summaries
    """
    try:
        summaries = custom_list_manager.list_all_summaries(active_only=active_only)
        return summaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list custom lists: {str(e)}")


@router.post("/lists", response_model=CustomSongList)
async def create_custom_list(request: CreateCustomListRequest):
    """
    Create a new custom song list.
    
    Args:
        request: List creation parameters
        
    Returns:
        The created custom list
    """
    try:
        custom_list = custom_list_manager.create_list(
            name=request.name,
            description=request.description,
            target_audience=request.target_audience,
            primary_decade=request.primary_decade,
            primary_genre=request.primary_genre
        )
        return custom_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create list: {str(e)}")


@router.get("/lists/{list_id}", response_model=CustomSongList)
async def get_custom_list(list_id: str):
    """
    Get a custom list by ID (with full song details).
    
    Args:
        list_id: List ID
        
    Returns:
        The custom list
    """
    custom_list = custom_list_manager.get_list(list_id)
    if not custom_list:
        raise HTTPException(status_code=404, detail="Custom list not found")
    return custom_list


@router.put("/lists/{list_id}", response_model=CustomSongList)
async def update_custom_list(
    list_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    target_audience: Optional[str] = None,
    primary_decade: Optional[str] = None,
    primary_genre: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """
    Update a custom list's metadata.
    
    Args:
        list_id: List ID
        name: New name (optional)
        description: New description (optional)
        target_audience: New target audience (optional)
        primary_decade: New primary decade (optional)
        primary_genre: New primary genre (optional)
        is_active: New active status (optional)
        
    Returns:
        Updated custom list
    """
    custom_list = custom_list_manager.update_list(
        list_id=list_id,
        name=name,
        description=description,
        target_audience=target_audience,
        primary_decade=primary_decade,
        primary_genre=primary_genre,
        is_active=is_active
    )
    
    if not custom_list:
        raise HTTPException(status_code=404, detail="Custom list not found")
    
    return custom_list


@router.delete("/lists/{list_id}")
async def delete_custom_list(list_id: str):
    """
    Delete a custom list.
    
    Args:
        list_id: List ID
        
    Returns:
        Success message
    """
    success = custom_list_manager.delete_list(list_id)
    if not success:
        raise HTTPException(status_code=404, detail="Custom list not found")
    
    return {"message": "List deleted successfully"}


@router.post("/lists/{list_id}/songs", response_model=CustomSongList)
async def add_song_to_list(list_id: str, song: CustomSong):
    """
    Add a song to a custom list.
    
    Args:
        list_id: List ID
        song: Song to add
        
    Returns:
        Updated custom list
    """
    custom_list = custom_list_manager.add_song(list_id, song)
    if not custom_list:
        raise HTTPException(status_code=404, detail="Custom list not found")
    
    return custom_list


@router.delete("/lists/{list_id}/songs/{song_id}", response_model=CustomSongList)
async def remove_song_from_list(list_id: str, song_id: str):
    """
    Remove a song from a custom list.
    
    Args:
        list_id: List ID
        song_id: Song ID to remove
        
    Returns:
        Updated custom list
    """
    custom_list = custom_list_manager.remove_song(list_id, song_id)
    if not custom_list:
        raise HTTPException(status_code=404, detail="Custom list not found")
    
    return custom_list


@router.post("/lists/filter", response_model=List[CustomSong])
async def filter_custom_list_songs(request: FilterCustomListRequest):
    """
    Filter songs from a custom list by criteria.
    
    Args:
        request: Filter parameters
        
    Returns:
        Filtered list of songs
    """
    songs = custom_list_manager.filter_songs(
        list_id=request.list_id,
        decade=request.decade,
        genre=request.genre,
        style=request.style,
        mood=request.mood,
        difficulty=request.difficulty,
        limit=request.limit
    )
    return songs


@router.post("/search-songs", response_model=List[dict])
async def search_songs_for_admin(request: SearchSongRequest):
    """
    Search for songs from a provider to add to a custom list.
    
    This endpoint helps admins find songs to add to their lists.
    
    Args:
        request: Search parameters
        
    Returns:
        List of songs found
    """
    try:
        songs = []
        
        if request.provider == "deezer":
            client = DeezerClient()
            if request.mode == "genre":
                songs = client.get_songs_by_genre(request.query, limit=25)
            elif request.mode == "artist":
                songs = client.get_top_tracks(request.query, limit=25)
        
        elif request.provider == "spotify":
            # Spotify requires credentials - they should be in env or provided
            # For now, return an error asking for credentials
            raise HTTPException(
                status_code=400,
                detail="Spotify search requires credentials. Use Deezer instead or implement credential passing."
            )
        
        elif request.provider == "demo":
            # Return demo songs
            from app.mock_data import MOCK_SONGS
            songs = MOCK_SONGS
        
        return songs
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/categories/decades", response_model=List[str])
async def get_decades():
    """Get list of available decades for categorization."""
    return [
        "1950s", "1960s", "1970s", "1980s", "1990s",
        "2000s", "2010s", "2020s"
    ]


@router.get("/categories/genres", response_model=List[str])
async def get_genres():
    """Get list of common genres for categorization."""
    return [
        "Rock", "Pop", "Hip Hop", "R&B", "Jazz",
        "Country", "Electronic", "Classical", "Blues",
        "Metal", "Folk", "Reggae", "Latin", "Soul",
        "Funk", "Disco", "Punk", "Indie", "Alternative"
    ]


@router.get("/categories/styles", response_model=List[str])
async def get_styles():
    """Get list of common styles for categorization."""
    return [
        "Classic", "Modern", "Alternative", "Mainstream",
        "Underground", "Experimental", "Traditional", "Contemporary"
    ]


@router.get("/categories/moods", response_model=List[str])
async def get_moods():
    """Get list of common moods for categorization."""
    return [
        "Upbeat", "Mellow", "Energetic", "Relaxing",
        "Happy", "Sad", "Romantic", "Party", "Chill",
        "Intense", "Melancholic", "Motivational"
    ]


# ============================================================================
# Metadata Library Endpoints
# ============================================================================

@router.get("/library/song/{provider}/{song_id}")
async def get_library_song(provider: str, song_id: str):
    """
    Check if a song exists in user's metadata library.
    
    Args:
        provider: Music provider (deezer, spotify, etc.)
        song_id: Song ID from provider
        
    Returns:
        Song metadata if found, or not_found status
    """
    metadata = metadata_library.get_song_metadata(song_id, provider)
    
    if metadata:
        return {
            "found": True,
            "song": metadata
        }
    
    return {
        "found": False
    }


@router.post("/library/song")
async def save_library_song(
    song_id: str,
    provider: str,
    name: str,
    artist: str,
    album: Optional[str] = None,
    release_date: Optional[str] = None,
    decade: Optional[str] = None,
    genre: Optional[str] = None,
    style: Optional[str] = None,
    mood: Optional[str] = None,
    difficulty: Optional[str] = None,
    notes: Optional[str] = None
):
    """
    Save song metadata to user's library.
    
    This is called when a song is added to a custom list,
    storing the metadata for future auto-population.
    """
    metadata = {
        'decade': decade,
        'genre': genre,
        'style': style,
        'mood': mood,
        'difficulty': difficulty,
        'notes': notes
    }
    
    saved_song = metadata_library.save_song_metadata(
        song_id=song_id,
        provider=provider,
        name=name,
        artist=artist,
        album=album,
        release_date=release_date,
        metadata=metadata
    )
    
    return {
        "success": True,
        "song": saved_song
    }


@router.get("/library/artist/{artist_name}")
async def get_artist_suggestions(artist_name: str):
    """
    Get metadata suggestions based on user's history with this artist.
    
    Returns songs by this artist and suggested metadata based on
    most common values from previous entries.
    """
    suggestions = metadata_library.get_artist_suggestions(artist_name)
    return suggestions


@router.get("/library/stats")
async def get_library_statistics():
    """
    Get comprehensive statistics about user's metadata library.
    
    Returns:
        Statistics including song count, genres, artists, etc.
    """
    stats = metadata_library.get_statistics()
    return stats


@router.get("/library/songs")
async def get_all_library_songs():
    """Get all songs in user's metadata library."""
    songs = metadata_library.get_all_songs()
    return {
        "songs": songs,
        "count": len(songs)
    }


@router.get("/library/export")
async def export_library():
    """Export user's entire metadata library."""
    library_data = metadata_library.export_library()
    return library_data


@router.post("/library/import")
async def import_library(data: dict):
    """
    Import metadata library data (merges with existing).
    
    Args:
        data: Library data to import
        
    Returns:
        Number of songs imported
    """
    imported_count = metadata_library.import_library(data)
    return {
        "success": True,
        "imported_count": imported_count
    }


# ============================================================================
# Enrichment Endpoint
# ============================================================================

@router.post("/enrich-song", response_model=dict)
async def enrich_song_metadata(
    artist: str,
    track: str,
    release_year: Optional[int] = None
):
    """
    Enrich song metadata using local music knowledge.
    
    Gets genre, mood, and style suggestions based on artist/track patterns.
    No external API or API key required!
    
    Args:
        artist: Artist name
        track: Track name
        release_year: Optional release year
        
    Returns:
        Dictionary with suggested metadata
    """
    try:
        enriched = local_enricher.enrich_song_metadata(artist, track, release_year)
        return {
            "success": True,
            "data": enriched
        }
    except Exception as e:
        # Don't fail the request if enrichment fails
        print(f"Enrichment failed: {e}")
        return {
            "success": False,
            "data": {
                "genre": None,
                "mood": None,
                "style": None,
                "tags": []
            },
            "error": str(e)
        }


# ============================================================================
# Guest Submission Endpoints
# ============================================================================

@router.post("/submit-playlist", response_model=CustomSongList)
async def submit_guest_playlist(request: GuestSubmissionRequest):
    """
    Submit a playlist from a guest contributor.
    
    Playlists submitted by guests are marked as 'pending' and require
    admin approval before becoming active.
    
    Args:
        request: Guest submission with name, description, contributor info, and songs
        
    Returns:
        The created custom list (with pending status)
    """
    try:
        if len(request.songs) == 0:
            raise HTTPException(status_code=400, detail="Playlist must contain at least one song")
        
        custom_list = custom_list_manager.create_list(
            name=request.name,
            description=request.description,
            created_by="guest",
            status="pending",
            submitted_by=request.submitted_by,
            songs=request.songs
        )
        return custom_list
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit playlist: {str(e)}")


@router.put("/lists/{list_id}/status", response_model=CustomSongList)
async def update_list_status(list_id: str, status: str):
    """
    Update the status of a playlist (for admin approval workflow).
    
    Args:
        list_id: List ID
        status: New status (pending, approved, rejected)
        
    Returns:
        Updated custom list
    """
    if status not in ["pending", "approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Status must be 'pending', 'approved', or 'rejected'")
    
    custom_list = custom_list_manager.update_status(list_id, status)
    
    if not custom_list:
        raise HTTPException(status_code=404, detail="Custom list not found")
    
    return custom_list
