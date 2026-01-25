#!/usr/bin/env python3
"""
Spotify Music Guessing Game - Refactored Version

A fun music guessing game using Spotify's API with 10-second preview clips.
This version uses modular architecture for better maintainability.
"""

import os
import sys
from typing import Optional, List, Dict, Any

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

from src.spotify_client import SpotifyClient
from src.game_engine import GameEngine
from src.audio_player import AudioPlayer


def load_credentials() -> tuple[Optional[str], Optional[str]]:
    """
    Load Spotify credentials from environment or user input.
    
    Attempts to load from .env file first, falls back to interactive prompt.
    
    Returns:
        tuple[Optional[str], Optional[str]]: (client_id, client_secret)
    """
    # Try loading from .env file
    if DOTENV_AVAILABLE:
        load_dotenv()
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if client_id and client_secret:
            print("✅ Loaded credentials from .env file")
            return client_id, client_secret
    
    # Fall back to interactive prompt
    print("\n📝 Spotify API credentials needed:")
    print("   1. Go to https://developer.spotify.com/dashboard")
    print("   2. Log in with your Spotify account")
    print("   3. Click 'Create an App'")
    print("   4. Copy your Client ID and Client Secret")
    
    client_id = input("\nEnter your Spotify Client ID: ").strip()
    client_secret = input("Enter your Spotify Client Secret: ").strip()
    
    return client_id, client_secret


def get_songs_from_user(spotify_client: SpotifyClient) -> List[Dict[str, Any]]:
    """
    Prompt user for game mode and retrieve songs accordingly.
    
    Args:
        spotify_client (SpotifyClient): Initialized Spotify client
        
    Returns:
        List[Dict[str, Any]]: List of track objects
    """
    print("\n🎮 SELECT GAME MODE:")
    print("1. Search by genre/keyword (e.g., 'rock', 'pop', '90s')")
    print("2. Use a Spotify playlist URL")
    print("3. Search by artist name")
    
    mode = input("\nChoose mode (1-3): ").strip()
    
    songs = []
    
    if mode == "1":
        query = input("Enter genre or keyword: ").strip()
        songs = spotify_client.get_songs_by_genre(query)
    elif mode == "2":
        playlist_url = input("Enter Spotify playlist URL: ").strip()
        try:
            songs = spotify_client.get_songs_from_playlist(playlist_url)
        except ValueError as e:
            print(f"❌ Error: {e}")
            return []
    elif mode == "3":
        artist = input("Enter artist name: ").strip()
        songs = spotify_client.get_top_tracks(artist)
    else:
        print("❌ Invalid mode selected!")
        return []
    
    return songs


def main():
    """Main entry point for the game."""
    print("="*60)
    print("🎵 SPOTIFY MUSIC GUESSING GAME 🎵")
    print("="*60)
    
    # Load credentials
    client_id, client_secret = load_credentials()
    
    if not client_id or not client_secret:
        print("❌ Both Client ID and Secret are required!")
        sys.exit(1)
    
    try:
        # Initialize components
        spotify_client = SpotifyClient(client_id, client_secret)
        print("✅ Connected to Spotify!")
        
        audio_player = AudioPlayer()
        game_engine = GameEngine()
        
        # Get songs based on user preference
        songs = get_songs_from_user(spotify_client)
        
        if not songs:
            print("❌ No songs found. Please try again.")
            sys.exit(1)
        
        # Get number of rounds
        num_rounds = input(
            f"\nHow many rounds? (max {len(songs)}): "
        ).strip()
        num_rounds = int(num_rounds) if num_rounds.isdigit() else 10
        
        # Play the game
        game_engine.play_game(songs, audio_player, num_rounds)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure your credentials are correct!")
        sys.exit(1)


if __name__ == "__main__":
    main()
