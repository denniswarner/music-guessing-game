"""
Unit tests for AudioPlayer module

Tests audio playback functionality with mocked dependencies.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
import tempfile
import os

from src.audio_player import AudioPlayer


class TestAudioPlayer:
    """Test suite for AudioPlayer class."""
    
    @pytest.fixture
    def audio_player(self):
        """
        Fixture to create AudioPlayer instance.
        
        Returns:
            AudioPlayer: Player instance for testing
        """
        return AudioPlayer()
    
    def test_initialization_with_audio_support(self):
        """Test initialization when audio dependencies are available."""
        with patch('src.audio_player.AUDIO_SUPPORT', True):
            player = AudioPlayer()
            assert player.has_local_support is True
    
    def test_initialization_without_audio_support(self):
        """Test initialization when audio dependencies are missing."""
        with patch('src.audio_player.AUDIO_SUPPORT', False):
            player = AudioPlayer()
            assert player.has_local_support is False
    
    @patch('src.audio_player.webbrowser.open')
    def test_play_in_browser(self, mock_browser, audio_player):
        """Test browser fallback playback."""
        url = 'http://preview.mp3'
        
        result = audio_player._play_in_browser(url)
        
        assert result is True
        mock_browser.assert_called_once_with(url)
    
    @patch('src.audio_player.AUDIO_SUPPORT', False)
    @patch('src.audio_player.webbrowser.open')
    def test_play_preview_without_local_support(self, mock_browser):
        """Test that player falls back to browser when no local support."""
        player = AudioPlayer()
        url = 'http://preview.mp3'
        
        result = player.play_preview_clip(url, duration_seconds=10)
        
        assert result is True
        mock_browser.assert_called_once_with(url)
    
    @patch('src.audio_player.AUDIO_SUPPORT', True)
    @patch('src.audio_player.requests')
    @patch('src.audio_player.AudioSegment')
    @patch('src.audio_player.play')
    @patch('src.audio_player.tempfile.NamedTemporaryFile')
    @patch('src.audio_player.os.unlink')
    def test_play_locally_success(
        self,
        mock_unlink,
        mock_tempfile,
        mock_play,
        mock_audio_segment,
        mock_requests
    ):
        """Test successful local audio playback."""
        # Setup mocks
        mock_response = Mock()
        mock_response.content = b'fake_audio_data'
        mock_requests.get.return_value = mock_response
        
        mock_temp = Mock()
        mock_temp.name = '/tmp/test.mp3'
        mock_temp.__enter__ = Mock(return_value=mock_temp)
        mock_temp.__exit__ = Mock(return_value=False)
        mock_tempfile.return_value = mock_temp
        
        mock_audio = Mock()
        mock_clip = Mock()
        mock_audio.__getitem__ = Mock(return_value=mock_clip)
        mock_audio_segment.from_mp3.return_value = mock_audio
        
        player = AudioPlayer()
        player.has_local_support = True
        
        url = 'http://preview.mp3'
        result = player._play_locally(url, duration_seconds=10)
        
        assert result is True
        mock_requests.get.assert_called_once_with(url, timeout=10)
        mock_audio_segment.from_mp3.assert_called_once_with('/tmp/test.mp3')
        mock_play.assert_called_once_with(mock_clip)
        mock_unlink.assert_called_once_with('/tmp/test.mp3')
    
    @patch('src.audio_player.AUDIO_SUPPORT', True)
    @patch('src.audio_player.requests')
    def test_play_locally_download_failure(self, mock_requests):
        """Test handling of download failure."""
        mock_requests.get.side_effect = Exception("Network error")
        
        player = AudioPlayer()
        player.has_local_support = True
        
        with pytest.raises(Exception, match="Network error"):
            player._play_locally('http://preview.mp3', 10)
    
    @patch('src.audio_player.AUDIO_SUPPORT', True)
    @patch('src.audio_player.webbrowser.open')
    def test_play_preview_fallback_on_error(self, mock_browser):
        """Test automatic fallback to browser on local playback error."""
        player = AudioPlayer()
        player.has_local_support = True
        
        # Mock _play_locally to raise exception
        with patch.object(
            player,
            '_play_locally',
            side_effect=Exception("Playback failed")
        ):
            url = 'http://preview.mp3'
            result = player.play_preview_clip(url, duration_seconds=10)
            
            assert result is True
            mock_browser.assert_called_once_with(url)
    
    @patch('subprocess.run')
    def test_check_dependencies_all_available(self, mock_subprocess):
        """Test dependency check when all are available."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result
        
        with patch('src.audio_player.AUDIO_SUPPORT', True):
            # Temporarily make imports available
            with patch.dict('sys.modules', {
                'pydub': Mock(),
                'requests': Mock()
            }):
                deps = AudioPlayer.check_dependencies()
                
                assert deps['pydub'] is True
                assert deps['requests'] is True
                assert deps['ffmpeg'] is True
    
    @patch('subprocess.run')
    def test_check_dependencies_missing_ffmpeg(self, mock_subprocess):
        """Test dependency check when ffmpeg is missing."""
        mock_subprocess.side_effect = FileNotFoundError("ffmpeg not found")
        
        with patch.dict('sys.modules', {
            'pydub': Mock(),
            'requests': Mock()
        }):
            deps = AudioPlayer.check_dependencies()
            
            assert deps['pydub'] is True
            assert deps['requests'] is True
            assert deps['ffmpeg'] is False
    
    def test_check_dependencies_none_available(self):
        """Test dependency check when no optional deps available."""
        # Simulate ImportError for all packages
        with patch('src.audio_player.AUDIO_SUPPORT', False):
            deps = AudioPlayer.check_dependencies()
            
            # At minimum, should return dict with all keys
            assert 'pydub' in deps
            assert 'requests' in deps
            assert 'ffmpeg' in deps
    
    @patch('src.audio_player.AUDIO_SUPPORT', True)
    @patch('src.audio_player.requests')
    @patch('src.audio_player.AudioSegment')
    @patch('src.audio_player.play')
    @patch('src.audio_player.tempfile.NamedTemporaryFile')
    @patch('src.audio_player.os.unlink')
    def test_play_locally_cleans_up_on_error(
        self,
        mock_unlink,
        mock_tempfile,
        mock_play,
        mock_audio_segment,
        mock_requests
    ):
        """Test that temp file is cleaned up even if playback fails."""
        # Setup mocks
        mock_response = Mock()
        mock_response.content = b'fake_audio_data'
        mock_requests.get.return_value = mock_response
        
        mock_temp = Mock()
        mock_temp.name = '/tmp/test.mp3'
        mock_temp.__enter__ = Mock(return_value=mock_temp)
        mock_temp.__exit__ = Mock(return_value=False)
        mock_tempfile.return_value = mock_temp
        
        mock_audio = Mock()
        mock_audio.__getitem__ = Mock(side_effect=Exception("Audio error"))
        mock_audio_segment.from_mp3.return_value = mock_audio
        
        player = AudioPlayer()
        player.has_local_support = True
        
        url = 'http://preview.mp3'
        
        # Should raise exception but still clean up
        with pytest.raises(Exception, match="Audio error"):
            player._play_locally(url, duration_seconds=10)
        
        # Verify cleanup was attempted
        mock_unlink.assert_called_once_with('/tmp/test.mp3')
    
    @patch('src.audio_player.AUDIO_SUPPORT', True)
    @patch('src.audio_player.requests')
    @patch('src.audio_player.AudioSegment')
    @patch('src.audio_player.play')
    @patch('src.audio_player.tempfile.NamedTemporaryFile')
    @patch('src.audio_player.os.unlink')
    def test_play_locally_trimming(
        self,
        mock_unlink,
        mock_tempfile,
        mock_play,
        mock_audio_segment,
        mock_requests
    ):
        """Test that audio is correctly trimmed to specified duration."""
        # Setup mocks
        mock_response = Mock()
        mock_response.content = b'fake_audio_data'
        mock_requests.get.return_value = mock_response
        
        mock_temp = Mock()
        mock_temp.name = '/tmp/test.mp3'
        mock_temp.__enter__ = Mock(return_value=mock_temp)
        mock_temp.__exit__ = Mock(return_value=False)
        mock_tempfile.return_value = mock_temp
        
        mock_audio = Mock()
        mock_clip = Mock()
        mock_audio.__getitem__ = Mock(return_value=mock_clip)
        mock_audio_segment.from_mp3.return_value = mock_audio
        
        player = AudioPlayer()
        player.has_local_support = True
        
        url = 'http://preview.mp3'
        player._play_locally(url, duration_seconds=15)
        
        # Verify trimming: 15 seconds = 15000 milliseconds
        mock_audio.__getitem__.assert_called_once()
        call_args = mock_audio.__getitem__.call_args[0]
        assert call_args[0].stop == 15000  # slice(None, 15000, None)
