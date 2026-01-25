# 🎮 Demo Mode Guide

**Play instantly without Spotify credentials!**

---

## 🎉 What is Demo Mode?

Demo Mode lets you experience the full Music Guessing Game web interface **without needing Spotify API credentials**. Perfect while Spotify has paused new app creation!

---

## ✨ Features

### What You Get
- ✅ **20 Classic Songs** from legendary artists
- ✅ **Full Web UI** with beautiful design
- ✅ **All Game Modes** (genre, artist filtering)
- ✅ **Complete Game Experience** (hints, scoring, statistics)
- ✅ **No Setup Required** - just click and play!

### Song Collection
- Queen - Bohemian Rhapsody
- Michael Jackson - Billie Jean & Thriller
- Guns N' Roses - Sweet Child O Mine  
- Nirvana - Smells Like Teen Spirit
- Eagles - Hotel California
- John Lennon - Imagine
- Led Zeppelin - Stairway to Heaven
- Bob Dylan - Like a Rolling Stone
- The Beatles - Hey Jude & I Want to Hold Your Hand
- Prince - Purple Rain
- And 10 more classics!

---

## 🚀 How to Use

### Step 1: Start the Servers

**Terminal 1 - Backend:**
```bash
./start-backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start-frontend.sh
```

### Step 2: Open the Game

Visit **http://localhost:3000** in your browser

### Step 3: Enable Demo Mode

1. Look for the **"🎮 Demo Mode"** card at the top
2. Click **"Enable"** button
3. The Spotify credential fields will disappear!

### Step 4: Choose Your Game

**Genre Mode:**
- Try: `rock`, `pop`, `80s`, `70s`, `60s`
- Or leave blank for all 20 songs

**Artist Mode:**
- Try: `Beatles`, `Queen`, `Michael Jackson`, `Nirvana`
- Or leave blank for all 20 songs

**Playlist Mode:**
- Not available in demo mode (grayed out)

### Step 5: Set Rounds & Play!

- Choose 1-20 rounds (limited to available songs)
- Click **"Start Game"**
- Enjoy! 🎵

---

## 🎯 Game Play Tips

### In Demo Mode:
- **No Audio Playback** - Mock songs don't have real preview URLs
- **Use Your Knowledge** - That's the challenge!
- **Hints Available** - Album, year, and artist hints still work
- **Full Scoring** - Same 2-point/1-point system

### Strategy:
1. Read the album name carefully
2. Check the release year
3. Make your first guess
4. Use the artist hint if needed
5. Make your second guess

---

## 🔄 Switching Modes

You can easily switch between Demo Mode and Real Mode:

### To Enable Demo Mode:
1. Click the **"Enable"** button in the Demo Mode card
2. Credentials fields disappear
3. Query becomes optional

### To Disable Demo Mode:
1. Click the **"Enabled"** button to toggle off
2. Credentials fields reappear
3. Enter your Spotify API credentials

---

## 📊 Available Songs by Category

### Rock
- Queen - Bohemian Rhapsody
- Guns N' Roses - Sweet Child O Mine
- Nirvana - Smells Like Teen Spirit
- Led Zeppelin - Stairway to Heaven
- The Clash - London Calling

### Pop
- Michael Jackson - Billie Jean, Thriller
- Prince - Purple Rain
- The Beatles - Hey Jude, I Want to Hold Your Hand
- The Beach Boys - Good Vibrations

### Soul/R&B
- Aretha Franklin - Respect
- Marvin Gaye - What's Going On
- Stevie Wonder - Superstition

### Classic Rock
- Eagles - Hotel California
- Bruce Springsteen - Born to Run
- Bob Dylan - Like a Rolling Stone
- Chuck Berry - Johnny B. Goode
- The Police - Every Breath You Take

### By Decade

**60s:**
- Chuck Berry - Johnny B. Goode (1958)
- Bob Dylan - Like a Rolling Stone (1965)
- The Beatles - I Want to Hold Your Hand (1963)
- The Beach Boys - Good Vibrations (1966)
- Aretha Franklin - Respect (1967)
- The Beatles - Hey Jude (1968)

**70s:**
- John Lennon - Imagine (1971)
- Led Zeppelin - Stairway to Heaven (1971)
- Marvin Gaye - What's Going On (1971)
- Stevie Wonder - Superstition (1972)
- Queen - Bohemian Rhapsody (1975)
- Bruce Springsteen - Born to Run (1975)
- Eagles - Hotel California (1976)
- The Clash - London Calling (1979)

**80s:**
- Michael Jackson - Billie Jean (1982)
- Michael Jackson - Thriller (1982)
- The Police - Every Breath You Take (1983)
- Prince - Purple Rain (1984)
- Guns N' Roses - Sweet Child O Mine (1987)

**90s:**
- Nirvana - Smells Like Teen Spirit (1991)

---

## 💡 Pro Tips

### Getting the Most Out of Demo Mode

1. **Practice Mode**: Use demo mode to practice before using real Spotify
2. **Learn the Songs**: Great way to familiarize yourself with classics
3. **Test the UI**: See how the game works before getting API credentials
4. **Party Mode**: Play with friends who know these songs well
5. **Educational**: Great for music history lessons!

### Filtering Tips

- Search `rock` for harder rock songs
- Search `pop` for more mainstream hits
- Search `80s` for that decade's classics
- Search artist names for specific artists
- Leave blank for maximum variety (all 20 songs)

---

## ❓ FAQ

### Q: Why no audio playback in demo mode?
**A:** Mock songs don't have real Spotify preview URLs. The game focuses on testing your music knowledge!

### Q: Can I add more songs to demo mode?
**A:** Yes! Edit `backend/app/mock_data.py` to add more songs to the `MOCK_SONGS` list.

### Q: Does demo mode save my progress?
**A:** No, like the real mode, sessions are in-memory only.

### Q: Will my score count toward leaderboards?
**A:** There are no leaderboards yet (future feature), but your score shows at the end!

### Q: Can I use playlist mode in demo?
**A:** No, playlist mode requires real Spotify API access.

### Q: How do I get real Spotify credentials?
**A:** Visit https://developer.spotify.com/dashboard when Spotify reopens app creation.

---

## 🔄 When to Use Each Mode

### Use Demo Mode When:
- ✅ Spotify app creation is paused
- ✅ You want to test the game quickly
- ✅ Playing with friends who know classic songs
- ✅ Learning the UI before getting credentials
- ✅ Teaching music history

### Use Real Mode When:
- ✅ You have Spotify API credentials
- ✅ You want custom playlists
- ✅ You want specific genres/artists
- ✅ You want audio playback
- ✅ You want more song variety

---

## 🎵 Have Fun!

Demo Mode gives you the full game experience without the wait. Perfect for:
- Testing the game
- Playing while waiting for Spotify
- Parties with music buffs
- Quick gaming sessions

**Enjoy!** 🎮🎉

---

## 📚 Related Docs

- **Setup Guide**: See `WEB_SETUP.md`
- **Main README**: See `README.md`
- **Architecture**: See `ARCHITECTURE.md`
