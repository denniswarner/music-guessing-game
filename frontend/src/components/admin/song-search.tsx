"use client";

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Music, Search, Plus, Sparkles, BookOpen, Database } from 'lucide-react';
import { searchSongs, addSongToList, enrichSongMetadata, checkLibrarySong, getArtistSuggestions, saveToLibrary } from '@/lib/admin-api';
import type { CategoryOptions, CustomSong } from '@/lib/admin-types';
import { toast } from 'sonner';

interface SongSearchProps {
  listId: string;
  categories: CategoryOptions | null;
  onClose: () => void;
  onSongAdded: () => void;
}

export function SongSearch({ listId, categories, onClose, onSongAdded }: SongSearchProps) {
  const [provider, setProvider] = useState<'deezer' | 'demo'>('deezer');
  const [mode, setMode] = useState<'genre' | 'artist'>('genre');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [selectedSong, setSelectedSong] = useState<any | null>(null);
  
  // Categorization form
  const [decade, setDecade] = useState('');
  const [genre, setGenre] = useState('');
  const [style, setStyle] = useState('');
  const [mood, setMood] = useState('');
  const [difficulty, setDifficulty] = useState('medium');
  const [notes, setNotes] = useState('');
  const [isEnriching, setIsEnriching] = useState(false);
  const [enrichmentTags, setEnrichmentTags] = useState<string[]>([]);
  const [enrichmentSource, setEnrichmentSource] = useState<'library' | 'artist' | 'local' | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) {
      alert('Please enter a search query');
      return;
    }

    try {
      setIsSearching(true);
      const data = await searchSongs({
        provider,
        mode,
        query: query.trim()
      });
      setResults(data);
    } catch (err: any) {
      console.error('Search failed:', err);
      alert('Search failed. Please try again.');
    } finally {
      setIsSearching(false);
    }
  };

  const handleSelectSong = async (song: any) => {
    setSelectedSong(song);
    setIsEnriching(true);
    setEnrichmentTags([]);
    setEnrichmentSource(null);
    
    // 1. Extract decade from release date
    let releaseYear: number | undefined;
    if (song.album?.release_date && song.album.release_date !== 'Unknown') {
      const year = song.album.release_date.substring(0, 4);
      const yearNum = parseInt(year);
      releaseYear = yearNum;
      
      if (yearNum >= 1950) {
        const decadeStart = Math.floor(yearNum / 10) * 10;
        const decadeStr = `${decadeStart}s`;
        setDecade(decadeStr);
      }
    }
    
    try {
      // 2. Check if this exact song is in user's library (highest priority)
      const libraryCheck = await checkLibrarySong(song.id, provider);
      
      if (libraryCheck.found && libraryCheck.song) {
        const libSong = libraryCheck.song;
        const meta = libSong.metadata;
        
        // Populate from library
        if (meta.genre) setGenre(meta.genre);
        if (meta.mood) setMood(meta.mood);
        if (meta.style) setStyle(meta.style);
        if (meta.difficulty) setDifficulty(meta.difficulty);
        if (meta.notes) setNotes(meta.notes);
        
        setEnrichmentSource('library');
        setEnrichmentTags(['From your library', `Used ${libSong.times_used}x`]);
        setIsEnriching(false);
        return;
      }
      
      // 3. Check if user has other songs by this artist (second priority)
      const artist = song.artists?.[0]?.name || 'Unknown Artist';
      const artistSuggestions = await getArtistSuggestions(artist);
      
      if (artistSuggestions.found && artistSuggestions.suggestions) {
        const sugg = artistSuggestions.suggestions;
        
        // Apply artist-based suggestions
        if (sugg.genre) setGenre(sugg.genre);
        if (sugg.mood) setMood(sugg.mood);
        if (sugg.style) setStyle(sugg.style);
        
        setEnrichmentSource('artist');
        setEnrichmentTags([
          `Based on ${artistSuggestions.count} ${artist} song${artistSuggestions.count > 1 ? 's' : ''}`,
          ...(sugg.genre ? [`Genre: ${sugg.genre}`] : [])
        ]);
        setIsEnriching(false);
        return;
      }
      
      // 4. Fall back to local enrichment (lowest priority)
      const track = song.name;
      const enriched = await enrichSongMetadata(artist, track, releaseYear);
      
      if (enriched.success && enriched.data) {
        if (enriched.data.genre) setGenre(enriched.data.genre);
        if (enriched.data.mood) setMood(enriched.data.mood);
        if (enriched.data.style) setStyle(enriched.data.style);
        if (enriched.data.tags && enriched.data.tags.length > 0) {
          setEnrichmentTags(enriched.data.tags);
        }
        
        setEnrichmentSource('local');
      }
      
    } catch (error) {
      console.error('Enrichment failed:', error);
      // Fall back to year-based style only
      if (releaseYear) {
        if (releaseYear < 1980) {
          setStyle('Classic');
        } else if (releaseYear < 2010) {
          setStyle('Modern');
        } else {
          setStyle('Contemporary');
        }
      }
    } finally {
      setIsEnriching(false);
    }
  };

  const handleAddSong = async () => {
    if (!selectedSong) return;

    try {
      const customSong: CustomSong = {
        id: selectedSong.id,
        name: selectedSong.name,
        artist: selectedSong.artists?.[0]?.name || 'Unknown Artist',
        album: selectedSong.album?.name,
        preview_url: selectedSong.preview_url,
        decade: decade || undefined,
        genre: genre || undefined,
        style: style || undefined,
        mood: mood || undefined,
        difficulty: difficulty,
        provider: selectedSong.provider || provider,
        notes: notes.trim() || undefined,
      };

      // Add to custom list
      await addSongToList(listId, customSong);
      
      // Save to metadata library for future use
      await saveToLibrary(
        selectedSong.id,
        provider,
        selectedSong.name,
        selectedSong.artists?.[0]?.name || 'Unknown Artist',
        selectedSong.album?.name,
        selectedSong.album?.release_date,
        {
          decade: decade || undefined,
          genre: genre || undefined,
          style: style || undefined,
          mood: mood || undefined,
          difficulty: difficulty || 'medium',
          notes: notes || undefined,
        }
      );
      
      // Reset and notify
      onSongAdded();
      toast.success('Song added to playlist!', {
        description: `"${selectedSong.name}" has been added and saved to your library.`
      });
    } catch (err: any) {
      console.error('Failed to add song:', err);
      toast.error('Failed to add song', {
        description: err.message || 'An error occurred.'
      });
    }
  };

  return (
    <Dialog open onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Add Songs</DialogTitle>
          <DialogDescription>
            Search for songs and add them to your list with categorization
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* Search Form */}
          {!selectedSong && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Provider</Label>
                  <Select value={provider} onValueChange={(v: any) => setProvider(v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="deezer">Deezer (Recommended)</SelectItem>
                      <SelectItem value="demo">Demo</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Mode</Label>
                  <Select value={mode} onValueChange={(v: any) => setMode(v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="genre">Genre</SelectItem>
                      <SelectItem value="artist">Artist</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="flex gap-2">
                <Input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder={mode === 'genre' ? 'e.g., rock, pop, 80s' : 'e.g., Queen, Beatles'}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />
                <Button onClick={handleSearch} disabled={isSearching} className="gap-2">
                  <Search className="h-4 w-4" />
                  {isSearching ? 'Searching...' : 'Search'}
                </Button>
              </div>

              {/* Search Results */}
              {results.length > 0 && (
                <div className="border rounded-lg p-4 max-h-96 overflow-y-auto">
                  <h3 className="font-semibold mb-3">Results ({results.length})</h3>
                  <div className="space-y-2">
                    {results.map((song) => (
                      <div
                        key={song.id}
                        className="flex items-center gap-3 p-3 rounded-lg border hover:bg-accent cursor-pointer transition-colors"
                        onClick={() => handleSelectSong(song)}
                      >
                        <Music className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <div className="font-medium truncate">{song.name}</div>
                          <div className="text-sm text-muted-foreground truncate">
                            {song.artists?.[0]?.name || 'Unknown Artist'}
                            {song.album?.name && ` • ${song.album.name}`}
                          </div>
                        </div>
                        <Button size="sm" variant="ghost">
                          Select
                        </Button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Categorization Form */}
          {selectedSong && (
            <div className="space-y-4">
              {/* Selected Song Info */}
              <div className="p-4 rounded-lg bg-accent">
                <div className="flex items-start gap-3">
                  <Music className="h-5 w-5 mt-1" />
                  <div className="flex-1">
                    <div className="font-semibold">{selectedSong.name}</div>
                    <div className="text-sm text-muted-foreground">
                      {selectedSong.artists?.[0]?.name || 'Unknown Artist'}
                      {selectedSong.album?.name && ` • ${selectedSong.album.name}`}
                      {selectedSong.album?.release_date && selectedSong.album.release_date !== 'Unknown' && 
                        ` • ${selectedSong.album.release_date.substring(0, 4)}`
                      }
                    </div>
                  </div>
                </div>
              </div>

              {/* Enrichment status */}
              {isEnriching && (
                <div className="text-sm bg-blue-50 dark:bg-blue-950 p-3 rounded-lg flex items-center gap-2">
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
                  <span>Checking your library and analyzing metadata...</span>
                </div>
              )}
              
              {/* Auto-populated notice */}
              {!isEnriching && enrichmentSource && (decade || genre || mood || style) && (
                <div className={`text-sm p-3 rounded-lg ${
                  enrichmentSource === 'library' 
                    ? 'bg-purple-50 dark:bg-purple-950'
                    : enrichmentSource === 'artist'
                    ? 'bg-blue-50 dark:bg-blue-950'
                    : 'bg-green-50 dark:bg-green-950'
                }`}>
                  <div className="flex items-center gap-2 mb-2">
                    {enrichmentSource === 'library' ? (
                      <Database className="h-4 w-4 text-purple-600 dark:text-purple-400" />
                    ) : enrichmentSource === 'artist' ? (
                      <BookOpen className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                    ) : (
                      <Sparkles className="h-4 w-4 text-green-600 dark:text-green-400" />
                    )}
                    <span className={`font-semibold ${
                      enrichmentSource === 'library'
                        ? 'text-purple-900 dark:text-purple-100'
                        : enrichmentSource === 'artist'
                        ? 'text-blue-900 dark:text-blue-100'
                        : 'text-green-900 dark:text-green-100'
                    }`}>
                      {enrichmentSource === 'library' && '📚 Loaded from Your Library!'}
                      {enrichmentSource === 'artist' && '🎤 Suggested from Artist History'}
                      {enrichmentSource === 'local' && '✨ Metadata Auto-Populated'}
                    </span>
                  </div>
                  <div className={`text-xs ${
                    enrichmentSource === 'library'
                      ? 'text-purple-700 dark:text-purple-300'
                      : enrichmentSource === 'artist'
                      ? 'text-blue-700 dark:text-blue-300'
                      : 'text-green-700 dark:text-green-300'
                  }`}>
                    {enrichmentSource === 'library' && 
                      "You've categorized this song before! Using your previous metadata."
                    }
                    {enrichmentSource === 'artist' && 
                      "Based on your previous entries for this artist."
                    }
                    {enrichmentSource === 'local' && 
                      "Suggested based on artist and track info. You can change them below."
                    }
                  </div>
                  {enrichmentTags.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1">
                      {enrichmentTags.map((tag, i) => (
                        <Badge key={i} variant="outline" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Categorization Fields */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Decade</Label>
                  <Select value={decade || "none"} onValueChange={(v) => setDecade(v === "none" ? "" : v)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select decade" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">None</SelectItem>
                      {categories?.decades.map((d) => (
                        <SelectItem key={d} value={d}>{d}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Genre</Label>
                  <Select value={genre || "none"} onValueChange={(v) => setGenre(v === "none" ? "" : v)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select genre" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">None</SelectItem>
                      {categories?.genres.map((g) => (
                        <SelectItem key={g} value={g}>{g}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Style</Label>
                  <Select value={style || "none"} onValueChange={(v) => setStyle(v === "none" ? "" : v)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select style" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">None</SelectItem>
                      {categories?.styles.map((s) => (
                        <SelectItem key={s} value={s}>{s}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Mood</Label>
                  <Select value={mood || "none"} onValueChange={(v) => setMood(v === "none" ? "" : v)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select mood" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">None</SelectItem>
                      {categories?.moods.map((m) => (
                        <SelectItem key={m} value={m}>{m}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Difficulty</Label>
                  <Select value={difficulty} onValueChange={setDifficulty}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="easy">Easy</SelectItem>
                      <SelectItem value="medium">Medium</SelectItem>
                      <SelectItem value="hard">Hard</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label>Notes (Optional)</Label>
                <Input
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="e.g., Great crowd pleaser"
                />
              </div>

              {/* Actions */}
              <div className="flex gap-2 justify-end">
                <Button variant="outline" onClick={() => setSelectedSong(null)}>
                  Back to Search
                </Button>
                <Button onClick={handleAddSong} className="gap-2">
                  <Plus className="h-4 w-4" />
                  Add Song
                </Button>
              </div>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
