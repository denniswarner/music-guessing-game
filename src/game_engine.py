"""
Game Engine Module

Core game logic including round management, scoring, hints, and user interaction.
"""

from typing import Dict, Any, List, Optional
import random


class GameEngine:
    """
    Manages the game state and logic for the music guessing game.
    
    Handles round progression, scoring, hint display, and guess validation.
    """
    
    # Scoring constants
    FIRST_GUESS_SCORE = 1.0
    SECOND_GUESS_SCORE = 0.5
    NO_GUESS_SCORE = 0.0
    
    def __init__(self):
        """Initialize a new game with zero score and rounds."""
        self.score: float = 0.0
        self.total_questions: int = 0
    
    def play_round(
        self, 
        song: Dict[str, Any], 
        audio_player,
        interactive: bool = True
    ) -> bool:
        """
        Play one complete round of the game.
        
        Args:
            song (Dict[str, Any]): Spotify track object with metadata
            audio_player: AudioPlayer instance for playing previews
            interactive (bool): If False, skip user input (for testing)
            
        Returns:
            bool: True if player guessed correctly (either attempt)
        """
        self.total_questions += 1
        
        print("\n" + "="*60)
        print(f"🎮 ROUND {self.total_questions}")
        print("="*60)
        
        # Get artist names for hints
        artists = ", ".join([artist['name'] for artist in song['artists']])
        
        # Play the audio preview
        print("\n🎵 Playing 10-second preview...")
        audio_player.play_preview_clip(song['preview_url'], duration_seconds=10)
        
        if interactive:
            input("\nPress ENTER when ready to see hints...")
        
        # Display initial hints (album and year)
        self._display_hints(song, show_artist=False)
        
        # Get first guess
        if interactive:
            guess = input("\n🎤 Your guess (song title): ").strip()
        else:
            guess = ""  # For testing
        
        correct_title = song['name']
        
        # Check first guess
        if self._validate_guess(guess, correct_title):
            print("\n🎉 CORRECT! Great job!")
            self.score += self.FIRST_GUESS_SCORE
            points_earned = 2
            correct = True
        else:
            # Give second chance with artist hint
            print(f"\n❌ Not quite! Here's another hint...")
            print(f"   Artist(s): {artists}")
            
            if interactive:
                guess2 = input("\n🎤 Second guess: ").strip()
            else:
                guess2 = ""
            
            if self._validate_guess(guess2, correct_title):
                print("\n✅ CORRECT on second try!")
                self.score += self.SECOND_GUESS_SCORE
                points_earned = 1
                correct = True
            else:
                print(f"\n❌ The answer was: '{song['name']}' by {artists}")
                points_earned = 0
                correct = False
        
        # Display current score
        print(f"\n📊 Score: {self.score}/{self.total_questions}")
        
        return correct
    
    def play_game(
        self, 
        songs: List[Dict[str, Any]], 
        audio_player,
        num_rounds: int = 10,
        interactive: bool = True
    ) -> Dict[str, Any]:
        """
        Run the complete game loop for multiple rounds.
        
        Args:
            songs (List[Dict[str, Any]]): List of track objects to play
            audio_player: AudioPlayer instance
            num_rounds (int): Number of rounds to play (default: 10)
            interactive (bool): If False, skip user prompts (for testing)
            
        Returns:
            Dict[str, Any]: Final game statistics
                - 'score': float
                - 'total': int
                - 'percentage': float
                - 'rank': str
        """
        # Validate song count
        if len(songs) < num_rounds:
            print(f"⚠️  Only found {len(songs)} songs with previews.")
            num_rounds = len(songs)
        
        if num_rounds == 0:
            print("❌ No songs with preview clips found. Try a different search!")
            return self._get_game_stats()
        
        print(f"\n🎮 Starting game with {num_rounds} rounds!")
        print("="*60)
        
        # Shuffle and select songs
        # Reason: Create a copy to avoid modifying original list
        shuffled_songs = songs.copy()
        random.shuffle(shuffled_songs)
        game_songs = shuffled_songs[:num_rounds]
        
        # Play each round
        for i, song in enumerate(game_songs):
            self.play_round(song, audio_player, interactive=interactive)
            
            # Ask to continue (except after last round)
            if i < len(game_songs) - 1 and interactive:
                continue_game = input(
                    "\n▶️  Continue to next round? (yes/no): "
                ).strip().lower()
                if continue_game not in ['yes', 'y', '']:
                    break
        
        # Display final results
        stats = self._get_game_stats()
        self._display_final_results(stats)
        
        return stats
    
    def _validate_guess(self, guess: str, correct_title: str) -> bool:
        """
        Check if a guess matches the correct title.
        
        Uses case-insensitive substring matching for flexibility.
        
        Args:
            guess (str): User's guess
            correct_title (str): Actual song title
            
        Returns:
            bool: True if guess is correct or partially matches
        """
        if not guess:
            return False
        
        guess_lower = guess.lower().strip()
        title_lower = correct_title.lower().strip()
        
        # Exact match or substring match
        return guess_lower == title_lower or guess_lower in title_lower
    
    def _display_hints(self, song: Dict[str, Any], show_artist: bool = False):
        """
        Display hints about the song to the player.
        
        Args:
            song (Dict[str, Any]): Track object with metadata
            show_artist (bool): If True, also show artist name
        """
        print(f"\n💡 HINTS:")
        print(f"   Album: {song['album']['name']}")
        print(f"   Released: {song['album']['release_date'][:4]}")
        
        if show_artist:
            artists = ", ".join([artist['name'] for artist in song['artists']])
            print(f"   Artist(s): {artists}")
    
    def _get_game_stats(self) -> Dict[str, Any]:
        """
        Calculate game statistics.
        
        Returns:
            Dict[str, Any]: Statistics dictionary with score, total, percentage, rank
        """
        percentage = (
            (self.score / self.total_questions * 100) 
            if self.total_questions > 0 
            else 0.0
        )
        
        # Determine rank based on percentage
        if percentage >= 80:
            rank = "MUSIC MASTER"
        elif percentage >= 60:
            rank = "Great job"
        elif percentage >= 40:
            rank = "Not bad"
        else:
            rank = "Keep practicing"
        
        return {
            'score': self.score,
            'total': self.total_questions,
            'percentage': percentage,
            'rank': rank
        }
    
    def _display_final_results(self, stats: Dict[str, Any]):
        """
        Display final game results to the player.
        
        Args:
            stats (Dict[str, Any]): Statistics from _get_game_stats()
        """
        print("\n" + "="*60)
        print("🏁 GAME OVER!")
        print("="*60)
        print(f"Final Score: {stats['score']}/{stats['total']}")
        print(f"Percentage: {stats['percentage']:.1f}%")
        
        # Display rank with emoji
        rank = stats['rank']
        if rank == "MUSIC MASTER":
            print(f"🏆 {rank}!")
        elif rank == "Great job":
            print(f"🎵 {rank}!")
        elif rank == "Not bad":
            print(f"🎶 {rank}!")
        else:
            print(f"🎼 {rank}!")
    
    def reset(self):
        """Reset game state to start a new game."""
        self.score = 0.0
        self.total_questions = 0
