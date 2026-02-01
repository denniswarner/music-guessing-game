"use client";

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Music, Search, Plus, Trash2, Send, CheckCircle } from 'lucide-react';
import { searchSongs, getCategories, submitGuestPlaylist } from '@/lib/admin-api';
import type { CustomSong, CategoryOptions } from '@/lib/admin-types';
import { toast } from 'sonner';

export default function ContributePage() {
  // Playlist info
  const [playlistName, setPlaylistName] = useState('');
  const [playlistDescription, setPlaylistDescription] = useState('');
  const [contributorName, setContributorName] = useState('');
  
  // Songs in the playlist
  const [songs, setSongs] = useState<CustomSong[]>([]);
  
  // Search state
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  
  // Categories for metadata
  const [categories, setCategories] = useState<CategoryOptions | null>(null);
  
  // Submission state
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  // Load categories on first search
  const loadCategoriesIfNeeded = async () => {
    if (!categories) {
      try {
        const cats = await getCategories();
        setCategories(cats);
      } catch (err) {
        console.error('Failed to load categories:', err);
      }
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      toast.error('Please enter a search term');
      return;
    }

    try {
      setIsSearching(true);
      await loadCategoriesIfNeeded();
      
      const results = await searchSongs({
        provider: 'deezer',
        mode: 'genre', // General search - works for artist, song title, genre, etc.
        query: searchQuery.trim()
      });
      setSearchResults(results);
      
      if (results.length === 0) {
        toast.info('No songs found. Try a different search term.');
      }
    } catch (err: any) {
      console.error('Search failed:', err);
      toast.error('Search failed. Please try again.');
    } finally {
      setIsSearching(false);
    }
  };

  const handleAddSong = (song: any) => {
    // Check if already added
    if (songs.some(s => s.id === song.id)) {
      toast.info('This song is already in your playlist');
      return;
    }

    // Extract decade from release date
    let decade: string | undefined;
    if (song.album?.release_date && song.album.release_date !== 'Unknown') {
      const year = parseInt(song.album.release_date.substring(0, 4));
      if (year >= 1950) {
        const decadeStart = Math.floor(year / 10) * 10;
        decade = `${decadeStart}s`;
      }
    }

    const customSong: CustomSong = {
      id: song.id,
      name: song.name,
      artist: song.artists?.[0]?.name || 'Unknown Artist',
      album: song.album?.name,
      preview_url: song.preview_url,
      decade,
      provider: 'deezer',
      difficulty: 'medium'
    };

    setSongs([...songs, customSong]);
    toast.success(`Added "${song.name}" to your playlist`);
  };

  const handleRemoveSong = (songId: string) => {
    setSongs(songs.filter(s => s.id !== songId));
  };

  const handleSubmit = async () => {
    // Validation
    if (!playlistName.trim()) {
      toast.error('Please enter a playlist name');
      return;
    }
    if (!contributorName.trim()) {
      toast.error('Please enter your name');
      return;
    }
    if (songs.length === 0) {
      toast.error('Please add at least one song to your playlist');
      return;
    }

    try {
      setIsSubmitting(true);
      
      await submitGuestPlaylist(
        playlistName.trim(),
        playlistDescription.trim(),
        contributorName.trim(),
        songs
      );
      
      setIsSubmitted(true);
      toast.success('Playlist submitted successfully!');
    } catch (err: any) {
      console.error('Submit failed:', err);
      toast.error('Failed to submit playlist. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Success screen after submission
  if (isSubmitted) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-green-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
        <Card className="w-full max-w-md text-center">
          <CardContent className="pt-8 pb-8">
            <div className="flex justify-center mb-4">
              <div className="p-4 bg-green-100 dark:bg-green-900 rounded-full">
                <CheckCircle className="h-12 w-12 text-green-600 dark:text-green-400" />
              </div>
            </div>
            <h1 className="text-2xl font-bold mb-2">Thank You!</h1>
            <p className="text-muted-foreground mb-6">
              Your playlist "{playlistName}" has been submitted for review. 
              The admin will review it shortly.
            </p>
            <div className="space-y-2">
              <Button onClick={() => window.location.reload()} className="w-full">
                Submit Another Playlist
              </Button>
              <Button variant="outline" onClick={() => window.location.href = '/'} className="w-full">
                Go to Game
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="p-4 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full">
              <Music className="h-12 w-12 text-white" />
            </div>
          </div>
          <h1 className="text-3xl font-bold mb-2">Contribute a Playlist</h1>
          <p className="text-muted-foreground">
            Create a playlist for the Music Guessing Game! Search for songs and build your collection.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column - Search & Add Songs */}
          <div className="space-y-6">
            {/* Search Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Search className="h-5 w-5" />
                  Search Songs
                </CardTitle>
                <CardDescription>
                  Search Deezer for songs to add to your playlist
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-2">
                  <Input
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search by artist, song title, or genre..."
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                    className="flex-1"
                  />
                  <Button onClick={handleSearch} disabled={isSearching}>
                    {isSearching ? '...' : 'Search'}
                  </Button>
                </div>
                
                <p className="text-xs text-muted-foreground">
                  Try: "Queen", "Bohemian Rhapsody", "80s rock", "jazz", etc.
                </p>

                {/* Search Results */}
                {searchResults.length > 0 && (
                  <div className="border rounded-lg p-3 max-h-80 overflow-y-auto">
                    <div className="text-xs text-muted-foreground mb-2">
                      {searchResults.length} results
                    </div>
                    <div className="space-y-2">
                      {searchResults.map((song) => (
                        <div
                          key={song.id}
                          className="flex items-center gap-2 p-2 rounded-lg border hover:bg-accent transition-colors"
                        >
                          <div className="flex-1 min-w-0">
                            <div className="text-sm font-medium truncate">{song.name}</div>
                            <div className="text-xs text-muted-foreground truncate">
                              {song.artists?.[0]?.name}
                            </div>
                          </div>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => handleAddSong(song)}
                            disabled={songs.some(s => s.id === song.id)}
                          >
                            <Plus className="h-4 w-4" />
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Playlist Details & Songs */}
          <div className="space-y-6">
            {/* Playlist Info Card */}
            <Card>
              <CardHeader>
                <CardTitle>Your Playlist</CardTitle>
                <CardDescription>
                  Give your playlist a name and add your details
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="contributor">Your Name *</Label>
                  <Input
                    id="contributor"
                    value={contributorName}
                    onChange={(e) => setContributorName(e.target.value)}
                    placeholder="Your name or nickname"
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="name">Playlist Name *</Label>
                  <Input
                    id="name"
                    value={playlistName}
                    onChange={(e) => setPlaylistName(e.target.value)}
                    placeholder="e.g., 90s Rock Hits"
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="description">Description (optional)</Label>
                  <Textarea
                    id="description"
                    value={playlistDescription}
                    onChange={(e) => setPlaylistDescription(e.target.value)}
                    placeholder="Describe your playlist..."
                    rows={2}
                  />
                </div>
              </CardContent>
            </Card>

            {/* Songs List Card */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Songs ({songs.length})</CardTitle>
                    <CardDescription>
                      {songs.length === 0 ? 'Search and add songs above' : 'Your selected songs'}
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {songs.length === 0 ? (
                  <div className="text-center py-6 text-muted-foreground">
                    <Music className="h-8 w-8 mx-auto mb-2 opacity-50" />
                    <p className="text-sm">No songs yet. Search and add some!</p>
                  </div>
                ) : (
                  <div className="space-y-2 max-h-60 overflow-y-auto">
                    {songs.map((song, index) => (
                      <div
                        key={song.id}
                        className="flex items-center gap-2 p-2 rounded-lg border"
                      >
                        <span className="text-xs text-muted-foreground w-5">{index + 1}</span>
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-medium truncate">{song.name}</div>
                          <div className="text-xs text-muted-foreground truncate">
                            {song.artist}
                          </div>
                        </div>
                        {song.decade && (
                          <Badge variant="secondary" className="text-xs">
                            {song.decade}
                          </Badge>
                        )}
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => handleRemoveSong(song.id)}
                        >
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Submit Button */}
            <Button
              onClick={handleSubmit}
              disabled={isSubmitting || songs.length === 0}
              className="w-full gap-2"
              size="lg"
            >
              <Send className="h-4 w-4" />
              {isSubmitting ? 'Submitting...' : 'Submit Playlist for Review'}
            </Button>
            
            <p className="text-xs text-center text-muted-foreground">
              Your playlist will be reviewed by the admin before being added to the game.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
