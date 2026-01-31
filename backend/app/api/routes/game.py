"""
Game API Routes

Endpoints for managing game sessions and processing guesses.
Supports multiple music providers: Spotify, Deezer, and Demo mode.
"""

from fastapi import APIRouter, HTTPException
import sys
import os
import random

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.spotify_client import SpotifyClient
from src.deezer_client import DeezerClient
from app.models import (
    GameStartRequest, GameSession, GuessRequest, GuessResponse,
    GameStats, Track, ErrorResponse
)
from app.game_manager import session_manager
from app.mock_data import filter_mock_songs
from app.custom_list_manager import custom_list_manager

router = APIRouter()


def get_music_client(provider: str, credentials: dict):
    """
    Factory function to create the appropriate music provider client.
    
    Args:
        provider: Music provider name ('spotify', 'deezer', 'demo')
        credentials: Provider credentials (if needed)
        
    Returns:
        Music client instance
        
    Raises:
        ValueError: If provider is invalid or credentials missing
    """
    if provider == "spotify":
        if not credentials.client_id or not credentials.client_secret:
            raise ValueError("Spotify requires client_id and client_secret")
        return SpotifyClient(credentials.client_id, credentials.client_secret)
    
    elif provider == "deezer":
        # Deezer doesn't require credentials for public API
        return DeezerClient()
    
    elif provider == "demo":
        return None  # Demo mode doesn't need a client
    
    else:
        raise ValueError(f"Unknown provider: {provider}")


@router.post("/start", response_model=GameSession)
async def start_game(request: GameStartRequest):
    """
    Start a new game session with the selected music provider.
    
    Supports:
    - Spotify (requires credentials)
    - Deezer (no credentials needed)
    - Demo mode (mock data)
    - Custom mode (admin-created lists)
    
    Args:
        request: Game configuration including provider, credentials, and search params
        
    Returns:
        GameSession: New game session information
        
    Raises:
        HTTPException: If game creation fails
    """
    try:
        # Handle custom list mode
        if request.mode == "custom" or request.provider == "custom":
            if not request.custom_list_id:
                raise HTTPException(status_code=400, detail="custom_list_id required for custom mode")
            
            # Get filters if provided
            filters = request.custom_filters or {}
            
            # Get songs from custom list
            songs = custom_list_manager.filter_songs(
                list_id=request.custom_list_id,
                decade=filters.get("decade"),
                genre=filters.get("genre"),
                style=filters.get("style"),
                mood=filters.get("mood"),
                difficulty=filters.get("difficulty")
            )
            
            if not songs:
                raise HTTPException(
                    status_code=404,
                    detail="No songs found in custom list with the specified filters"
                )
            
            # Convert CustomSong to dict format expected by game
            songs = [
                {
                    'id': song.id,
                    'name': song.name,
                    'artists': [{'name': song.artist}],
                    'album': {'name': song.album or 'Unknown Album', 'release_date': 'Unknown'},
                    'preview_url': song.preview_url,
                    'provider': song.provider
                }
                for song in songs
            ]
            
            random.shuffle(songs)
            num_rounds = min(request.num_rounds, len(songs))
            
            # Increment play count for this list
            custom_list_manager.increment_play_count(request.custom_list_id)
            
            session_id = session_manager.create_session(
                client_id="custom",
                client_secret="",
                songs=songs,
                total_rounds=num_rounds
            )
        
        # Handle demo mode
        elif request.demo_mode or request.provider == "demo":
            songs = filter_mock_songs(request.query)
            if not songs:
                songs = filter_mock_songs()  # Get all if no match
            
            random.shuffle(songs)
            num_rounds = min(request.num_rounds, len(songs))
            
            session_id = session_manager.create_session(
                client_id="demo",
                client_secret="demo",
                songs=songs,
                total_rounds=num_rounds
            )
        
        else:
            # Initialize the appropriate music provider client
            music_client = get_music_client(request.provider, request.credentials)
            
            # Get songs based on mode
            if request.mode == "genre":
                songs = music_client.get_songs_by_genre(request.query, limit=50)
            elif request.mode == "playlist":
                songs = music_client.get_songs_from_playlist(request.query)
            elif request.mode == "artist":
                songs = music_client.get_top_tracks(request.query)
            else:
                raise HTTPException(status_code=400, detail="Invalid game mode")
        
            if not songs:
                raise HTTPException(
                    status_code=404,
                    detail=f"No songs with preview URLs found for '{request.query}' on {request.provider}"
                )
            
            # Songs from our clients are already normalized internally
            # Just shuffle and limit them
            random.shuffle(songs)
            num_rounds = min(request.num_rounds, len(songs))
            
            # Create session
            session_id = session_manager.create_session(
                client_id=request.provider,  # Pass provider name instead
                client_secret="",
                songs=songs,
                total_rounds=num_rounds
            )
            
            # Use the songs directly (already normalized)
            songs = songs[:num_rounds]
        
        # Convert songs to Track models
        tracks = [
            session_manager.convert_track_to_model(song) 
            for song in songs[:num_rounds]
        ]
        
        return GameSession(
            session_id=session_id,
            total_rounds=num_rounds,
            current_round=0,
            score=0.0,
            songs=tracks
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start game: {str(e)}")


@router.post("/guess", response_model=GuessResponse)
async def submit_guess(request: GuessRequest):
    """
    Submit a guess for the current round.
    
    Args:
        request: Guess submission with session ID and guess text
        
    Returns:
        GuessResponse: Result of the guess
        
    Raises:
        HTTPException: If session not found or guess processing fails
    """
    session = session_manager.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    try:
        # Get current song
        if session.current_round >= len(session.songs):
            raise HTTPException(status_code=400, detail="Game already completed")
        
        current_song = session.songs[session.current_round]
        correct_title = current_song['name']
        artists = ", ".join([a['name'] for a in current_song['artists']])
        
        # Validate guess
        is_correct = session.game_engine._validate_guess(request.guess, correct_title)
        
        points_earned = 0.0
        artist_hint = None
        is_final_guess = False
        
        if not session.first_guess_made:
            # First guess
            session.first_guess_made = True
            
            if is_correct:
                # Correct on first try
                session.game_engine.score += session.game_engine.FIRST_GUESS_SCORE
                session.game_engine.total_questions += 1
                points_earned = 2.0
                is_final_guess = True
                
                # Move to next round
                session.current_round += 1
                session.first_guess_made = False
            else:
                # Incorrect, give hint for second guess
                artist_hint = artists
                points_earned = 0.0
        else:
            # Second guess
            is_final_guess = True
            session.game_engine.total_questions += 1
            
            if is_correct:
                # Correct on second try
                session.game_engine.score += session.game_engine.SECOND_GUESS_SCORE
                points_earned = 1.0
            else:
                # Incorrect on second try
                points_earned = 0.0
            
            # Move to next round
            session.current_round += 1
            session.first_guess_made = False
        
        return GuessResponse(
            correct=is_correct,
            points_earned=points_earned,
            correct_answer=correct_title if is_final_guess and not is_correct else None,
            artist_hint=artist_hint,
            total_score=session.game_engine.score,
            is_final_guess=is_final_guess
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process guess: {str(e)}")


@router.get("/session/{session_id}", response_model=dict)
async def get_session_info(session_id: str):
    """
    Get current session information.
    
    Args:
        session_id: Session identifier
        
    Returns:
        dict: Session state information
    """
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    return {
        "session_id": session.session_id,
        "total_rounds": session.total_rounds,
        "current_round": session.current_round,
        "score": session.game_engine.score,
        "total_questions": session.game_engine.total_questions
    }


@router.get("/stats/{session_id}", response_model=GameStats)
async def get_game_stats(session_id: str):
    """
    Get final game statistics.
    
    Args:
        session_id: Session identifier
        
    Returns:
        GameStats: Final statistics
    """
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    stats = session.game_engine._get_game_stats()
    
    return GameStats(
        total_rounds=stats['total'],
        score=stats['score'],
        percentage=stats['percentage'],
        rank=stats['rank']
    )


@router.delete("/session/{session_id}")
async def end_game(session_id: str):
    """
    End a game session and clean up.
    
    Args:
        session_id: Session identifier
        
    Returns:
        dict: Confirmation message
    """
    session_manager.delete_session(session_id)
    return {"message": "Game session ended"}
