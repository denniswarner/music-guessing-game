"""
Music Guessing Game - Core Package

This package contains the modular components of the music guessing game.
"""

from src.spotify_client import SpotifyClient
from src.game_engine import GameEngine
from src.audio_player import AudioPlayer

__all__ = ['SpotifyClient', 'GameEngine', 'AudioPlayer']
__version__ = '1.0.0'
