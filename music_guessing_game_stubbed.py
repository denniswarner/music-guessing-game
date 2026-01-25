#!/usr/bin/env python3
"""
Spotify Music Guessing Game - STUBBED VERSION
A fun game to play with friends - using mock data for testing!
Plays 10-second clips for a quick challenge!
"""

import random
import time

# Mock song database
MOCK_SONGS = [
    {
        'name': 'Bohemian Rhapsody',
        'artists': [{'name': 'Queen'}],
        'album': {'name': 'A Night at the Opera', 'release_date': '1975-11-21'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock1'
    },
    {
        'name': 'Billie Jean',
        'artists': [{'name': 'Michael Jackson'}],
        'album': {'name': 'Thriller', 'release_date': '1982-01-02'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock2'
    },
    {
        'name': 'Sweet Child O Mine',
        'artists': [{'name': "Guns N' Roses"}],
        'album': {'name': 'Appetite for Destruction', 'release_date': '1987-07-21'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock3'
    },
    {
        'name': 'Smells Like Teen Spirit',
        'artists': [{'name': 'Nirvana'}],
        'album': {'name': 'Nevermind', 'release_date': '1991-09-24'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock4'
    },
    {
        'name': 'Hotel California',
        'artists': [{'name': 'Eagles'}],
        'album': {'name': 'Hotel California', 'release_date': '1976-12-08'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock5'
    },
    {
        'name': 'Imagine',
        'artists': [{'name': 'John Lennon'}],
        'album': {'name': 'Imagine', 'release_date': '1971-10-11'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock6'
    },
    {
        'name': 'Stairway to Heaven',
        'artists': [{'name': 'Led Zeppelin'}],
        'album': {'name': 'Led Zeppelin IV', 'release_date': '1971-11-08'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock7'
    },
    {
        'name': 'Like a Rolling Stone',
        'artists': [{'name': 'Bob Dylan'}],
        'album': {'name': 'Highway 61 Revisited', 'release_date': '1965-08-30'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock8'
    },
    {
        'name': 'Hey Jude',
        'artists': [{'name': 'The Beatles'}],
        'album': {'name': 'Hey Jude', 'release_date': '1968-08-26'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock9'
    },
    {
        'name': 'Purple Rain',
        'artists': [{'name': 'Prince'}],
        'album': {'name': 'Purple Rain', 'release_date': '1984-06-25'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock10'
    },
    {
        'name': 'What\'s Going On',
        'artists': [{'name': 'Marvin Gaye'}],
        'album': {'name': 'What\'s Going On', 'release_date': '1971-05-21'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock11'
    },
    {
        'name': 'Superstition',
        'artists': [{'name': 'Stevie Wonder'}],
        'album': {'name': 'Talking Book', 'release_date': '1972-10-28'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock12'
    },
    {
        'name': 'Thriller',
        'artists': [{'name': 'Michael Jackson'}],
        'album': {'name': 'Thriller', 'release_date': '1982-11-30'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock13'
    },
    {
        'name': 'Born to Run',
        'artists': [{'name': 'Bruce Springsteen'}],
        'album': {'name': 'Born to Run', 'release_date': '1975-08-25'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock14'
    },
    {
        'name': 'Respect',
        'artists': [{'name': 'Aretha Franklin'}],
        'album': {'name': 'I Never Loved a Man the Way I Love You', 'release_date': '1967-03-10'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock15'
    },
    {
        'name': 'Johnny B. Goode',
        'artists': [{'name': 'Chuck Berry'}],
        'album': {'name': 'Chuck Berry Is on Top', 'release_date': '1958-03-31'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock16'
    },
    {
        'name': 'Good Vibrations',
        'artists': [{'name': 'The Beach Boys'}],
        'album': {'name': 'Smiley Smile', 'release_date': '1966-10-10'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock17'
    },
    {
        'name': 'I Want to Hold Your Hand',
        'artists': [{'name': 'The Beatles'}],
        'album': {'name': 'Meet the Beatles!', 'release_date': '1963-11-29'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock18'
    },
    {
        'name': 'London Calling',
        'artists': [{'name': 'The Clash'}],
        'album': {'name': 'London Calling', 'release_date': '1979-12-14'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock19'
    },
    {
        'name': 'Every Breath You Take',
        'artists': [{'name': 'The Police'}],
        'album': {'name': 'Synchronicity', 'release_date': '1983-05-20'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock20'
    }
]

class MockSpotifyAPI:
    """Mock Spotify API for testing"""
    
    def search(self, q, type='track', limit=50):
        """Mock search function"""
        query = q.lower()
        
        # Filter songs based on simple keyword matching
        filtered_songs = MOCK_SONGS.copy()
        
        if 'genre:rock' in query or 'rock' in query:
            # Return rock-ish songs
            filtered_songs = [s for s in MOCK_SONGS if any(artist in s['artists'][0]['name'] 
                            for artist in ['Queen', "Guns N' Roses", 'Nirvana', 'Led Zeppelin', 'The Clash'])]
        elif 'genre:pop' in query or 'pop' in query:
            filtered_songs = [s for s in MOCK_SONGS if any(artist in s['artists'][0]['name']
                            for artist in ['Michael Jackson', 'Prince', 'The Beatles', 'The Beach Boys'])]
        elif '80s' in query or '1980' in query:
            filtered_songs = [s for s in MOCK_SONGS if s['album']['release_date'].startswith('198')]
        elif '70s' in query or '1970' in query:
            filtered_songs = [s for s in MOCK_SONGS if s['album']['release_date'].startswith('197')]
        elif '60s' in query or '1960' in query:
            filtered_songs = [s for s in MOCK_SONGS if s['album']['release_date'].startswith('196')]
        elif 'artist:' in query:
            artist_name = query.split('artist:')[1].strip()
            filtered_songs = [s for s in MOCK_SONGS if artist_name in s['artists'][0]['name'].lower()]
        
        return {'tracks': {'items': filtered_songs[:limit]}}
    
    def playlist_tracks(self, playlist_id):
        """Mock playlist function"""
        # Return all songs as if from a playlist
        return {'items': [{'track': song} for song in MOCK_SONGS]}
    
    def artist_top_tracks(self, artist_id):
        """Mock artist top tracks"""
        # Return random subset
        random_songs = random.sample(MOCK_SONGS, min(10, len(MOCK_SONGS)))
        return {'tracks': random_songs}


class MusicGuessingGame:
    def __init__(self, use_mock=True):
        """Initialize the game - stubbed version doesn't need real credentials"""
        self.sp = MockSpotifyAPI()
        self.score = 0
        self.total_questions = 0
        print("✅ Using MOCK Spotify data (perfect for testing!)")
        
    def get_songs_by_genre(self, genre, limit=50):
        """Get songs by genre/search term"""
        print(f"🎵 Searching for {genre} songs...")
        results = self.sp.search(q=f'genre:{genre}', type='track', limit=limit)
        songs_with_previews = results['tracks']['items']
        return songs_with_previews
    
    def get_songs_from_playlist(self, playlist_url):
        """Get songs from a Spotify playlist URL (mocked)"""
        print(f"🎵 Loading playlist (using mock data)...")
        results = self.sp.playlist_tracks('mock_playlist')
        songs_with_previews = [track['track'] for track in results['items']]
        return songs_with_previews
    
    def get_top_tracks(self, artist_name, limit=20):
        """Get top tracks from an artist"""
        print(f"🎵 Searching for {artist_name}'s songs...")
        results = self.sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
        
        # Filter mock songs by artist
        matching_songs = [s for s in MOCK_SONGS if artist_name.lower() in s['artists'][0]['name'].lower()]
        
        if not matching_songs:
            print(f"No songs found for '{artist_name}' in mock database!")
            print("Try: The Beatles, Queen, Michael Jackson, Nirvana, Prince")
            return []
        
        return matching_songs
    
    def play_round(self, song):
        """Play one round of the game"""
        self.total_questions += 1
        
        print("\n" + "="*60)
        print(f"🎮 ROUND {self.total_questions}")
        print("="*60)
        
        # Show hints
        artists = ", ".join([artist['name'] for artist in song['artists']])
        
        print("\n🎧 [MOCK MODE] Imagine you're listening to a 10-second preview...")
        print(f"   (In real mode, this would play: {song['preview_url']})")
        
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
            print(f"⚠️  Only found {len(songs)} songs in mock database.")
            num_rounds = len(songs)
        
        if num_rounds == 0:
            print("❌ No songs found. Try a different search!")
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
    print("🎵 SPOTIFY MUSIC GUESSING GAME - STUBBED VERSION 🎵")
    print("="*60)
    print("\n⚠️  MOCK MODE: Using fake data for testing")
    print("   (No Spotify API needed - perfect while services are down!)")
    print("   Available songs: Classic rock, pop, and soul hits\n")
    
    game = MusicGuessingGame(use_mock=True)
    
    # Game mode selection
    print("🎮 SELECT GAME MODE:")
    print("1. Search by genre/keyword (e.g., 'rock', 'pop', '80s', '70s')")
    print("2. Use all available songs (mock playlist)")
    print("3. Search by artist name (try: Beatles, Queen, Michael Jackson)")
    
    mode = input("\nChoose mode (1-3): ").strip()
    
    songs = []
    if mode == "1":
        query = input("Enter genre or keyword: ").strip()
        songs = game.get_songs_by_genre(query)
    elif mode == "2":
        print("Using all 20 classic hits!")
        songs = MOCK_SONGS.copy()
    elif mode == "3":
        artist = input("Enter artist name: ").strip()
        songs = game.get_top_tracks(artist)
    else:
        print("Invalid mode selected!")
        return
    
    if songs:
        num_rounds = input(f"\nHow many rounds? (max {len(songs)}): ").strip()
        num_rounds = int(num_rounds) if num_rounds.isdigit() else min(10, len(songs))
        
        game.play_game(songs, num_rounds)
    else:
        print("\n💡 TIP: Try 'rock', '80s', 'The Beatles', or mode 2 for all songs!")


if __name__ == "__main__":
    main()
