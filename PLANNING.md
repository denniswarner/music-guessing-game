# 🎵 Music Guessing Game - Project Planning

**Created:** January 25, 2026  
**Project Type:** Python CLI Game  
**Primary Language:** Python 3.8+

---

## 📋 Project Overview

A command-line music trivia game that integrates with Spotify's API to play 10-second song previews. Players guess song titles based on audio clips and hints, with a scoring system that rewards accuracy.

### Core Purpose
- Provide an entertaining music trivia experience for individuals and groups
- Leverage Spotify's extensive music catalog and preview system
- Offer multiple game modes to accommodate different preferences

---

## 🏗️ Architecture

### Modular Structure

The project follows a **modular architecture** to maintain code clarity and testability:

```
music_guessing_game/
├── src/
│   ├── __init__.py
│   ├── spotify_client.py      # Spotify API interactions
│   ├── game_engine.py          # Game logic, scoring, rounds
│   └── audio_player.py         # Audio playback functionality
├── tests/
│   ├── __init__.py
│   ├── test_spotify_client.py
│   ├── test_game_engine.py
│   └── test_audio_player.py
├── music_guessing_game.py      # Main entry point
├── music_guessing_game_stubbed.py  # Mock version for testing
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── PLANNING.md
└── TASK.md
```

### Component Responsibilities

#### 1. **spotify_client.py**
- Authenticate with Spotify API using Client Credentials flow
- Search songs by genre/keyword
- Fetch playlist tracks
- Retrieve artist top tracks
- Filter songs that have preview URLs

#### 2. **game_engine.py**
- Manage game state (score, round count)
- Handle round progression
- Process user guesses with flexible matching
- Display hints (album, year, artist)
- Calculate final scores and rankings

#### 3. **audio_player.py**
- Download and trim audio previews to 10 seconds
- Play audio using pydub/ffmpeg (if available)
- Fallback to browser playback
- Clean up temporary files

---

## 🎨 Design Decisions

### 1. **Single Entry Point**
- `music_guessing_game.py` serves as the main CLI interface
- Imports modular components from `src/`
- Keeps user interaction separate from business logic

### 2. **Preview Duration: 10 Seconds**
- Spotify provides 30-second previews by default
- 10 seconds chosen as optimal challenge length
- Requires pydub + ffmpeg for trimming
- Graceful degradation to 30s browser playback if unavailable

### 3. **Scoring System**
```
First guess correct:  2 points (1.0 added to score)
Second guess correct: 1 point (0.5 added to score)
Incorrect:            0 points
```
- Two-try system balances difficulty and frustration
- Hints revealed progressively (album/year → artist)

### 4. **Mock/Stubbed Version**
- `music_guessing_game_stubbed.py` provides offline testing
- Uses 20 classic songs as mock database
- No API credentials required
- Useful for development and when Spotify is unavailable

### 5. **Flexible Answer Matching**
- Case-insensitive comparison
- Substring matching (e.g., "bohemian" matches "Bohemian Rhapsody")
- Reduces frustration from minor typos

---

## 🔐 Security & Configuration

### Environment Variables
- Spotify credentials stored in `.env` file (not committed)
- `.env.example` provides template
- Runtime prompt as fallback if `.env` not found

### No User Authentication Required
- Uses Spotify Client Credentials (app-level auth)
- No OAuth flow needed
- No access to user's personal data

---

## 🧪 Testing Strategy

### Unit Tests (pytest)
Each module has corresponding tests:

1. **test_spotify_client.py**
   - Mock API responses
   - Test search filtering
   - Test preview URL validation
   - Test error handling (invalid credentials, rate limits)

2. **test_game_engine.py**
   - Test scoring calculations
   - Test guess matching logic (case, substrings)
   - Test round progression
   - Test edge cases (0 songs, empty guesses)

3. **test_audio_player.py**
   - Mock audio downloads
   - Test 10-second trimming
   - Test fallback behavior
   - Test temp file cleanup

### Test Coverage Goal
- Minimum 80% code coverage
- All core game logic fully tested
- Edge cases and error conditions covered

---

## 📦 Dependencies

### Core Dependencies
- **spotipy** (2.23.0): Spotify API client
- **requests** (2.31.0): HTTP library (transitive, but explicit)
- **pydub** (0.25.1): Audio manipulation
- **ffmpeg** (external): Audio codec (optional but recommended)

### Development Dependencies
- **pytest** (≥7.0.0): Testing framework
- **pytest-cov**: Coverage reporting
- **python-dotenv**: Environment variable management

---

## 🎯 Code Style & Conventions

### Python Standards
- **PEP 8** compliance
- **Type hints** for all function signatures
- **Docstrings** (Google style) for all public functions
- **Black** formatter (line length: 88)

### File Length Constraint
- **Maximum 500 lines per file**
- Split into modules if approaching limit
- Reason: Maintainability and testability

### Naming Conventions
- **Classes**: PascalCase (e.g., `MusicGuessingGame`)
- **Functions/variables**: snake_case (e.g., `play_preview_clip`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MOCK_SONGS`)
- **Private methods**: Leading underscore (e.g., `_validate_guess`)

### Import Organization
```python
# Standard library
import os
import random

# Third-party
import spotipy
from pydub import AudioSegment

# Local modules
from src.spotify_client import SpotifyClient
from src.game_engine import GameEngine
```

### Error Handling
- Use try/except for external API calls
- Provide user-friendly error messages
- Log errors for debugging (future enhancement)
- Graceful degradation (e.g., browser fallback for audio)

### Comments
- Explain **why**, not **what**
- Use `# Reason:` prefix for complex logic explanations
- Document assumptions and edge cases

---

## 🚀 Future Enhancements

### Potential Features (Not Currently Scoped)
1. **Multiplayer mode**: Pass-and-play or networked gameplay
2. **Difficulty levels**: Adjust hint timing and scoring
3. **Leaderboard**: Persistent score tracking
4. **Custom playlists**: Save favorite game configurations
5. **Audio visualization**: Terminal-based waveform display
6. **Spotify OAuth**: Access user's personal playlists
7. **Web interface**: Flask/FastAPI frontend
8. **Database integration**: Store game history

### Technical Debt
- Add logging framework (structlog or loguru)
- Add CLI argument parsing (argparse or click)
- Add configuration file support (YAML/TOML)
- Internationalization (i18n)

---

## 🔄 Development Workflow

### Before Starting a Task
1. Check `TASK.md` for existing tasks
2. Add new task if not listed
3. Mark task as "In Progress"

### During Development
1. Write code following style guide
2. Add docstrings and type hints
3. Keep files under 500 lines
4. Add `# Reason:` comments for complex logic

### After Completing a Feature
1. Write/update unit tests
2. Run test suite (`pytest`)
3. Update `README.md` if user-facing changes
4. Mark task complete in `TASK.md`
5. Add discovered sub-tasks to `TASK.md`

### Git Workflow
- Descriptive commit messages
- Small, focused commits
- Don't commit secrets or `.env` files

---

## 📊 Success Metrics

### Functionality
- ✅ Game runs without errors on fresh install
- ✅ All three game modes work correctly
- ✅ Audio playback works (with fallback)
- ✅ Scoring system accurate

### Code Quality
- ✅ All tests passing
- ✅ 80%+ code coverage
- ✅ PEP 8 compliant
- ✅ All functions have docstrings

### User Experience
- ✅ Setup takes <5 minutes
- ✅ Clear error messages
- ✅ Intuitive CLI prompts
- ✅ Graceful handling of edge cases

---

## 📝 Notes

- This is a **personal/educational project** - not intended for commercial use
- Spotify API usage complies with their Developer Terms
- Preview clips are ≤30 seconds per Spotify's license
- No music files are permanently stored

---

**Last Updated:** January 25, 2026
