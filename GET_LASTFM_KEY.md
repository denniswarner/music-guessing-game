# 🔑 Get Your Last.fm API Key

The Last.fm integration requires a **free API key** to automatically populate song metadata (genre, mood, style).

## Why You Need This

Without a Last.fm API key, the auto-population features won't work. You'll need to manually categorize each song.

**Good news:** It's completely free and takes 2 minutes! ⏱️

---

## Step-by-Step Guide

### 1. Visit Last.fm API Page
Go to: **https://www.last.fm/api/account/create**

### 2. Log In or Sign Up
- If you have a Last.fm account → Log in
- If not → Create a free account first

### 3. Fill Out the Application Form

#### Application Name
```
Music Guessing Game
```

#### Application Description
```
Personal music guessing game with custom song list management
```

#### Application Homepage URL
```
http://localhost:3000
```
(or just use `http://localhost` if it doesn't accept :3000)

#### Callback URL
```
Leave blank (not needed for API access)
```

### 4. Accept Terms & Submit
- ✅ Check "I agree to the Terms of Service"
- Click **"Submit"**

### 5. Copy Your API Key
You'll see two keys:
- **API Key** ← Copy this one! 🎯
- **Shared Secret** ← Not needed

### 6. Add to Your `.env` File

1. **Open** (or create) `.env` in your project root:
   ```bash
   /Volumes/Schmitty/Projects/My Apps/Music Guessing Game/.env
   ```

2. **Add this line:**
   ```
   LASTFM_API_KEY=your_actual_api_key_here
   ```

3. **Replace** `your_actual_api_key_here` with the key you copied

4. **Save** the file

### 7. Restart Backend Server

Kill the current backend and restart it:

```bash
# In terminal
cd "/Volumes/Schmitty/Projects/My Apps/Music Guessing Game"
./start-backend.sh
```

Or manually:
```bash
cd backend
python3 run.py
```

---

## ✅ Test It Works

1. Go to **http://localhost:3000/admin**
2. Click **"Add Songs"**
3. Search for **"Queen"**
4. Click on **"Bohemian Rhapsody"**
5. You should see:
   ```
   ⏳ Fetching metadata from Last.fm...
   
   ✨ Metadata Auto-Populated!
   Genre: Rock
   Mood: Epic
   Style: Classic
   Last.fm tags: rock · classic rock · progressive rock
   ```

---

## 🔍 Troubleshooting

### "Fetching metadata" but fields stay empty

**Check backend logs:**
```bash
# Look for errors
cd backend
python3 run.py
```

**Common issues:**
- ❌ API key not in `.env` file
- ❌ Backend not restarted after adding key
- ❌ Typo in API key
- ❌ `.env` file in wrong location (must be in project root)

### Backend shows "403 Forbidden"
- Your API key is invalid or expired
- Get a new key from Last.fm

### Backend shows "Last.fm API key not configured"
- `.env` file doesn't exist or doesn't have `LASTFM_API_KEY`
- Backend needs restart after adding key

---

## 📝 Example `.env` File

Your complete `.env` file should look like this:

```bash
# Spotify API Credentials
SPOTIFY_CLIENT_ID=your_spotify_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_secret_here

# Last.fm API Key
LASTFM_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

---

## 💡 Benefits of Setting This Up

Once configured, you get:
- ✅ **Automatic genre detection** from Last.fm tags
- ✅ **Mood suggestions** based on community tags
- ✅ **Style categorization** using music metadata
- ✅ **Top 5 Last.fm tags** displayed for reference
- ✅ **Smart fallbacks** if data isn't available

---

## ⚠️ Rate Limits

Free Last.fm API has generous limits:
- **No daily limit** for standard API calls
- **No credit card** required
- **No expiration** on free tier

Perfect for personal projects! 🎉

---

## 🔗 Useful Links

- **Get API Key**: https://www.last.fm/api/account/create
- **Last.fm API Docs**: https://www.last.fm/api
- **Your API Account**: https://www.last.fm/api/accounts
- **Tag Browser**: https://www.last.fm/tags (see what tags Last.fm has)

---

**Questions?** Check the backend logs for error messages!

**Ready to go!** Once you have your API key configured, the auto-population will work seamlessly! 🎵✨
