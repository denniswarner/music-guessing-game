"""
Custom Song List Manager

Manages storage and retrieval of admin-created custom song lists.
Uses JSON file storage for simplicity and portability.
"""

import json
import os
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path

from app.custom_lists_models import CustomSongList, CustomSong, CustomListSummary


class CustomListManager:
    """Manages custom song lists with file-based storage."""
    
    def __init__(self, storage_dir: str = "data/custom_lists"):
        """
        Initialize the custom list manager.
        
        Args:
            storage_dir: Directory to store list JSON files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_index_file()
    
    def _ensure_index_file(self):
        """Ensure the index file exists."""
        index_path = self.storage_dir / "index.json"
        if not index_path.exists():
            index_path.write_text(json.dumps({"lists": []}, indent=2))
    
    def _get_list_path(self, list_id: str) -> Path:
        """Get the file path for a list."""
        return self.storage_dir / f"{list_id}.json"
    
    def _update_index(self, list_summary: CustomListSummary):
        """Update the index with list summary."""
        index_path = self.storage_dir / "index.json"
        index = json.loads(index_path.read_text())
        
        # Remove existing entry if present
        index["lists"] = [l for l in index["lists"] if l["id"] != list_summary.id]
        
        # Add updated entry
        index["lists"].append(list_summary.dict())
        
        index_path.write_text(json.dumps(index, indent=2))
    
    def _remove_from_index(self, list_id: str):
        """Remove a list from the index."""
        index_path = self.storage_dir / "index.json"
        index = json.loads(index_path.read_text())
        index["lists"] = [l for l in index["lists"] if l["id"] != list_id]
        index_path.write_text(json.dumps(index, indent=2))
    
    def create_list(
        self,
        name: str,
        description: Optional[str] = None,
        target_audience: Optional[str] = None,
        primary_decade: Optional[str] = None,
        primary_genre: Optional[str] = None,
        created_by: str = "admin"
    ) -> CustomSongList:
        """
        Create a new custom song list.
        
        Args:
            name: List name
            description: List description
            target_audience: Target audience description
            primary_decade: Primary decade focus
            primary_genre: Primary genre focus
            created_by: Creator username
            
        Returns:
            CustomSongList: The created list
        """
        list_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        custom_list = CustomSongList(
            id=list_id,
            name=name,
            description=description,
            target_audience=target_audience,
            primary_decade=primary_decade,
            primary_genre=primary_genre,
            songs=[],
            created_at=now,
            updated_at=now,
            created_by=created_by,
            is_active=True,
            times_played=0
        )
        
        # Save to file
        list_path = self._get_list_path(list_id)
        list_path.write_text(json.dumps(custom_list.dict(), indent=2))
        
        # Update index
        summary = self._list_to_summary(custom_list)
        self._update_index(summary)
        
        return custom_list
    
    def get_list(self, list_id: str) -> Optional[CustomSongList]:
        """
        Get a custom list by ID.
        
        Args:
            list_id: List ID
            
        Returns:
            CustomSongList or None if not found
        """
        list_path = self._get_list_path(list_id)
        if not list_path.exists():
            return None
        
        data = json.loads(list_path.read_text())
        return CustomSongList(**data)
    
    def list_all_summaries(self, active_only: bool = False) -> List[CustomListSummary]:
        """
        Get summaries of all lists.
        
        Args:
            active_only: Only return active lists
            
        Returns:
            List of CustomListSummary objects
        """
        index_path = self.storage_dir / "index.json"
        index = json.loads(index_path.read_text())
        
        summaries = [CustomListSummary(**l) for l in index["lists"]]
        
        if active_only:
            summaries = [s for s in summaries if s.is_active]
        
        return sorted(summaries, key=lambda x: x.updated_at, reverse=True)
    
    def update_list(
        self,
        list_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        target_audience: Optional[str] = None,
        primary_decade: Optional[str] = None,
        primary_genre: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Optional[CustomSongList]:
        """
        Update list metadata.
        
        Args:
            list_id: List ID
            name: New name (optional)
            description: New description (optional)
            target_audience: New target audience (optional)
            primary_decade: New primary decade (optional)
            primary_genre: New primary genre (optional)
            is_active: New active status (optional)
            
        Returns:
            Updated CustomSongList or None if not found
        """
        custom_list = self.get_list(list_id)
        if not custom_list:
            return None
        
        # Update fields
        if name is not None:
            custom_list.name = name
        if description is not None:
            custom_list.description = description
        if target_audience is not None:
            custom_list.target_audience = target_audience
        if primary_decade is not None:
            custom_list.primary_decade = primary_decade
        if primary_genre is not None:
            custom_list.primary_genre = primary_genre
        if is_active is not None:
            custom_list.is_active = is_active
        
        custom_list.updated_at = datetime.utcnow().isoformat()
        
        # Save
        list_path = self._get_list_path(list_id)
        list_path.write_text(json.dumps(custom_list.dict(), indent=2))
        
        # Update index
        summary = self._list_to_summary(custom_list)
        self._update_index(summary)
        
        return custom_list
    
    def delete_list(self, list_id: str) -> bool:
        """
        Delete a custom list.
        
        Args:
            list_id: List ID
            
        Returns:
            True if deleted, False if not found
        """
        list_path = self._get_list_path(list_id)
        if not list_path.exists():
            return False
        
        list_path.unlink()
        self._remove_from_index(list_id)
        return True
    
    def add_song(self, list_id: str, song: CustomSong) -> Optional[CustomSongList]:
        """
        Add a song to a list.
        
        Args:
            list_id: List ID
            song: Song to add
            
        Returns:
            Updated CustomSongList or None if not found
        """
        custom_list = self.get_list(list_id)
        if not custom_list:
            return None
        
        # Check if song already exists
        if any(s.id == song.id for s in custom_list.songs):
            # Update existing song
            custom_list.songs = [song if s.id == song.id else s for s in custom_list.songs]
        else:
            # Add new song
            custom_list.songs.append(song)
        
        custom_list.updated_at = datetime.utcnow().isoformat()
        
        # Save
        list_path = self._get_list_path(list_id)
        list_path.write_text(json.dumps(custom_list.dict(), indent=2))
        
        # Update index
        summary = self._list_to_summary(custom_list)
        self._update_index(summary)
        
        return custom_list
    
    def remove_song(self, list_id: str, song_id: str) -> Optional[CustomSongList]:
        """
        Remove a song from a list.
        
        Args:
            list_id: List ID
            song_id: Song ID to remove
            
        Returns:
            Updated CustomSongList or None if not found
        """
        custom_list = self.get_list(list_id)
        if not custom_list:
            return None
        
        custom_list.songs = [s for s in custom_list.songs if s.id != song_id]
        custom_list.updated_at = datetime.utcnow().isoformat()
        
        # Save
        list_path = self._get_list_path(list_id)
        list_path.write_text(json.dumps(custom_list.dict(), indent=2))
        
        # Update index
        summary = self._list_to_summary(custom_list)
        self._update_index(summary)
        
        return custom_list
    
    def filter_songs(
        self,
        list_id: str,
        decade: Optional[str] = None,
        genre: Optional[str] = None,
        style: Optional[str] = None,
        mood: Optional[str] = None,
        difficulty: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[CustomSong]:
        """
        Filter songs from a list by criteria.
        
        Args:
            list_id: List ID
            decade: Filter by decade
            genre: Filter by genre
            style: Filter by style
            mood: Filter by mood
            difficulty: Filter by difficulty
            limit: Max songs to return
            
        Returns:
            Filtered list of songs
        """
        custom_list = self.get_list(list_id)
        if not custom_list:
            return []
        
        filtered = custom_list.songs
        
        if decade:
            filtered = [s for s in filtered if s.decade == decade]
        if genre:
            filtered = [s for s in filtered if s.genre == genre]
        if style:
            filtered = [s for s in filtered if s.style == style]
        if mood:
            filtered = [s for s in filtered if s.mood == mood]
        if difficulty:
            filtered = [s for s in filtered if s.difficulty == difficulty]
        
        if limit:
            filtered = filtered[:limit]
        
        return filtered
    
    def increment_play_count(self, list_id: str):
        """
        Increment the play count for a list.
        
        Args:
            list_id: List ID
        """
        custom_list = self.get_list(list_id)
        if custom_list:
            custom_list.times_played += 1
            custom_list.updated_at = datetime.utcnow().isoformat()
            
            list_path = self._get_list_path(list_id)
            list_path.write_text(json.dumps(custom_list.dict(), indent=2))
            
            summary = self._list_to_summary(custom_list)
            self._update_index(summary)
    
    def _list_to_summary(self, custom_list: CustomSongList) -> CustomListSummary:
        """Convert a CustomSongList to a summary."""
        return CustomListSummary(
            id=custom_list.id,
            name=custom_list.name,
            description=custom_list.description,
            target_audience=custom_list.target_audience,
            primary_decade=custom_list.primary_decade,
            primary_genre=custom_list.primary_genre,
            song_count=len(custom_list.songs),
            created_at=custom_list.created_at,
            updated_at=custom_list.updated_at,
            times_played=custom_list.times_played,
            is_active=custom_list.is_active
        )


# Global manager instance
custom_list_manager = CustomListManager()
