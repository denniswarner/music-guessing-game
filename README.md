# 🎵 Spotify Music Guessing Game

A fun music guessing game for you and your friends using Spotify's official API with **10-second preview clips**!

## 📋 Requirements

- **Python 3.8+** (3.8, 3.9, 3.10, 3.11, or 3.12)
- **Spotify Account** (free account works!)
- **ffmpeg** (optional, for 10-second clips)

## 🌐 **NEW: Web Version Available!**

You can now play in your browser with a beautiful modern UI! 

**Quick Start:**
```bash
# Terminal 1: Start backend
./start-backend.sh

# Terminal 2: Start frontend
./start-frontend.sh
```

Then open **http://localhost:3000** in your browser.

👉 **See [WEB_SETUP.md](WEB_SETUP.md) for complete web version setup guide**

---

## 🚀 Quick Setup (CLI Version)

### 1. Get Spotify API Credentials (Free!)

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account (free account works fine)
3. Click **"Create an App"**
4. Fill in:
   - App name: "Music Guessing Game" (or whatever you like)
   - App description: "Personal music game"
   - Check the box to agree to terms
5. Click **"Create"**
6. You'll see your **Client ID** and **Client Secret** (click "Show Client Secret")
7. Keep these handy - you'll need them to run the game!

### 2. Install Python Dependencies

Make sure you have Python 3.8 or higher installed:

```bash
python --version  # Should show 3.8 or higher
```

Install dependencies:

```bash
pip install -r requirements.txt
```

**Note:** For playing 10-second clips directly in the terminal, you'll also need ffmpeg:
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt-get install ffmpeg`
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)

(If you don't install ffmpeg, the game will open 30-second clips in your browser instead)

### 3. Configure Your Credentials

**Option A: Use .env file (Recommended)**

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   SPOTIFY_CLIENT_ID=your_actual_client_id
   SPOTIFY_CLIENT_SECRET=your_actual_client_secret
   ```

**Option B: Enter manually when prompted**

The game will ask for your credentials when you run it if no `.env` file is found.

### 4. Run the Game!

**Refactored version (recommended):**
```bash
python music_guessing_game_refactored.py
```

**Original version:**
```bash
python music_guessing_game.py
```

**Stubbed/Mock version (no API needed):**
```bash
python music_guessing_game_stubbed.py
```

## 🎮 How to Play

1. **Run the script** and enter your Spotify credentials when prompted
2. **Choose a game mode:**
   - **Genre/Keyword**: Search for songs by genre (rock, pop, jazz) or era (90s, 2000s)
   - **Playlist**: Use any public Spotify playlist URL
   - **Artist**: Play with songs from a specific artist
3. **Listen to the preview** (opens in your browser automatically)
4. **Make your guess!**
   - First guess: 2 points
   - Second guess (after artist hint): 1 point
5. **Compete with friends** for the highest score!

## 🎯 Game Tips

- **For parties:** Use a genre everyone knows (like "pop" or "90s")
- **For music nerds:** Try specific artists or deep-cut playlists
- **Difficulty levels:**
  - Easy: Current pop hits
  - Medium: 80s/90s classics
  - Hard: Indie, jazz, or specific niche genres

## 📝 Example Game Modes

**Genre Search:**
- "rock"
- "hip hop"
- "jazz"
- "90s"
- "Christmas"

**Playlist URL:**
Just copy any Spotify playlist link like:
`https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M`

**Artist:**
- "Taylor Swift"
- "The Beatles"
- "Drake"

## ⚙️ Features

### Core Features
- ✅ Uses official Spotify API (100% legal!)
- ✅ 10-second preview clips (perfect challenge length!)
- ✅ Hints system (album, year, artist)
- ✅ Score tracking
- ✅ Multiple game modes
- ✅ No music download required
- ✅ Modular architecture for easy testing and maintenance
- ✅ Comprehensive test suite with pytest
- ✅ Environment variable support (.env files)

### Web Version Features ✨
- ✅ Beautiful modern UI with Next.js + React
- ✅ TypeScript for type safety
- ✅ Tailwind CSS + Shadcn/ui components
- ✅ Smooth animations with Framer Motion
- ✅ Real-time audio player with controls
- ✅ Responsive design (mobile + desktop)
- ✅ Dark mode support
- ✅ FastAPI backend with REST API
- ✅ Interactive API documentation

## 🏗️ Project Structure

The project uses a modular architecture for maintainability:

```
music_guessing_game/
├── src/                          # Core modules
│   ├── spotify_client.py         # Spotify API interactions
│   ├── game_engine.py            # Game logic and scoring
│   └── audio_player.py           # Audio playback
├── tests/                        # Unit tests
│   ├── test_spotify_client.py
│   ├── test_game_engine.py
│   └── test_audio_player.py
├── music_guessing_game_refactored.py  # Main entry (modular)
├── music_guessing_game.py        # Original version
├── music_guessing_game_stubbed.py  # Mock version for testing
├── requirements.txt              # Python dependencies
├── .env.example                  # Credentials template
├── PLANNING.md                   # Architecture docs
└── TASK.md                       # Task tracking
```

## 🧪 Running Tests

Run the test suite:

```bash
pytest
```

Run with coverage report:

```bash
pytest --cov=src tests/
```

Run specific test file:

```bash
pytest tests/test_game_engine.py
```

## 🔧 Troubleshooting

**"No songs with previews found"**
- Not all songs have preview clips on Spotify
- Try a different genre or more popular artists

**"Authentication failed"**
- Double-check your Client ID and Client Secret
- Make sure you copied them correctly (no extra spaces)
- Verify your `.env` file format matches `.env.example`

**"Module not found"**
- Make sure you're using Python 3.8+
- Run `pip install -r requirements.txt`
- Try creating a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```

**"Cannot import from src"**
- Make sure you're running from the project root directory
- Try: `python -m music_guessing_game_refactored`

## 👩‍💻 Development

### Contributing

1. Check `PLANNING.md` for architecture and design decisions
2. Check `TASK.md` for current tasks and project status
3. Write tests for new features
4. Keep files under 500 lines
5. Follow PEP 8 style guide

### Running in Development

Install development dependencies:

```bash
pip install -r requirements.txt
```

Run tests with verbose output:

```bash
pytest -v
```

## 🎉 Have Fun!

Perfect for:
- Party games
- Road trips
- Music trivia nights
- Testing your music knowledge
- Learning Python project structure

## 📄 License

This is a personal/educational project. Spotify API usage complies with their Developer Terms. Preview clips are provided by Spotify and are ≤30 seconds per their license.

---

Enjoy the game! 🎵🎮

For more details, see:
- `PLANNING.md` - Architecture and design decisions
- `TASK.md` - Current tasks and project roadmap
