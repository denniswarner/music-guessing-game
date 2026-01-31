# Last.fm Integration 🎵

## Overview

The admin section now uses **Last.fm API** to automatically fetch rich metadata when adding songs to custom lists!

## ✨ What Gets Auto-Populated

When you select a song, Last.fm provides:

1. **Genre** - Rock, Pop, Hip Hop, Jazz, etc.
2. **Mood** - Upbeat, Chill, Energetic, Romantic, etc.
3. **Style** - Classic, Modern, Contemporary, Alternative, etc.
4. **Tags** - User-generated tags from Last.fm community

## 🚀 How It Works

1. You search for a song (via Deezer)
2. Select a song from results
3. **Last.fm is queried automatically** using artist + track name
4. Genre, Mood, and Style fields are populated
5. You can override any suggestions
6. Click "Add Song" to save

## 🔑 API Key (Optional)

### Using the Demo Key
A demo Last.fm API key is included by default. It works but has rate limits.

### Get Your Own (Recommended for Production)

1. **Go to:** https://www.last.fm/api/account/create
2. **Fill in:**
   - Application name: "Music Guessing Game"
   - Application description: "Custom song list management"
   - Application homepage: Your URL or "http://localhost:3000"
3. **Click "Submit"**
4. **Copy your API Key**
5. **Add to `.env` file:**
   ```
   LASTFM_API_KEY=your_api_key_here
   ```
6. **Restart backend server**

### No API Key Needed!
The system includes a demo key, so everything works out of the box! Getting your own key just removes rate limits.

---

## 📊 Tag Mapping

Last.fm returns user-generated tags. We map them to our categories:

### Genre Mapping
```
Last.fm Tag → Our Genre
---------------------------
"rock" → Rock
"pop" → Pop
"hip hop" → Hip Hop
"electronic" → Electronic
"jazz" → Jazz
etc.
```

### Mood Mapping
```
Last.fm Tag → Our Mood
---------------------------
"upbeat" → Upbeat
"chill" → Chill
"party" → Party
"sad" → Sad
"energetic" → Energetic
etc.
```

### Style Mapping
```
Last.fm Tag → Our Style
---------------------------
"classic" → Classic
"modern" → Modern
"indie" → Underground
"experimental" → Experimental
etc.
```

---

## 🎯 Examples

### Example 1: Bohemian Rhapsody
```
Song: Bohemian Rhapsody - Queen
Last.fm Tags: rock, classic rock, progressive rock

Result:
✓ Genre: Rock
✓ Style: Classic
✓ Mood: Epic (if tagged)
```

### Example 2: Uptown Funk
```
Song: Uptown Funk - Mark Ronson
Last.fm Tags: funk, dance, pop, party

Result:
✓ Genre: Funk
✓ Mood: Party
✓ Style: Contemporary
```

### Example 3: Clair de Lune
```
Song: Clair de Lune - Debussy
Last.fm Tags: classical, instrumental, relaxing

Result:
✓ Genre: Classical
✓ Mood: Relaxing
✓ Style: Classic
```

---

## 🔧 Technical Details

### Backend
- **File:** `backend/app/lastfm_client.py`
- **Endpoint:** `POST /api/admin/enrich-song`
- **Parameters:** artist, track, release_year (optional)

### API Call
```python
# Backend automatically calls Last.fm
enriched = lastfm_client.enrich_song_metadata(
    artist="Queen",
    track="Bohemian Rhapsody",
    release_year=1975
)

# Returns:
{
    "genre": "Rock",
    "mood": "Epic",
    "style": "Classic",
    "tags": ["rock", "classic rock", "progressive rock"]
}
```

### Frontend
- **File:** `frontend/src/components/admin/song-search.tsx`
- **Function:** `enrichSongMetadata()`
- Shows loading state while fetching
- Displays success message with tags
- Falls back to year-based logic if Last.fm fails

---

## 💡 Benefits

1. **Save Time** - No manual categorization needed
2. **Consistency** - Tags based on community consensus
3. **Accuracy** - Leverages Last.fm's music knowledge graph
4. **Flexibility** - Can still override any suggestion
5. **Free** - Last.fm API is completely free

---

## ⚠️ Limitations

1. **Coverage** - Very popular songs have best metadata
2. **Obscure Songs** - May have fewer/no tags
3. **Rate Limits** - Demo key has limits (get your own key)
4. **Accuracy** - User-generated tags may vary
5. **Internet Required** - Needs API access

---

## 🎨 UI Features

### Loading State
```
⏳ Fetching metadata from Last.fm...
```

### Success State
```
✨ Metadata Auto-Populated!
Genre, mood, and style have been suggested using Last.fm.

Last.fm tags: rock · classic rock · progressive rock · 70s
```

### Fallback
If Last.fm fails, uses year-based logic:
- Before 1980 → Classic
- 1980-2009 → Modern
- 2010+ → Contemporary

---

## 🔮 Future Enhancements

Potential additions:
- Artist bio/description
- Similar songs suggestions
- Popularity/playcount data
- Album art enrichment
- Multi-language support
- Batch enrichment

---

## 📖 Resources

- **Last.fm API Docs**: https://www.last.fm/api
- **Get API Key**: https://www.last.fm/api/account/create
- **Tag Browser**: https://www.last.fm/tags
- **Method Used**: `track.getTopTags`

---

**Enjoy automatic song categorization!** 🎵✨

The system will now intelligently populate Genre, Mood, and Style when you add songs!
