"""
Game API Routes

Endpoints for managing game sessions and processing guesses.
"""

from fastapi import APIRouter, HTTPException
import sys
import os
import random

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.spotify_client import SpotifyClient
from app.models import (
    GameStartRequest, GameSession, GuessRequest, GuessResponse,
    GameStats, Track, ErrorResponse
)
from app.game_manager import session_manager

router = APIRouter()


@router.post("/start", response_model=GameSession)
async def start_game(request: GameStartRequest):
    """
    Start a new game session.
    
    Args:
        request: Game configuration including credentials and search params
        
    Returns:
        GameSession: New game session information
        
    Raises:
        HTTPException: If game creation fails
    """
    try:
        # Initialize Spotify client
        spotify_client = SpotifyClient(
            request.credentials.client_id,
            request.credentials.client_secret
        )
        
        # Get songs based on mode
        if request.mode == "genre":
            songs = spotify_client.get_songs_by_genre(request.query, limit=50)
        elif request.mode == "playlist":
            songs = spotify_client.get_songs_from_playlist(request.query)
        elif request.mode == "artist":
            songs = spotify_client.get_top_tracks(request.query)
        else:
            raise HTTPException(status_code=400, detail="Invalid game mode")
        
        if not songs:
            raise HTTPException(
                status_code=404,
                detail=f"No songs with preview URLs found for '{request.query}'"
            )
        
        # Shuffle songs
        random.shuffle(songs)
        
        # Adjust rounds if fewer songs available
        num_rounds = min(request.num_rounds, len(songs))
        
        # Create session
        session_id = session_manager.create_session(
            client_id=request.credentials.client_id,
            client_secret=request.credentials.client_secret,
            songs=songs,
            total_rounds=num_rounds
        )
        
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
