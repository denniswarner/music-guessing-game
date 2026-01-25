#!/usr/bin/env python3
"""
Spotify Music Guessing Game
A fun game to play with friends using Spotify's preview clips!
Plays 10-second clips for a quick challenge!
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import webbrowser
import time
import os
import tempfile
try:
    from pydub import AudioSegment
    from pydub.playback import play
    import requests
    AUDIO_SUPPORT = True
except ImportError:
    AUDIO_SUPPORT = False

class MusicGuessingGame:
    def __init__(self, client_id, client_secret):
        """Initialize the game with Spotify credentials"""
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.score = 0
        self.total_questions = 0
        
    def play_preview_clip(self, preview_url, duration_seconds=10):
        """Download and play a preview clip for specified duration"""
        if not AUDIO_SUPPORT:
            print("🎧 Opening 30-second preview in browser (install pydub for 10-sec clips)")
            webbrowser.open(preview_url)
            return
        
        try:
            print("🎧 Downloading and playing 10-second clip...")
            
            # Download the preview
            response = requests.get(preview_url)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_file.write(response.content)
                temp_path = temp_file.name
            
            # Load and trim to 10 seconds
            audio = AudioSegment.from_mp3(temp_path)
            clip = audio[:duration_seconds * 1000]  # Convert to milliseconds
            
            # Play the clip
            play(clip)
            
            # Clean up
            os.unlink(temp_path)
            
        except Exception as e:
            print(f"⚠️  Couldn't play locally: {e}")
            print("🎧 Opening in browser instead...")
            webbrowser.open(preview_url)
        
    def get_songs_by_genre(self, genre, limit=50):
        """Get songs by genre/search term"""
        print(f"🎵 Searching for {genre} songs...")
        results = self.sp.search(q=f'genre:{genre}', type='track', limit=limit)
        
        # Filter songs that have preview URLs
        songs_with_previews = [
            track for track in results['tracks']['items']
            if track['preview_url'] is not None
        ]
        
        return songs_with_previews
    
    def get_songs_from_playlist(self, playlist_url):
        """Get songs from a Spotify playlist URL"""
        # Extract playlist ID from URL
        playlist_id = playlist_url.split('/')[-1].split('?')[0]
        
        print(f"🎵 Loading playlist...")
        results = self.sp.playlist_tracks(playlist_id)
        
        songs_with_previews = [
            track['track'] for track in results['items']
            if track['track'] and track['track']['preview_url'] is not None
        ]
        
        return songs_with_previews
    
    def get_top_tracks(self, artist_name, limit=20):
        """Get top tracks from an artist"""
        print(f"🎵 Searching for {artist_name}'s songs...")
        results = self.sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
        
        if not results['artists']['items']:
            print(f"Artist '{artist_name}' not found!")
            return []
        
        artist_id = results['artists']['items'][0]['id']
        top_tracks = self.sp.artist_top_tracks(artist_id)
        
        songs_with_previews = [
            track for track in top_tracks['tracks']
            if track['preview_url'] is not None
        ]
        
        return songs_with_previews
    
    def play_round(self, song):
        """Play one round of the game"""
        self.total_questions += 1
        
        print("\n" + "="*60)
        print(f"🎮 ROUND {self.total_questions}")
        print("="*60)
        
        # Show hints
        artists = ", ".join([artist['name'] for artist in song['artists']])
        
        print("\n🎵 Playing 10-second preview...")
        
        # Play the 10-second clip
        self.play_preview_clip(song['preview_url'], duration_seconds=10)
        
        input("\nPress ENTER when ready to see hints...")
        
        print(f"\n💡 HINTS:")
        print(f"   Album: {song['album']['name']}")
        print(f"   Released: {song['album']['release_date'][:4]}")
        
        # Get user's guess
        guess = input("\n🎤 Your guess (song title): ").strip().lower()
        correct_title = song['name'].lower()
        
        # Check answer (flexible matching)
        if guess == correct_title or guess in correct_title:
            print("\n🎉 CORRECT! Great job!")
            self.score += 1
            points_earned = 2
        else:
            # Give them the artist hint
            print(f"\n❌ Not quite! Here's another hint...")
            print(f"   Artist(s): {artists}")
            
            guess2 = input("\n🎤 Second guess: ").strip().lower()
            if guess2 == correct_title or guess2 in correct_title:
                print("\n✅ CORRECT on second try!")
                self.score += 0.5
                points_earned = 1
            else:
                print(f"\n❌ The answer was: '{song['name']}' by {artists}")
                points_earned = 0
        
        print(f"\n📊 Score: {self.score}/{self.total_questions}")
        
        return points_earned > 0
    
    def play_game(self, songs, num_rounds=10):
        """Main game loop"""
        if len(songs) < num_rounds:
            print(f"⚠️  Only found {len(songs)} songs with previews.")
            num_rounds = len(songs)
        
        if num_rounds == 0:
            print("❌ No songs with preview clips found. Try a different search!")
            return
        
        print(f"\n🎮 Starting game with {num_rounds} rounds!")
        print("="*60)
        
        # Shuffle and select songs
        random.shuffle(songs)
        game_songs = songs[:num_rounds]
        
        for i, song in enumerate(game_songs):
            self.play_round(song)
            
            if i < len(game_songs) - 1:
                continue_game = input("\n▶️  Continue to next round? (yes/no): ").strip().lower()
                if continue_game not in ['yes', 'y', '']:
                    break
        
        # Final score
        print("\n" + "="*60)
        print("🏁 GAME OVER!")
        print("="*60)
        print(f"Final Score: {self.score}/{self.total_questions}")
        percentage = (self.score / self.total_questions * 100) if self.total_questions > 0 else 0
        print(f"Percentage: {percentage:.1f}%")
        
        if percentage >= 80:
            print("🏆 MUSIC MASTER!")
        elif percentage >= 60:
            print("🎵 Great job!")
        elif percentage >= 40:
            print("🎶 Not bad!")
        else:
            print("🎼 Keep practicing!")


def main():
    print("="*60)
    print("🎵 SPOTIFY MUSIC GUESSING GAME 🎵")
    print("="*60)
    
    print("\n📝 First, you need Spotify API credentials:")
    print("   1. Go to https://developer.spotify.com/dashboard")
    print("   2. Log in with your Spotify account")
    print("   3. Click 'Create an App'")
    print("   4. Copy your Client ID and Client Secret")
    
    client_id = input("\nEnter your Spotify Client ID: ").strip()
    client_secret = input("Enter your Spotify Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Both Client ID and Secret are required!")
        return
    
    try:
        game = MusicGuessingGame(client_id, client_secret)
        print("✅ Connected to Spotify!")
        
        # Game mode selection
        print("\n🎮 SELECT GAME MODE:")
        print("1. Search by genre/keyword (e.g., 'rock', 'pop', '90s')")
        print("2. Use a Spotify playlist URL")
        print("3. Search by artist name")
        
        mode = input("\nChoose mode (1-3): ").strip()
        
        songs = []
        if mode == "1":
            query = input("Enter genre or keyword: ").strip()
            songs = game.get_songs_by_genre(query)
        elif mode == "2":
            playlist_url = input("Enter Spotify playlist URL: ").strip()
            songs = game.get_songs_from_playlist(playlist_url)
        elif mode == "3":
            artist = input("Enter artist name: ").strip()
            songs = game.get_top_tracks(artist)
        else:
            print("Invalid mode selected!")
            return
        
        if songs:
            num_rounds = input(f"\nHow many rounds? (max {len(songs)}): ").strip()
            num_rounds = int(num_rounds) if num_rounds.isdigit() else 10
            
            game.play_game(songs, num_rounds)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure your credentials are correct!")


if __name__ == "__main__":
    main()
