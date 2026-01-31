# Admin Features: Custom Song Lists

## 🎯 Overview

The Music Guessing Game now includes powerful **admin features** that allow you to create custom, curated song lists tailored to specific audiences and events!

## ✨ Key Features

### 1. **Custom Song Lists**
- Create unlimited custom song lists
- Categorize songs by decade, genre, style, mood, and difficulty
- Target specific audiences (Corporate Events, Birthday Parties, etc.)
- Track usage statistics

### 2. **Song Categorization**
- **Decade**: 1950s, 1960s, 1970s, 1980s, 1990s, 2000s, 2010s, 2020s
- **Genre**: Rock, Pop, Hip Hop, R&B, Jazz, Country, Electronic, etc.
- **Style**: Classic, Modern, Alternative, Mainstream, etc.
- **Mood**: Upbeat, Mellow, Energetic, Romantic, Party, Chill, etc.
- **Difficulty**: Easy, Medium, Hard

### 3. **Flexible Game Creation**
- Use entire custom lists
- Filter by any combination of categories
- Perfect for themed events

---

## 🚀 Quick Start

### Step 1: Create a Custom List

**API Request:**
```bash
curl -X POST http://localhost:8000/api/admin/lists \
  -H "Content-Type: application/json" \
  -d '{
    "name": "80s Rock Night",
    "description": "Classic rock hits from the 1980s",
    "target_audience": "Corporate Event",
    "primary_decade": "1980s",
    "primary_genre": "Rock"
  }'
```

**Response:**
```json
{
  "id": "abc-123-def",
  "name": "80s Rock Night",
  "songs": [],
  "created_at": "2026-01-31T...",
  ...
}
```

### Step 2: Search for Songs to Add

```bash
curl -X POST http://localhost:8000/api/admin/search-songs \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "deezer",
    "mode": "artist",
    "query": "Queen"
  }'
```

### Step 3: Add Songs with Categories

```bash
curl -X POST http://localhost:8000/api/admin/lists/abc-123-def/songs \
  -H "Content-Type: application/json" \
  -d '{
    "id": "song-123",
    "name": "Bohemian Rhapsody",
    "artist": "Queen",
    "album": "A Night at the Opera",
    "preview_url": "https://...",
    "decade": "1970s",
    "genre": "Rock",
    "style": "Classic",
    "mood": "Epic",
    "difficulty": "hard",
    "provider": "deezer"
  }'
```

### Step 4: Use in a Game

```bash
curl -X POST http://localhost:8000/api/game/start \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "custom",
    "mode": "custom",
    "custom_list_id": "abc-123-def",
    "num_rounds": 10
  }'
```

---

## 📚 API Reference

### List Management

#### `GET /api/admin/lists`
Get all custom lists (summaries).

**Query Parameters:**
- `active_only` (bool): Only return active lists

**Response:**
```json
[
  {
    "id": "abc-123",
    "name": "80s Rock Night",
    "song_count": 25,
    "primary_decade": "1980s",
    "times_played": 12,
    ...
  }
]
```

#### `POST /api/admin/lists`
Create a new custom list.

**Request Body:**
```json
{
  "name": "List Name",
  "description": "Description",
  "target_audience": "Corporate Event",
  "primary_decade": "1980s",
  "primary_genre": "Rock"
}
```

#### `GET /api/admin/lists/{list_id}`
Get full details of a custom list including all songs.

#### `PUT /api/admin/lists/{list_id}`
Update list metadata.

**Query Parameters:**
- `name`, `description`, `target_audience`, `primary_decade`, `primary_genre`, `is_active`

#### `DELETE /api/admin/lists/{list_id}`
Delete a custom list.

---

### Song Management

#### `POST /api/admin/lists/{list_id}/songs`
Add a song to a list.

**Request Body:**
```json
{
  "id": "song-123",
  "name": "Song Name",
  "artist": "Artist Name",
  "album": "Album Name",
  "preview_url": "https://...",
  "decade": "1980s",
  "genre": "Rock",
  "style": "Classic",
  "mood": "Upbeat",
  "difficulty": "medium",
  "provider": "deezer",
  "notes": "Great crowd pleaser"
}
```

#### `DELETE /api/admin/lists/{list_id}/songs/{song_id}`
Remove a song from a list.

#### `POST /api/admin/lists/filter`
Filter songs from a list by criteria.

**Request Body:**
```json
{
  "list_id": "abc-123",
  "decade": "1980s",
  "genre": "Rock",
  "mood": "Upbeat",
  "limit": 20
}
```

---

### Helper Endpoints

#### `GET /api/admin/categories/decades`
Get list of available decades.

#### `GET /api/admin/categories/genres`
Get list of available genres.

#### `GET /api/admin/categories/styles`
Get list of available styles.

#### `GET /api/admin/categories/moods`
Get list of available moods.

#### `POST /api/admin/search-songs`
Search for songs from providers (Deezer/Demo) to add to lists.

---

## 💡 Use Cases

### 1. **Corporate Event**
```json
{
  "name": "Tech Company Mixer",
  "target_audience": "Young Professionals",
  "primary_decade": "2010s",
  "primary_genre": "Pop"
}
```
**Song Tags:** Modern, Upbeat, Easy

### 2. **80s Theme Party**
```json
{
  "name": "Totally Rad 80s Night",
  "target_audience": "General Audience",
  "primary_decade": "1980s",
  "primary_genre": "Pop"
}
```
**Song Tags:** Classic, Party, Medium

### 3. **Family Game Night**
```json
{
  "name": "Family Friendly Classics",
  "target_audience": "All Ages",
  "primary_genre": "Pop",
  "mood": "Happy"
}
```
**Song Tags:** Easy difficulty, Family-friendly

### 4. **Music Trivia Expert Mode**
```json
{
  "name": "Deep Cuts Challenge",
  "target_audience": "Music Enthusiasts",
  "difficulty": "hard"
}
```
**Song Tags:** Underground, Alternative, Hard

---

## 🎮 Playing with Custom Lists

### Full List
```javascript
// Start game with entire custom list
{
  "provider": "custom",
  "mode": "custom",
  "custom_list_id": "abc-123-def",
  "num_rounds": 10
}
```

### Filtered by Decade
```javascript
// Only 80s songs from the list
{
  "provider": "custom",
  "mode": "custom",
  "custom_list_id": "abc-123-def",
  "custom_filters": {
    "decade": "1980s"
  },
  "num_rounds": 10
}
```

### Multiple Filters
```javascript
// Only upbeat rock songs from the 80s
{
  "provider": "custom",
  "mode": "custom",
  "custom_list_id": "abc-123-def",
  "custom_filters": {
    "decade": "1980s",
    "genre": "Rock",
    "mood": "Upbeat"
  },
  "num_rounds": 10
}
```

---

## 💾 Data Storage

Custom lists are stored as JSON files in `data/custom_lists/`:

```
data/custom_lists/
├── index.json          # Index of all lists
├── abc-123-def.json    # Individual list file
└── xyz-456-ghi.json    # Another list file
```

### Backup & Restore
Simply copy the `data/custom_lists/` folder to backup all your custom lists!

---

## 🎨 Best Practices

### 1. **Naming Conventions**
- Use descriptive names: "80s Rock Night" not "List 1"
- Include the theme: "Corporate Holiday Party 2024"

### 2. **Categorization**
- Always tag decade and genre
- Add difficulty based on song obscurity
- Use mood for vibe-based filtering

### 3. **Song Count**
- Aim for 20-30 songs per list minimum
- Add variety within the theme
- Include easy, medium, and hard songs

### 4. **Target Audience**
- Be specific: "College Students" vs "General Audience"
- Consider age range and music knowledge
- Match difficulty to audience

---

## 📊 Usage Statistics

Track how popular your lists are:

```json
{
  "name": "80s Rock Night",
  "times_played": 47,
  "created_at": "2025-01-15",
  "song_count": 35
}
```

Use this to:
- Identify popular lists
- Retire unused lists
- Understand audience preferences

---

## 🔐 Security Note

**Current Implementation:** The admin API is currently open (no authentication).

**For Production:**
- Add authentication middleware
- Implement role-based access (admin vs regular users)
- Add rate limiting

**Quick Auth Example:**
```python
from fastapi import Header, HTTPException

async def verify_admin_token(x_admin_token: str = Header(...)):
    if x_admin_token != "your-secret-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
```

---

## 🚀 Next Steps

1. **Test the API** - Use the examples above to create your first custom list
2. **Add Songs** - Search Deezer for songs and add them with categories
3. **Play a Game** - Use your custom list in a game
4. **Build Frontend** - Create a beautiful admin UI (coming soon!)

---

## 📝 Example: Complete Workflow

```bash
# 1. Create list
LIST_ID=$(curl -s -X POST http://localhost:8000/api/admin/lists \
  -H "Content-Type: application/json" \
  -d '{"name": "Party Hits", "primary_genre": "Pop"}' | jq -r '.id')

# 2. Search for songs
curl -X POST http://localhost:8000/api/admin/search-songs \
  -H "Content-Type: application/json" \
  -d '{"provider": "deezer", "mode": "genre", "query": "party"}'

# 3. Add songs (repeat for each song)
curl -X POST http://localhost:8000/api/admin/lists/$LIST_ID/songs \
  -H "Content-Type: application/json" \
  -d '{...song data...}'

# 4. Start a game
curl -X POST http://localhost:8000/api/game/start \
  -H "Content-Type: application/json" \
  -d "{\"provider\": \"custom\", \"mode\": \"custom\", \"custom_list_id\": \"$LIST_ID\", \"num_rounds\": 5}"
```

---

**Happy List Creating!** 🎵🎶🎵
