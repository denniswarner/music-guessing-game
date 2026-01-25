"""
Unit tests for SpotifyClient module

Tests Spotify API interactions with mocked responses.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.spotify_client import SpotifyClient


class TestSpotifyClient:
    """Test suite for SpotifyClient class."""
    
    @pytest.fixture
    def mock_spotify_api(self):
        """
        Fixture to mock spotipy.Spotify class.
        
        Returns:
            Mock: Mocked Spotify client
        """
        with patch('src.spotify_client.spotipy.Spotify') as mock_sp:
            yield mock_sp
    
    @pytest.fixture
    def spotify_client(self, mock_spotify_api):
        """
        Fixture to create SpotifyClient instance with mocked API.
        
        Returns:
            SpotifyClient: Client instance for testing
        """
        with patch('src.spotify_client.SpotifyClientCredentials'):
            client = SpotifyClient("test_id", "test_secret")
            return client
    
    def test_initialization(self):
        """Test that SpotifyClient initializes correctly with credentials."""
        with patch('src.spotify_client.SpotifyClientCredentials') as mock_creds:
            with patch('src.spotify_client.spotipy.Spotify') as mock_sp:
                client = SpotifyClient("my_id", "my_secret")
                
                assert client is not None
                mock_creds.assert_called_once_with(
                    client_id="my_id",
                    client_secret="my_secret"
                )
    
    def test_get_songs_by_genre_success(self, spotify_client):
        """Test successful genre search with preview URLs."""
        # Mock response data
        mock_tracks = {
            'tracks': {
                'items': [
                    {'name': 'Song 1', 'preview_url': 'http://preview1.mp3'},
                    {'name': 'Song 2', 'preview_url': None},  # No preview
                    {'name': 'Song 3', 'preview_url': 'http://preview3.mp3'},
                ]
            }
        }
        
        spotify_client.sp.search = Mock(return_value=mock_tracks)
        
        result = spotify_client.get_songs_by_genre('rock', limit=50)
        
        # Should filter out songs without preview URLs
        assert len(result) == 2
        assert result[0]['name'] == 'Song 1'
        assert result[1]['name'] == 'Song 3'
        
        spotify_client.sp.search.assert_called_once_with(
            q='genre:rock',
            type='track',
            limit=50
        )
    
    def test_get_songs_by_genre_no_previews(self, spotify_client):
        """Test genre search when no songs have preview URLs."""
        mock_tracks = {
            'tracks': {
                'items': [
                    {'name': 'Song 1', 'preview_url': None},
                    {'name': 'Song 2', 'preview_url': None},
                ]
            }
        }
        
        spotify_client.sp.search = Mock(return_value=mock_tracks)
        
        result = spotify_client.get_songs_by_genre('jazz')
        
        assert len(result) == 0
    
    def test_get_songs_from_playlist_success(self, spotify_client):
        """Test successful playlist track retrieval."""
        mock_playlist = {
            'items': [
                {
                    'track': {
                        'name': 'Track 1',
                        'preview_url': 'http://preview1.mp3'
                    }
                },
                {
                    'track': {
                        'name': 'Track 2',
                        'preview_url': 'http://preview2.mp3'
                    }
                },
                {
                    'track': None  # Edge case: null track
                }
            ]
        }
        
        spotify_client.sp.playlist_tracks = Mock(return_value=mock_playlist)
        
        url = 'https://open.spotify.com/playlist/abc123?si=xyz'
        result = spotify_client.get_songs_from_playlist(url)
        
        assert len(result) == 2
        assert result[0]['name'] == 'Track 1'
        
        spotify_client.sp.playlist_tracks.assert_called_once_with('abc123')
    
    def test_get_songs_from_playlist_invalid_url(self, spotify_client):
        """Test playlist method with invalid URL format."""
        with pytest.raises(ValueError, match="Invalid playlist URL"):
            spotify_client.get_songs_from_playlist('not_a_valid_url')
    
    def test_get_top_tracks_artist_found(self, spotify_client):
        """Test retrieving top tracks for existing artist."""
        mock_search = {
            'artists': {
                'items': [
                    {'id': 'artist123', 'name': 'Test Artist'}
                ]
            }
        }
        
        mock_top_tracks = {
            'tracks': [
                {'name': 'Hit 1', 'preview_url': 'http://preview1.mp3'},
                {'name': 'Hit 2', 'preview_url': None},
                {'name': 'Hit 3', 'preview_url': 'http://preview3.mp3'},
            ]
        }
        
        spotify_client.sp.search = Mock(return_value=mock_search)
        spotify_client.sp.artist_top_tracks = Mock(return_value=mock_top_tracks)
        
        result = spotify_client.get_top_tracks('Test Artist')
        
        assert len(result) == 2  # Only tracks with previews
        assert result[0]['name'] == 'Hit 1'
        
        spotify_client.sp.search.assert_called_once_with(
            q='artist:Test Artist',
            type='artist',
            limit=1
        )
        spotify_client.sp.artist_top_tracks.assert_called_once_with('artist123')
    
    def test_get_top_tracks_artist_not_found(self, spotify_client):
        """Test top tracks when artist doesn't exist."""
        mock_search = {
            'artists': {
                'items': []  # No artists found
            }
        }
        
        spotify_client.sp.search = Mock(return_value=mock_search)
        
        result = spotify_client.get_top_tracks('Nonexistent Artist')
        
        assert len(result) == 0
    
    def test_validate_preview_url_with_url(self):
        """Test validation of track with preview URL."""
        track = {'preview_url': 'http://preview.mp3'}
        assert SpotifyClient.validate_preview_url(track) is True
    
    def test_validate_preview_url_without_url(self):
        """Test validation of track without preview URL."""
        track = {'preview_url': None}
        assert SpotifyClient.validate_preview_url(track) is False
    
    def test_validate_preview_url_missing_key(self):
        """Test validation of track missing preview_url key."""
        track = {'name': 'Song'}
        assert SpotifyClient.validate_preview_url(track) is False
