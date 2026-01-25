# 🏗️ Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Music Guessing Game                          │
│                   (Python 3.8+ Application)                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Entry Point Layer                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  music_guessing_game_refactored.py                       │  │
│  │  • Load credentials (.env or user input)                 │  │
│  │  • Initialize components                                 │  │
│  │  • Handle user interaction                               │  │
│  │  • Coordinate game flow                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Core Modules (src/)                        │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │ SpotifyClient    │  │  GameEngine      │  │ AudioPlayer  │ │
│  │                  │  │                  │  │              │ │
│  │ • authenticate   │  │ • play_round()   │  │ • play_clip()│ │
│  │ • search_songs() │  │ • validate_guess │  │ • fallback   │ │
│  │ • get_playlist() │  │ • calculate_score│  │ • cleanup    │ │
│  │ • get_artist()   │  │ • display_hints  │  │              │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│         │                       │                     │         │
└─────────│───────────────────────│─────────────────────│─────────┘
          │                       │                     │
          ▼                       ▼                     ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Spotify API     │  │  User Interface  │  │  Audio System    │
│  • Search        │  │  • Console I/O   │  │  • pydub/ffmpeg  │
│  • Playlists     │  │  • Prompts       │  │  • Browser       │
│  • Artist Info   │  │  • Score Display │  │                  │
│  • Preview URLs  │  │                  │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

---

## Component Interaction Flow

### 1. Game Initialization

```
User runs script
      │
      ▼
Load credentials from .env or prompt
      │
      ▼
Initialize SpotifyClient(client_id, client_secret)
      │
      ▼
Initialize AudioPlayer()
      │
      ▼
Initialize GameEngine()
      │
      ▼
Ready to play!
```

### 2. Game Round Flow

```
User selects mode (genre/playlist/artist)
      │
      ▼
SpotifyClient.get_songs_*()
      │
      ▼
Filter songs with preview URLs
      │
      ▼
GameEngine.play_game(songs, audio_player, num_rounds)
      │
      ├─→ For each round:
      │   │
      │   ├─→ GameEngine.play_round(song, audio_player)
      │   │        │
      │   │        ├─→ AudioPlayer.play_preview_clip(url, 10s)
      │   │        │        │
      │   │        │        ├─→ Try local playback (pydub)
      │   │        │        │        └─→ Download, trim, play
      │   │        │        │
      │   │        │        └─→ Fallback to browser
      │   │        │
      │   │        ├─→ Display hints (album, year)
      │   │        │
      │   │        ├─→ Get first guess
      │   │        │
      │   │        ├─→ Validate guess
      │   │        │
      │   │        ├─→ If wrong: show artist, get second guess
      │   │        │
      │   │        ├─→ Update score
      │   │        │
      │   │        └─→ Return result
      │   │
      │   └─→ Ask to continue
      │
      ▼
Display final results and statistics
```

---

## Data Flow

### Song Data Structure

```python
{
    'name': str,              # Song title
    'preview_url': str,       # MP3 preview URL (30s max)
    'artists': [              # List of artists
        {'name': str}
    ],
    'album': {
        'name': str,          # Album name
        'release_date': str   # YYYY-MM-DD format
    }
}
```

### Game State

```python
GameEngine {
    score: float             # 0.0 to N
    total_questions: int     # Round counter
    
    FIRST_GUESS_SCORE: 1.0   # Full points
    SECOND_GUESS_SCORE: 0.5  # Half points
    NO_GUESS_SCORE: 0.0      # No points
}
```

---

## Module Dependencies

```
music_guessing_game_refactored.py
    │
    ├─→ src.spotify_client
    │       └─→ spotipy
    │
    ├─→ src.game_engine
    │       └─→ (standard library)
    │
    ├─→ src.audio_player
    │       ├─→ pydub (optional)
    │       ├─→ requests (optional)
    │       └─→ webbrowser (fallback)
    │
    └─→ python-dotenv (optional)
```

### External Dependencies

| Package | Version | Purpose | Required |
|---------|---------|---------|----------|
| spotipy | 2.23.0 | Spotify API client | ✅ Yes |
| requests | 2.31.0 | HTTP downloads | ⚠️ For local audio |
| pydub | 0.25.1 | Audio processing | ⚠️ For local audio |
| python-dotenv | 1.0.0 | .env file support | 🔵 Optional |
| pytest | 7.4.3 | Testing framework | 🧪 Dev only |
| pytest-cov | 4.1.0 | Coverage reporting | 🧪 Dev only |

**System Dependencies:**
- ffmpeg (for pydub audio decoding)

---

## Testing Architecture

```
tests/
  │
  ├─→ test_spotify_client.py
  │      │
  │      ├─→ Mock spotipy.Spotify
  │      ├─→ Mock SpotifyClientCredentials
  │      └─→ Test all search methods
  │
  ├─→ test_game_engine.py
  │      │
  │      ├─→ Mock AudioPlayer
  │      ├─→ Mock user input (builtins.input)
  │      └─→ Test scoring, validation, game flow
  │
  └─→ test_audio_player.py
         │
         ├─→ Mock pydub components
         ├─→ Mock webbrowser
         ├─→ Mock file system operations
         └─→ Test playback and fallback
```

---

## Error Handling Strategy

### Layered Approach

```
┌─────────────────────────────────────────┐
│  User-Facing Layer                      │
│  • Friendly error messages              │
│  • Suggestions for fixes                │
│  • Graceful exits                       │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  Business Logic Layer                   │
│  • Validate inputs                      │
│  • Handle edge cases                    │
│  • Return empty lists on failure        │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  External API Layer                     │
│  • Catch API exceptions                 │
│  • Retry on transient failures          │
│  • Log errors (future enhancement)      │
└─────────────────────────────────────────┘
```

### Fallback Mechanisms

1. **Audio Playback:**
   - Try: pydub + ffmpeg (10s trimmed)
   - Fallback: Browser (30s full preview)

2. **Credentials:**
   - Try: .env file
   - Fallback: Interactive prompt

3. **Song Search:**
   - Filter: Only songs with preview URLs
   - Fallback: Try different search term

---

## Configuration Management

```
Environment Variables (.env)
    │
    ├─→ SPOTIFY_CLIENT_ID
    ├─→ SPOTIFY_CLIENT_SECRET
    └─→ (Future: DEFAULT_ROUNDS, DEFAULT_GENRE)
    
Python Version (.python-version)
    │
    └─→ 3.8.0 minimum

Requirements (requirements.txt)
    │
    ├─→ Core dependencies
    └─→ Development dependencies
```

---

## Security Model

```
┌──────────────────────────────────────────┐
│  Credentials Protection                  │
│                                          │
│  ✅ Never hardcoded                      │
│  ✅ .env excluded from git               │
│  ✅ .env.example as template             │
│  ✅ Runtime prompts as fallback          │
│  ✅ No credentials in logs/output        │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│  API Usage                               │
│                                          │
│  • Client Credentials flow (no OAuth)    │
│  • No access to user data                │
│  • Read-only operations                  │
│  • Preview clips ≤30s (Spotify license)  │
└──────────────────────────────────────────┘
```

---

## Performance Considerations

### API Calls
- **Batch operations:** Request 50 songs at once (Spotify limit)
- **Filtering:** Client-side filter for preview URLs
- **Rate limiting:** Future enhancement (not yet implemented)

### Audio Processing
- **Download once:** Temp file automatically cleaned up
- **Trim to 10s:** Reduces playback time and memory
- **Fallback:** Browser if local processing fails

### Memory Usage
- **Streaming:** Audio downloaded to temp file (not memory)
- **Cleanup:** Temp files removed after each round
- **State:** Minimal game state (2 variables)

---

## Future Architecture Enhancements

### Planned Improvements

```
┌──────────────────────────────────────────┐
│  Logging Layer (structlog)               │
│  • Debug logs                            │
│  • Error tracking                        │
│  • Performance metrics                   │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│  CLI Layer (click/argparse)              │
│  • --mode flag                           │
│  • --rounds flag                         │
│  • --config file                         │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│  Persistence Layer (SQLite)              │
│  • Score history                         │
│  • Leaderboards                          │
│  • Game sessions                         │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│  Web Interface (Flask/FastAPI)           │
│  • Browser-based UI                      │
│  • Multiplayer support                   │
│  • Real-time updates                     │
└──────────────────────────────────────────┘
```

---

## Testing Strategy

### Unit Tests (Current)
- Mock all external dependencies
- Test each module in isolation
- 52 tests covering core functionality

### Integration Tests (Future)
- Test component interactions
- Use real Spotify API (test account)
- Verify end-to-end flows

### Performance Tests (Future)
- Measure API response times
- Test with large playlists
- Memory usage profiling

---

## Deployment Options

### Current (Local)
```
User's Machine
    │
    ├─→ Python 3.8+ interpreter
    ├─→ pip install requirements
    └─→ python music_guessing_game_refactored.py
```

### Future Options

**Docker Container:**
```dockerfile
FROM python:3.8-slim
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "music_guessing_game_refactored.py"]
```

**PyPI Package:**
```bash
pip install music-guessing-game
music-game
```

**Standalone Executable:**
```bash
# Using PyInstaller
pyinstaller --onefile music_guessing_game_refactored.py
```

---

## Code Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Total Modules | 3 | ✅ |
| Average Lines/Module | 190 | ✅ |
| Test Coverage | TBD | 🔜 |
| Cyclomatic Complexity | Low | ✅ |
| Code Duplication | None | ✅ |
| Max Function Length | ~30 lines | ✅ |

---

**Architecture Status: Production Ready ✅**

The modular architecture provides:
- ✅ Clear separation of concerns
- ✅ Easy testing and maintenance
- ✅ Graceful error handling
- ✅ Extensible design for future features
