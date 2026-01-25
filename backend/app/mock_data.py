"""
Mock song data for demo mode.

Uses the same classic songs as the stubbed CLI version.
"""

MOCK_SONGS = [
    {
        'id': 'mock1',
        'name': 'Bohemian Rhapsody',
        'artists': [{'name': 'Queen'}],
        'album': {'name': 'A Night at the Opera', 'release_date': '1975-11-21'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock1'
    },
    {
        'id': 'mock2',
        'name': 'Billie Jean',
        'artists': [{'name': 'Michael Jackson'}],
        'album': {'name': 'Thriller', 'release_date': '1982-01-02'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock2'
    },
    {
        'id': 'mock3',
        'name': 'Sweet Child O Mine',
        'artists': [{'name': "Guns N' Roses"}],
        'album': {'name': 'Appetite for Destruction', 'release_date': '1987-07-21'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock3'
    },
    {
        'id': 'mock4',
        'name': 'Smells Like Teen Spirit',
        'artists': [{'name': 'Nirvana'}],
        'album': {'name': 'Nevermind', 'release_date': '1991-09-24'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock4'
    },
    {
        'id': 'mock5',
        'name': 'Hotel California',
        'artists': [{'name': 'Eagles'}],
        'album': {'name': 'Hotel California', 'release_date': '1976-12-08'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock5'
    },
    {
        'id': 'mock6',
        'name': 'Imagine',
        'artists': [{'name': 'John Lennon'}],
        'album': {'name': 'Imagine', 'release_date': '1971-10-11'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock6'
    },
    {
        'id': 'mock7',
        'name': 'Stairway to Heaven',
        'artists': [{'name': 'Led Zeppelin'}],
        'album': {'name': 'Led Zeppelin IV', 'release_date': '1971-11-08'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock7'
    },
    {
        'id': 'mock8',
        'name': 'Like a Rolling Stone',
        'artists': [{'name': 'Bob Dylan'}],
        'album': {'name': 'Highway 61 Revisited', 'release_date': '1965-08-30'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock8'
    },
    {
        'id': 'mock9',
        'name': 'Hey Jude',
        'artists': [{'name': 'The Beatles'}],
        'album': {'name': 'Hey Jude', 'release_date': '1968-08-26'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock9'
    },
    {
        'id': 'mock10',
        'name': 'Purple Rain',
        'artists': [{'name': 'Prince'}],
        'album': {'name': 'Purple Rain', 'release_date': '1984-06-25'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock10'
    },
    {
        'id': 'mock11',
        'name': "What's Going On",
        'artists': [{'name': 'Marvin Gaye'}],
        'album': {'name': "What's Going On", 'release_date': '1971-05-21'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock11'
    },
    {
        'id': 'mock12',
        'name': 'Superstition',
        'artists': [{'name': 'Stevie Wonder'}],
        'album': {'name': 'Talking Book', 'release_date': '1972-10-28'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock12'
    },
    {
        'id': 'mock13',
        'name': 'Thriller',
        'artists': [{'name': 'Michael Jackson'}],
        'album': {'name': 'Thriller', 'release_date': '1982-11-30'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock13'
    },
    {
        'id': 'mock14',
        'name': 'Born to Run',
        'artists': [{'name': 'Bruce Springsteen'}],
        'album': {'name': 'Born to Run', 'release_date': '1975-08-25'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock14'
    },
    {
        'id': 'mock15',
        'name': 'Respect',
        'artists': [{'name': 'Aretha Franklin'}],
        'album': {'name': 'I Never Loved a Man the Way I Love You', 'release_date': '1967-03-10'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock15'
    },
    {
        'id': 'mock16',
        'name': 'Johnny B. Goode',
        'artists': [{'name': 'Chuck Berry'}],
        'album': {'name': 'Chuck Berry Is on Top', 'release_date': '1958-03-31'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock16'
    },
    {
        'id': 'mock17',
        'name': 'Good Vibrations',
        'artists': [{'name': 'The Beach Boys'}],
        'album': {'name': 'Smiley Smile', 'release_date': '1966-10-10'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock17'
    },
    {
        'id': 'mock18',
        'name': 'I Want to Hold Your Hand',
        'artists': [{'name': 'The Beatles'}],
        'album': {'name': 'Meet the Beatles!', 'release_date': '1963-11-29'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock18'
    },
    {
        'id': 'mock19',
        'name': 'London Calling',
        'artists': [{'name': 'The Clash'}],
        'album': {'name': 'London Calling', 'release_date': '1979-12-14'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock19'
    },
    {
        'id': 'mock20',
        'name': 'Every Breath You Take',
        'artists': [{'name': 'The Police'}],
        'album': {'name': 'Synchronicity', 'release_date': '1983-05-20'},
        'preview_url': 'https://p.scdn.co/mp3-preview/mock20'
    }
]


def filter_mock_songs(query: str = None):
    """
    Filter mock songs based on query.
    
    Args:
        query: Search term (genre, artist, etc.)
        
    Returns:
        List of filtered songs
    """
    if not query:
        return MOCK_SONGS.copy()
    
    query_lower = query.lower()
    
    # Simple filtering by artist or decade
    if 'rock' in query_lower:
        return [s for s in MOCK_SONGS if any(
            artist in s['artists'][0]['name'] 
            for artist in ['Queen', "Guns N' Roses", 'Nirvana', 'Led Zeppelin', 'The Clash']
        )]
    elif 'pop' in query_lower:
        return [s for s in MOCK_SONGS if any(
            artist in s['artists'][0]['name']
            for artist in ['Michael Jackson', 'Prince', 'The Beatles', 'The Beach Boys']
        )]
    elif '80s' in query_lower or '1980' in query_lower:
        return [s for s in MOCK_SONGS if s['album']['release_date'].startswith('198')]
    elif '70s' in query_lower or '1970' in query_lower:
        return [s for s in MOCK_SONGS if s['album']['release_date'].startswith('197')]
    elif '60s' in query_lower or '1960' in query_lower:
        return [s for s in MOCK_SONGS if s['album']['release_date'].startswith('196')]
    else:
        # Try to match artist name
        matching = [s for s in MOCK_SONGS if query_lower in s['artists'][0]['name'].lower()]
        return matching if matching else MOCK_SONGS.copy()
