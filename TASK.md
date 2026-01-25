# 📋 Task List - Music Guessing Game

**Project:** Spotify Music Guessing Game  
**Started:** January 25, 2026  
**Status:** Active Development

---

## ✅ Completed Tasks

### Initial Setup (January 25, 2026)
- [x] Create basic game implementation (`music_guessing_game.py`)
- [x] Create stubbed/mock version for testing (`music_guessing_game_stubbed.py`)
- [x] Write comprehensive README with setup instructions
- [x] Define Python dependencies in `requirements.txt`
- [x] Implement 10-second audio preview playback
- [x] Add three game modes (genre, playlist, artist)
- [x] Implement scoring system with hints

### Project Structure & Documentation (January 25, 2026)
- [x] Create PLANNING.md with architecture and design decisions
- [x] Create TASK.md for ongoing task tracking

---

## 🚧 In Progress

### Refactoring & Modularization (January 25, 2026)
- [ ] Split monolithic file into modular components
  - [ ] Create `src/` directory structure
  - [ ] Extract `SpotifyClient` class → `src/spotify_client.py`
  - [ ] Extract `GameEngine` class → `src/game_engine.py`
  - [ ] Extract audio functions → `src/audio_player.py`
  - [ ] Update main entry point to import from modules
  - [ ] Ensure backward compatibility

### Testing Infrastructure (January 25, 2026)
- [ ] Set up pytest testing framework
  - [ ] Create `tests/` directory
  - [ ] Add `pytest` and `pytest-cov` to requirements
  - [ ] Write unit tests for SpotifyClient
  - [ ] Write unit tests for GameEngine
  - [ ] Write unit tests for audio player
  - [ ] Achieve 80%+ code coverage

### Configuration & Environment (January 25, 2026)
- [ ] Add environment variable support
  - [ ] Create `.env.example` template
  - [ ] Add `python-dotenv` dependency
  - [ ] Update code to load credentials from `.env`
  - [ ] Update README with `.env` setup instructions
  - [ ] Add `.env` to `.gitignore`

### Version Control (January 25, 2026)
- [ ] Initialize git repository
  - [ ] Run `git init`
  - [ ] Create `.gitignore` for Python projects
  - [ ] Make initial commit
  - [ ] Add remote repository (if applicable)

### Documentation Updates (January 25, 2026)
- [ ] Specify Python version requirements
  - [ ] Add `.python-version` file
  - [ ] Update README with Python 3.8+ requirement
  - [ ] Document ffmpeg installation per OS

---

## 📝 Backlog (Future Tasks)

### Code Quality
- [ ] Add type hints to all functions
- [ ] Add docstrings to all public methods
- [ ] Run Black formatter on all files
- [ ] Set up pre-commit hooks for linting

### Features
- [ ] Add command-line argument parsing (click/argparse)
  - [ ] `--mode` flag for game mode selection
  - [ ] `--rounds` flag for number of rounds
  - [ ] `--difficulty` flag for future difficulty levels
- [ ] Add configuration file support (config.yaml)
- [ ] Implement score persistence (SQLite or JSON)
- [ ] Add difficulty levels (easy/medium/hard)

### User Experience
- [ ] Add colorized terminal output (colorama/rich)
- [ ] Improve error messages with suggestions
- [ ] Add progress indicators for API calls
- [ ] Add keyboard shortcuts (skip, quit, replay)

### Testing
- [ ] Add integration tests for full game flow
- [ ] Add performance tests for API calls
- [ ] Test cross-platform compatibility (Windows/Mac/Linux)

### DevOps
- [ ] Add CI/CD pipeline (GitHub Actions)
- [ ] Add automated testing on PR
- [ ] Add code coverage reporting
- [ ] Create release workflow

---

## 🔍 Discovered During Work

### Issues to Address
- [ ] Improve substring matching for song guesses (fuzzy matching?)
- [ ] Handle rate limiting from Spotify API
- [ ] Add timeout for audio download (slow connections)
- [ ] Validate playlist URLs before API call
- [ ] Handle songs with no preview URL more gracefully

### Technical Debt
- [ ] Refactor `play_round()` method (too long, multiple responsibilities)
- [ ] Extract hint display logic into separate method
- [ ] Add constants for magic numbers (score values, timeouts)
- [ ] Replace print statements with proper logging framework

---

## 🎯 Current Sprint Goals

**Sprint 1: Foundational Improvements (January 25-31, 2026)**
1. Complete modular refactoring
2. Set up testing infrastructure with basic tests
3. Initialize git repository
4. Add environment variable support
5. Update documentation

**Success Criteria:**
- All tests passing
- Code split into logical modules
- Git history established
- `.env` file support working

---

## 📊 Progress Tracking

| Category | Tasks Complete | Tasks Total | % Complete |
|----------|----------------|-------------|------------|
| Setup | 7 | 7 | 100% |
| Documentation | 2 | 2 | 100% |
| Refactoring | 0 | 6 | 0% |
| Testing | 0 | 6 | 0% |
| Configuration | 0 | 5 | 0% |
| Version Control | 0 | 4 | 0% |
| **TOTAL** | **9** | **30** | **30%** |

---

## 💡 Notes & Reminders

- Keep all files under 500 lines
- Write tests BEFORE marking features complete
- Update this file immediately after completing tasks
- Add new tasks as they're discovered
- Reference PLANNING.md for architecture decisions

---

**Last Updated:** January 25, 2026
