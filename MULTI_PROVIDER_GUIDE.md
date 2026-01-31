# Multi-Provider Music Support Guide

Your Music Guessing Game now supports **three music providers**:

1. **🎮 Demo Mode** - No credentials needed
2. **🎶 Deezer** - No credentials needed ⭐ **RECOMMENDED**
3. **🎵 Spotify** - Requires API credentials

---

## 🎶 Deezer (Recommended!)

### Why Choose Deezer?

- ✅ **No API credentials required** - Start playing immediately
- ✅ **30-second previews** (vs Spotify's 10 seconds)
- ✅ **Large music catalog** - Millions of songs
- ✅ **Easy to use** - Just select Deezer and play!
- ✅ **Free** - No API fees or limits for basic usage

### How to Use Deezer

1. Open the web frontend: http://localhost:3000
2. Select **"🎶 Deezer"** as your music provider
3. Choose your game mode:
   - **Genre**: Search by genre (e.g., "rock", "pop", "80s")
   - **Artist**: Search by artist name (e.g., "The Beatles", "Queen")
   - **Playlist**: Use a Deezer playlist URL or ID
4. Click **"Start Game"** and enjoy!

### Deezer Playlist Support

To use a Deezer playlist:

- **Full URL**: `https://www.deezer.com/playlist/1234567890`
- **Just the ID**: `1234567890`

Find playlists at: https://www.deezer.com/

---

## 🎵 Spotify

### Why Choose Spotify?

- Large music catalog
- Popular playlists
- Artist top tracks

### Setup Instructions

1. Go to https://developer.spotify.com/dashboard
2. Log in with your Spotify account
3. Click **"Create app"**
4. Fill in:
   - App name: "Music Guessing Game"
   - App description: "A fun music guessing game"
   - Redirect URI: `http://localhost:8888/callback`
5. Accept terms and click **"Save"**
6. Copy your **Client ID** and **Client Secret**

### How to Use Spotify

1. Open the web frontend: http://localhost:3000
2. Select **"🎵 Spotify"** as your music provider
3. Enter your Client ID and Client Secret
4. Choose your game mode and start playing!

### Known Issues

⚠️ **Note**: Spotify is currently limiting new integrations. You may see:
> "New integrations are currently on hold while we make updates to improve reliability and performance."

**Recommendation**: Use Deezer instead - it works great and requires no credentials!

---

## 🎮 Demo Mode

### Why Choose Demo Mode?

- Perfect for testing
- No internet required (uses mock data)
- 20 handpicked classic songs
- Great for learning how the game works

### How to Use Demo Mode

1. Open the web frontend: http://localhost:3000
2. Select **"🎮 Demo"** as your music provider
3. Optionally filter by:
   - Genre: "rock", "pop", "80s", "70s", "60s"
   - Artist: "Beatles", "Queen", "Michael Jackson", etc.
4. Start playing!

---

## 🆚 Provider Comparison

| Feature | Deezer | Spotify | Demo |
|---------|--------|---------|------|
| **Setup Difficulty** | ⭐ Easy | ⭐⭐⭐ Hard | ⭐ Easy |
| **Credentials Required** | ❌ No | ✅ Yes | ❌ No |
| **Preview Length** | 30 seconds | 10 seconds | Mock |
| **Catalog Size** | Millions | Millions | 20 songs |
| **Internet Required** | ✅ Yes | ✅ Yes | ❌ No |
| **Playlist Support** | ✅ Yes | ✅ Yes | ❌ No |
| **Genre Search** | ✅ Yes | ✅ Yes | Limited |
| **Artist Search** | ✅ Yes | ✅ Yes | Limited |

---

## 🚀 Quick Start

### Easiest Way (Deezer)

```bash
# 1. Start servers
./start-backend.sh
# In another terminal:
./start-frontend.sh

# 2. Open browser
open http://localhost:3000

# 3. Select "Deezer" and play!
```

### With Spotify Credentials

```bash
# 1. Get credentials from https://developer.spotify.com/dashboard
# 2. Start servers
./start-backend.sh
./start-frontend.sh

# 3. Open browser, select "Spotify", enter credentials
open http://localhost:3000
```

### Try Demo Mode First

```bash
# 1. Start servers
./start-backend.sh
./start-frontend.sh

# 2. Open browser, select "Demo"
open http://localhost:3000
```

---

## 🔧 Technical Details

### Architecture

The game uses a **provider abstraction layer**:

```
┌─────────────────┐
│  Frontend UI    │
│  (Provider      │
│   Selector)     │
└────────┬────────┘
         │
┌────────▼────────┐
│  FastAPI        │
│  Backend        │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│Spotify│ │ Deezer  │
│Client │ │ Client  │
└───────┘ └─────────┘
```

### Files Created

**Backend:**
- `src/base_music_client.py` - Abstract base class
- `src/deezer_client.py` - Deezer API client
- `src/spotify_client.py` - Updated to use base class

**Frontend:**
- Updated `frontend/src/lib/types.ts` - Provider types
- Updated `frontend/src/lib/api.ts` - Provider parameter
- Updated `frontend/src/components/game-setup.tsx` - Provider selector

---

## 🎯 Best Practices

### For Development
- Start with **Demo Mode** to test features
- Use **Deezer** for real music without credentials
- Use **Spotify** only if you already have credentials

### For Users
- **Recommend Deezer** - best balance of ease and features
- **Demo Mode** - great for first-time users
- **Spotify** - only if user has credentials ready

---

## 🐛 Troubleshooting

### "Failed to start game"
- Make sure backend is running: `./start-backend.sh`
- Check provider selection matches your credentials

### "No songs found"
- Try a different search term
- For playlists, verify the URL is correct
- Try switching providers

### Deezer not working
- Check your internet connection
- Deezer API may have rate limits (unlikely for normal use)
- Try Demo Mode as fallback

### Spotify errors
- Verify credentials are correct
- Check if Spotify API is accepting new apps
- Consider switching to Deezer

---

## 📚 Additional Resources

- **Deezer API Docs**: https://developers.deezer.com/
- **Spotify API Docs**: https://developer.spotify.com/documentation/web-api
- **Project README**: See `README.md` for general setup

---

## ✨ Future Enhancements

Potential additional providers:
- Apple Music API
- YouTube Music API  
- Last.fm API (metadata only)
- SoundCloud API

Want to add a provider? Follow the pattern in `src/base_music_client.py`!
