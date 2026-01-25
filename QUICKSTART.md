# ⚡ Quick Start Guide

## 🎯 Get Playing in 5 Minutes!

### Step 1: Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

Optional (for 10-second clips):
```bash
# Mac
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### Step 2: Configure Credentials (2 min)

1. Get your Spotify API keys:
   - Go to https://developer.spotify.com/dashboard
   - Log in and click "Create an App"
   - Copy your Client ID and Client Secret

2. Create your `.env` file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and paste your credentials:
   ```
   SPOTIFY_CLIENT_ID=paste_your_client_id_here
   SPOTIFY_CLIENT_SECRET=paste_your_client_secret_here
   ```

### Step 3: Play! (2 min)

```bash
python music_guessing_game_refactored.py
```

That's it! 🎉

---

## 🎮 Quick Game Tips

**Easy Mode:** Try "pop" or "90s"  
**Medium Mode:** Try "rock" or specific artists  
**Hard Mode:** Try "jazz" or deep-cut playlists

**Pro Tip:** The stubbed version works without API credentials:
```bash
python music_guessing_game_stubbed.py
```

---

## 🧪 Verify Setup (Optional)

Run tests to ensure everything works:

```bash
pytest -v
```

Expected: 52 tests passed ✅

---

## 📚 Learn More

- **README.md** - Full setup guide
- **PLANNING.md** - Architecture details
- **ARCHITECTURE.md** - System diagrams
- **SETUP_SUMMARY.md** - Complete statistics

---

**Need Help?**

Check the troubleshooting section in README.md or run the stubbed version first to test without API.

🎵 Happy guessing! 🎵
