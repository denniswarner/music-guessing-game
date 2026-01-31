"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  Database, Search, Music, Calendar, Tag, TrendingUp, 
  ArrowLeft, Filter, SortAsc, SortDesc 
} from 'lucide-react';
import { getAllLibrarySongs } from '@/lib/admin-api';

export default function LibraryPage() {
  const router = useRouter();
  const [songs, setSongs] = useState<any[]>([]);
  const [filteredSongs, setFilteredSongs] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterGenre, setFilterGenre] = useState('all');
  const [filterDecade, setFilterDecade] = useState('all');
  const [sortBy, setSortBy] = useState<'name' | 'artist' | 'added' | 'used'>('name');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  useEffect(() => {
    loadLibrary();
  }, []);

  useEffect(() => {
    filterAndSortSongs();
  }, [songs, searchQuery, filterGenre, filterDecade, sortBy, sortOrder]);

  const loadLibrary = async () => {
    try {
      setIsLoading(true);
      const data = await getAllLibrarySongs();
      setSongs(data.songs);
    } catch (error) {
      console.error('Failed to load library:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const filterAndSortSongs = () => {
    let filtered = [...songs];

    // Search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(song => 
        song.name.toLowerCase().includes(query) ||
        song.artist.toLowerCase().includes(query) ||
        song.album?.toLowerCase().includes(query)
      );
    }

    // Genre filter
    if (filterGenre !== 'all') {
      filtered = filtered.filter(song => song.metadata?.genre === filterGenre);
    }

    // Decade filter
    if (filterDecade !== 'all') {
      filtered = filtered.filter(song => song.metadata?.decade === filterDecade);
    }

    // Sort
    filtered.sort((a, b) => {
      let aVal, bVal;
      
      switch (sortBy) {
        case 'name':
          aVal = a.name.toLowerCase();
          bVal = b.name.toLowerCase();
          break;
        case 'artist':
          aVal = a.artist.toLowerCase();
          bVal = b.artist.toLowerCase();
          break;
        case 'added':
          aVal = new Date(a.added_date).getTime();
          bVal = new Date(b.added_date).getTime();
          break;
        case 'used':
          aVal = a.times_used || 0;
          bVal = b.times_used || 0;
          break;
        default:
          return 0;
      }

      if (sortOrder === 'asc') {
        return aVal > bVal ? 1 : -1;
      } else {
        return aVal < bVal ? 1 : -1;
      }
    });

    setFilteredSongs(filtered);
  };

  const getUniqueGenres = () => {
    const genres = songs
      .map(s => s.metadata?.genre)
      .filter(g => g);
    return ['all', ...Array.from(new Set(genres))];
  };

  const getUniqueDecades = () => {
    const decades = songs
      .map(s => s.metadata?.decade)
      .filter(d => d);
    return ['all', ...Array.from(new Set(decades)).sort()];
  };

  const toggleSort = (field: typeof sortBy) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('asc');
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              onClick={() => router.push('/admin')}
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
            <div>
              <div className="flex items-center gap-2">
                <Database className="h-8 w-8 text-purple-600 dark:text-purple-400" />
                <h1 className="text-4xl font-bold">Music Library</h1>
              </div>
              <p className="text-muted-foreground mt-1">
                Browse all {songs.length} songs in your personal metadata library
              </p>
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <Card className="mb-6">
          <CardContent className="pt-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* Search */}
              <div className="md:col-span-2">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search by song, artist, or album..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>

              {/* Genre Filter */}
              <div>
                <select
                  value={filterGenre}
                  onChange={(e) => setFilterGenre(e.target.value)}
                  className="w-full h-10 px-3 rounded-md border border-input bg-background"
                >
                  {getUniqueGenres().map(genre => (
                    <option key={genre} value={genre}>
                      {genre === 'all' ? 'All Genres' : genre}
                    </option>
                  ))}
                </select>
              </div>

              {/* Decade Filter */}
              <div>
                <select
                  value={filterDecade}
                  onChange={(e) => setFilterDecade(e.target.value)}
                  className="w-full h-10 px-3 rounded-md border border-input bg-background"
                >
                  {getUniqueDecades().map(decade => (
                    <option key={decade} value={decade}>
                      {decade === 'all' ? 'All Decades' : decade}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Sort Buttons */}
            <div className="flex gap-2 mt-4">
              <span className="text-sm text-muted-foreground self-center">Sort by:</span>
              <Button
                variant={sortBy === 'name' ? 'default' : 'outline'}
                size="sm"
                onClick={() => toggleSort('name')}
              >
                Song Name {sortBy === 'name' && (sortOrder === 'asc' ? <SortAsc className="h-3 w-3 ml-1" /> : <SortDesc className="h-3 w-3 ml-1" />)}
              </Button>
              <Button
                variant={sortBy === 'artist' ? 'default' : 'outline'}
                size="sm"
                onClick={() => toggleSort('artist')}
              >
                Artist {sortBy === 'artist' && (sortOrder === 'asc' ? <SortAsc className="h-3 w-3 ml-1" /> : <SortDesc className="h-3 w-3 ml-1" />)}
              </Button>
              <Button
                variant={sortBy === 'added' ? 'default' : 'outline'}
                size="sm"
                onClick={() => toggleSort('added')}
              >
                Date Added {sortBy === 'added' && (sortOrder === 'asc' ? <SortAsc className="h-3 w-3 ml-1" /> : <SortDesc className="h-3 w-3 ml-1" />)}
              </Button>
              <Button
                variant={sortBy === 'used' ? 'default' : 'outline'}
                size="sm"
                onClick={() => toggleSort('used')}
              >
                Most Used {sortBy === 'used' && (sortOrder === 'asc' ? <SortAsc className="h-3 w-3 ml-1" /> : <SortDesc className="h-3 w-3 ml-1" />)}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Results Count */}
        <div className="mb-4 text-sm text-muted-foreground">
          Showing {filteredSongs.length} of {songs.length} songs
        </div>

        {/* Songs List */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent"></div>
            <p className="mt-4 text-muted-foreground">Loading library...</p>
          </div>
        ) : filteredSongs.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <Music className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
              <h3 className="text-lg font-semibold mb-2">
                {songs.length === 0 ? 'No Songs in Library Yet' : 'No Matching Songs'}
              </h3>
              <p className="text-muted-foreground">
                {songs.length === 0 
                  ? 'Add songs to your custom lists to build your library!'
                  : 'Try adjusting your filters or search query.'
                }
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {filteredSongs.map((song) => (
              <Card key={`${song.provider}_${song.id}`} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      {/* Song Info */}
                      <div className="flex items-start gap-3">
                        <Music className="h-5 w-5 mt-1 text-purple-600 dark:text-purple-400" />
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold">{song.name}</h3>
                          <p className="text-muted-foreground">{song.artist}</p>
                          {song.album && (
                            <p className="text-sm text-muted-foreground">
                              {song.album} {song.release_date && song.release_date !== 'Unknown' && `• ${song.release_date.substring(0, 4)}`}
                            </p>
                          )}
                        </div>
                      </div>

                      {/* Metadata Tags */}
                      <div className="flex flex-wrap gap-2 mt-3">
                        {song.metadata?.decade && (
                          <Badge variant="outline" className="gap-1">
                            <Calendar className="h-3 w-3" />
                            {song.metadata.decade}
                          </Badge>
                        )}
                        {song.metadata?.genre && (
                          <Badge variant="secondary">
                            {song.metadata.genre}
                          </Badge>
                        )}
                        {song.metadata?.style && (
                          <Badge variant="secondary">
                            {song.metadata.style}
                          </Badge>
                        )}
                        {song.metadata?.mood && (
                          <Badge variant="secondary">
                            {song.metadata.mood}
                          </Badge>
                        )}
                        {song.metadata?.difficulty && (
                          <Badge variant="outline">
                            {song.metadata.difficulty}
                          </Badge>
                        )}
                      </div>

                      {/* Notes */}
                      {song.metadata?.notes && (
                        <p className="text-sm text-muted-foreground mt-2 italic">
                          "{song.metadata.notes}"
                        </p>
                      )}
                    </div>

                    {/* Stats */}
                    <div className="text-right">
                      <Badge className="mb-2">
                        <TrendingUp className="h-3 w-3 mr-1" />
                        Used {song.times_used || 0}x
                      </Badge>
                      <p className="text-xs text-muted-foreground">
                        Added {formatDate(song.added_date)}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {song.provider}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
