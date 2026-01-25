"""
Unit tests for GameEngine module

Tests game logic, scoring, and guess validation.
"""

import pytest
from unittest.mock import Mock, patch
from src.game_engine import GameEngine


class TestGameEngine:
    """Test suite for GameEngine class."""
    
    @pytest.fixture
    def game_engine(self):
        """
        Fixture to create a fresh GameEngine instance.
        
        Returns:
            GameEngine: New game instance
        """
        return GameEngine()
    
    @pytest.fixture
    def mock_song(self):
        """
        Fixture providing a mock song dictionary.
        
        Returns:
            dict: Mock Spotify track object
        """
        return {
            'name': 'Bohemian Rhapsody',
            'artists': [{'name': 'Queen'}],
            'album': {
                'name': 'A Night at the Opera',
                'release_date': '1975-11-21'
            },
            'preview_url': 'http://preview.mp3'
        }
    
    @pytest.fixture
    def mock_audio_player(self):
        """
        Fixture providing a mock AudioPlayer.
        
        Returns:
            Mock: Mocked audio player
        """
        player = Mock()
        player.play_preview_clip = Mock(return_value=True)
        return player
    
    def test_initialization(self, game_engine):
        """Test that GameEngine initializes with zero state."""
        assert game_engine.score == 0.0
        assert game_engine.total_questions == 0
    
    def test_scoring_constants(self):
        """Test that scoring constants are defined correctly."""
        assert GameEngine.FIRST_GUESS_SCORE == 1.0
        assert GameEngine.SECOND_GUESS_SCORE == 0.5
        assert GameEngine.NO_GUESS_SCORE == 0.0
    
    def test_validate_guess_exact_match(self, game_engine):
        """Test exact title match validation."""
        result = game_engine._validate_guess(
            'Bohemian Rhapsody',
            'Bohemian Rhapsody'
        )
        assert result is True
    
    def test_validate_guess_case_insensitive(self, game_engine):
        """Test case-insensitive matching."""
        result = game_engine._validate_guess(
            'bohemian rhapsody',
            'Bohemian Rhapsody'
        )
        assert result is True
    
    def test_validate_guess_substring_match(self, game_engine):
        """Test partial/substring matching."""
        result = game_engine._validate_guess(
            'bohemian',
            'Bohemian Rhapsody'
        )
        assert result is True
    
    def test_validate_guess_with_whitespace(self, game_engine):
        """Test that whitespace is properly trimmed."""
        result = game_engine._validate_guess(
            '  bohemian rhapsody  ',
            'Bohemian Rhapsody'
        )
        assert result is True
    
    def test_validate_guess_incorrect(self, game_engine):
        """Test incorrect guess returns False."""
        result = game_engine._validate_guess(
            'Stairway to Heaven',
            'Bohemian Rhapsody'
        )
        assert result is False
    
    def test_validate_guess_empty_string(self, game_engine):
        """Test empty guess returns False."""
        result = game_engine._validate_guess('', 'Bohemian Rhapsody')
        assert result is False
    
    def test_get_game_stats_no_questions(self, game_engine):
        """Test statistics when no questions have been played."""
        stats = game_engine._get_game_stats()
        
        assert stats['score'] == 0.0
        assert stats['total'] == 0
        assert stats['percentage'] == 0.0
        assert stats['rank'] == 'Keep practicing'
    
    def test_get_game_stats_perfect_score(self, game_engine):
        """Test statistics with 100% correct answers."""
        game_engine.score = 5.0
        game_engine.total_questions = 5
        
        stats = game_engine._get_game_stats()
        
        assert stats['score'] == 5.0
        assert stats['total'] == 5
        assert stats['percentage'] == 100.0
        assert stats['rank'] == 'MUSIC MASTER'
    
    def test_get_game_stats_rank_great_job(self, game_engine):
        """Test rank for 60-79% score."""
        game_engine.score = 3.5
        game_engine.total_questions = 5
        
        stats = game_engine._get_game_stats()
        
        assert stats['percentage'] == 70.0
        assert stats['rank'] == 'Great job'
    
    def test_get_game_stats_rank_not_bad(self, game_engine):
        """Test rank for 40-59% score."""
        game_engine.score = 2.5
        game_engine.total_questions = 5
        
        stats = game_engine._get_game_stats()
        
        assert stats['percentage'] == 50.0
        assert stats['rank'] == 'Not bad'
    
    def test_get_game_stats_rank_keep_practicing(self, game_engine):
        """Test rank for below 40% score."""
        game_engine.score = 1.0
        game_engine.total_questions = 5
        
        stats = game_engine._get_game_stats()
        
        assert stats['percentage'] == 20.0
        assert stats['rank'] == 'Keep practicing'
    
    def test_reset(self, game_engine):
        """Test that reset clears game state."""
        # Set some state
        game_engine.score = 10.0
        game_engine.total_questions = 15
        
        # Reset
        game_engine.reset()
        
        assert game_engine.score == 0.0
        assert game_engine.total_questions == 0
    
    @patch('builtins.input', return_value='bohemian rhapsody')
    @patch('builtins.print')
    def test_play_round_correct_first_guess(
        self,
        mock_print,
        mock_input,
        game_engine,
        mock_song,
        mock_audio_player
    ):
        """Test round with correct first guess awards full points."""
        result = game_engine.play_round(
            mock_song,
            mock_audio_player,
            interactive=True
        )
        
        assert result is True
        assert game_engine.score == 1.0
        assert game_engine.total_questions == 1
        
        # Verify audio was played
        mock_audio_player.play_preview_clip.assert_called_once_with(
            'http://preview.mp3',
            duration_seconds=10
        )
    
    @patch('builtins.input', side_effect=['wrong guess', 'bohemian rhapsody'])
    @patch('builtins.print')
    def test_play_round_correct_second_guess(
        self,
        mock_print,
        mock_input,
        game_engine,
        mock_song,
        mock_audio_player
    ):
        """Test round with correct second guess awards half points."""
        result = game_engine.play_round(
            mock_song,
            mock_audio_player,
            interactive=True
        )
        
        assert result is True
        assert game_engine.score == 0.5
        assert game_engine.total_questions == 1
    
    @patch('builtins.input', side_effect=['wrong guess', 'also wrong'])
    @patch('builtins.print')
    def test_play_round_both_guesses_wrong(
        self,
        mock_print,
        mock_input,
        game_engine,
        mock_song,
        mock_audio_player
    ):
        """Test round with both incorrect guesses awards no points."""
        result = game_engine.play_round(
            mock_song,
            mock_audio_player,
            interactive=True
        )
        
        assert result is False
        assert game_engine.score == 0.0
        assert game_engine.total_questions == 1
    
    def test_play_round_non_interactive(
        self,
        game_engine,
        mock_song,
        mock_audio_player
    ):
        """Test round in non-interactive mode (for testing)."""
        with patch('builtins.print'):
            result = game_engine.play_round(
                mock_song,
                mock_audio_player,
                interactive=False
            )
        
        # Should complete without user input
        assert result is False  # Empty guesses are wrong
        assert game_engine.total_questions == 1
    
    def test_play_game_no_songs(self, game_engine, mock_audio_player):
        """Test game with zero songs available."""
        with patch('builtins.print'):
            stats = game_engine.play_game(
                [],
                mock_audio_player,
                num_rounds=10,
                interactive=False
            )
        
        assert stats['total'] == 0
        assert stats['score'] == 0.0
    
    def test_play_game_fewer_songs_than_rounds(
        self,
        game_engine,
        mock_song,
        mock_audio_player
    ):
        """Test game adjusts rounds when fewer songs available."""
        songs = [mock_song, mock_song]  # Only 2 songs
        
        with patch('builtins.print'):
            stats = game_engine.play_game(
                songs,
                mock_audio_player,
                num_rounds=10,
                interactive=False
            )
        
        # Should only play 2 rounds
        assert stats['total'] == 2
    
    @patch('builtins.input', side_effect=['', 'bohemian', '', 'bohemian'])
    def test_play_game_multiple_rounds(
        self,
        mock_input,
        game_engine,
        mock_song,
        mock_audio_player
    ):
        """Test complete game with multiple rounds."""
        songs = [mock_song] * 3
        
        with patch('builtins.print'):
            stats = game_engine.play_game(
                songs,
                mock_audio_player,
                num_rounds=2,
                interactive=True
            )
        
        assert stats['total'] == 2
        assert stats['score'] == 2.0  # Both correct on first try
    
    @patch('builtins.input', side_effect=['', 'bohemian', 'no'])
    def test_play_game_early_exit(
        self,
        mock_input,
        game_engine,
        mock_song,
        mock_audio_player
    ):
        """Test that user can exit game early."""
        songs = [mock_song] * 5
        
        with patch('builtins.print'):
            stats = game_engine.play_game(
                songs,
                mock_audio_player,
                num_rounds=5,
                interactive=True
            )
        
        # Should only play 1 round before exit
        assert stats['total'] == 1
