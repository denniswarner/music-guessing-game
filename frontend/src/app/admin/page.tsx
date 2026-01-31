"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Plus, Music, Users, Calendar, TrendingUp, Edit, Trash2, Play, Database, Settings, Link, ListMusic } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { getAllLists, getLibraryStats } from '@/lib/admin-api';
import type { CustomListSummary } from '@/lib/admin-types';
import type { MusicProvider } from '@/lib/types';
import { toast } from 'sonner';

export default function AdminPage() {
  const router = useRouter();
  const [lists, setLists] = useState<CustomListSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Provider settings
  const [currentProvider, setCurrentProvider] = useState<MusicProvider>('deezer');
  const [spotifyClientId, setSpotifyClientId] = useState('');
  const [spotifyClientSecret, setSpotifyClientSecret] = useState('');
  
  // Game start settings
  const [gameSource, setGameSource] = useState<'custom' | 'external'>('custom');
  const [selectedListId, setSelectedListId] = useState<string>('');
  const [playlistUrl, setPlaylistUrl] = useState('');
  const [playlistRounds, setPlaylistRounds] = useState('10');

  useEffect(() => {
    loadLists();
    loadProviderSettings();
  }, []);

  const loadLists = async () => {
    try {
      setIsLoading(true);
      const data = await getAllLists();
      setLists(data);
    } catch (err: any) {
      console.error('Failed to load lists:', err);
      setError('Failed to load custom lists');
    } finally {
      setIsLoading(false);
    }
  };

  const loadProviderSettings = () => {
    const savedProvider = localStorage.getItem('musicProvider') as MusicProvider;
    const savedClientId = localStorage.getItem('spotifyClientId');
    const savedClientSecret = localStorage.getItem('spotifyClientSecret');
    
    if (savedProvider) setCurrentProvider(savedProvider);
    if (savedClientId) setSpotifyClientId(savedClientId);
    if (savedClientSecret) setSpotifyClientSecret(savedClientSecret);
  };

  const saveProviderSettings = () => {
    localStorage.setItem('musicProvider', currentProvider);
    localStorage.setItem('spotifyClientId', spotifyClientId);
    localStorage.setItem('spotifyClientSecret', spotifyClientSecret);
    
    const providerNames = {
      demo: 'Demo',
      deezer: 'Deezer',
      spotify: 'Spotify'
    };
    
    toast.success('Music provider settings saved!', {
      description: `Now using ${providerNames[currentProvider]} for the game.`
    });
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
          <div>
            <h1 className="text-4xl font-bold mb-2">Admin Dashboard</h1>
            <p className="text-muted-foreground">
              Manage your custom song lists and music provider settings
            </p>
          </div>
          <div className="flex gap-3">
            <Button
              variant="outline"
              onClick={() => router.push('/admin/library')}
              className="gap-2"
            >
              <Database className="h-4 w-4" />
              Library
            </Button>
            <Button
              variant="outline"
              onClick={() => router.push('/')}
            >
              Back to Game
            </Button>
            <Button
              onClick={() => router.push('/admin/lists/new')}
              className="gap-2"
            >
              <Plus className="h-4 w-4" />
              Create List
            </Button>
          </div>
        </div>

        {/* Provider Settings Card - Always Visible */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Settings className="h-5 w-5" />
              Music Provider Settings
            </CardTitle>
            <CardDescription>
              Configure which music provider the game uses for audio previews
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Provider Selection */}
            <div className="space-y-3">
              <Label>Music Provider</Label>
              <div className="grid grid-cols-3 gap-3">
                <Button
                  type="button"
                  variant={currentProvider === 'demo' ? 'default' : 'outline'}
                  onClick={() => setCurrentProvider('demo')}
                  className="flex flex-col h-auto py-4"
                >
                  <span className="text-base">🎮 Demo</span>
                  <span className="text-xs opacity-75 mt-1">20 classic songs</span>
                </Button>
                <Button
                  type="button"
                  variant={currentProvider === 'deezer' ? 'default' : 'outline'}
                  onClick={() => setCurrentProvider('deezer')}
                  className="flex flex-col h-auto py-4"
                >
                  <span className="text-base">🎶 Deezer</span>
                  <span className="text-xs opacity-75 mt-1">No credentials needed!</span>
                </Button>
                <Button
                  type="button"
                  variant={currentProvider === 'spotify' ? 'default' : 'outline'}
                  onClick={() => setCurrentProvider('spotify')}
                  className="flex flex-col h-auto py-4"
                >
                  <span className="text-base">🎵 Spotify</span>
                  <span className="text-xs opacity-75 mt-1">Requires API credentials</span>
                </Button>
              </div>
            </div>

            {/* Provider Info */}
            {currentProvider === 'demo' && (
              <div className="p-4 bg-purple-100 dark:bg-purple-900/20 rounded-lg">
                <h3 className="font-semibold text-sm mb-1">🎮 Demo Mode</h3>
                <p className="text-xs text-muted-foreground">
                  Play with 20 handpicked classic songs. Perfect for testing or when you don't have API credentials!
                </p>
              </div>
            )}

            {currentProvider === 'deezer' && (
              <div className="p-4 bg-green-100 dark:bg-green-900/20 rounded-lg">
                <h3 className="font-semibold text-sm mb-1">🎶 Deezer (Recommended)</h3>
                <ul className="text-xs text-muted-foreground space-y-1 mt-2">
                  <li>• No API credentials required</li>
                  <li>• 30-second previews (vs Spotify's 10 seconds)</li>
                  <li>• Large music catalog</li>
                  <li>• Start playing immediately!</li>
                </ul>
              </div>
            )}

            {currentProvider === 'spotify' && (
              <div className="space-y-4">
                <div className="p-4 bg-green-100 dark:bg-green-900/20 rounded-lg">
                  <h3 className="font-semibold text-sm mb-1">🎵 Spotify</h3>
                  <p className="text-xs text-muted-foreground mb-2">
                    Enter your Spotify API credentials to access their music library.
                  </p>
                  <a
                    href="https://developer.spotify.com/dashboard"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-primary hover:underline"
                  >
                    Get credentials from Spotify Developer Dashboard →
                  </a>
                </div>
                
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="clientId">Spotify Client ID</Label>
                    <Input
                      id="clientId"
                      type="text"
                      placeholder="Your Spotify Client ID"
                      value={spotifyClientId}
                      onChange={(e) => setSpotifyClientId(e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="clientSecret">Spotify Client Secret</Label>
                    <Input
                      id="clientSecret"
                      type="password"
                      placeholder="Your Spotify Client Secret"
                      value={spotifyClientSecret}
                      onChange={(e) => setSpotifyClientSecret(e.target.value)}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Save Button */}
            <div className="flex justify-end">
              <Button onClick={saveProviderSettings} className="gap-2">
                <Settings className="h-4 w-4" />
                Save Settings
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Start a Game */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Play className="h-5 w-5" />
              Start a Game
            </CardTitle>
            <CardDescription>
              Choose a song source and start playing
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Song Source Selection */}
            <div className="space-y-3">
              <Label>Song Source</Label>
              <div className="grid grid-cols-2 gap-3">
                <Button
                  type="button"
                  variant={gameSource === 'custom' ? 'default' : 'outline'}
                  onClick={() => setGameSource('custom')}
                  className="flex items-center gap-2 h-auto py-3"
                >
                  <ListMusic className="h-4 w-4" />
                  <div className="text-left">
                    <div className="text-sm font-medium">Custom Playlist</div>
                    <div className="text-xs opacity-75">Your curated song lists</div>
                  </div>
                </Button>
                <Button
                  type="button"
                  variant={gameSource === 'external' ? 'default' : 'outline'}
                  onClick={() => setGameSource('external')}
                  disabled={currentProvider === 'demo'}
                  className="flex items-center gap-2 h-auto py-3"
                >
                  <Link className="h-4 w-4" />
                  <div className="text-left">
                    <div className="text-sm font-medium">External URL</div>
                    <div className="text-xs opacity-75">
                      {currentProvider === 'demo' ? 'Not available in Demo' : `${currentProvider === 'deezer' ? 'Deezer' : 'Spotify'} playlist`}
                    </div>
                  </div>
                </Button>
              </div>
            </div>

            {/* Custom Playlist Selection */}
            {gameSource === 'custom' && (
              <div className="space-y-2">
                <Label>Select Playlist</Label>
                {lists.length === 0 ? (
                  <div className="p-4 bg-muted rounded-lg text-center">
                    <p className="text-sm text-muted-foreground mb-2">No custom playlists yet</p>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => router.push('/admin/lists/new')}
                      className="gap-2"
                    >
                      <Plus className="h-3 w-3" />
                      Create Your First Playlist
                    </Button>
                  </div>
                ) : (
                  <Select value={selectedListId} onValueChange={setSelectedListId}>
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="Choose a playlist..." />
                    </SelectTrigger>
                    <SelectContent>
                      {lists.filter(l => l.is_active).map((list) => (
                        <SelectItem key={list.id} value={list.id}>
                          <div className="flex items-center gap-2">
                            <Music className="h-3 w-3" />
                            <span>{list.name}</span>
                            <span className="text-muted-foreground">({list.song_count} songs)</span>
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              </div>
            )}

            {/* External Playlist URL */}
            {gameSource === 'external' && currentProvider !== 'demo' && (
              <div className="space-y-2">
                <Label htmlFor="playlistUrl">
                  {currentProvider === 'deezer' ? 'Deezer Playlist URL or ID' : 'Spotify Playlist URL'}
                </Label>
                <Input
                  id="playlistUrl"
                  type="text"
                  placeholder={
                    currentProvider === 'deezer' 
                      ? 'e.g., 1234567890 or https://www.deezer.com/playlist/...'
                      : 'e.g., https://open.spotify.com/playlist/...'
                  }
                  value={playlistUrl}
                  onChange={(e) => setPlaylistUrl(e.target.value)}
                />
              </div>
            )}

            {/* Number of Rounds */}
            <div className="space-y-2">
              <Label htmlFor="gameRounds">Number of Rounds</Label>
              <Input
                id="gameRounds"
                type="number"
                min="1"
                max="50"
                value={playlistRounds}
                onChange={(e) => setPlaylistRounds(e.target.value)}
              />
            </div>

            {/* Start Game Button */}
            <Button 
              className="w-full gap-2"
              size="lg"
              disabled={
                (gameSource === 'custom' && !selectedListId) ||
                (gameSource === 'external' && !playlistUrl)
              }
              onClick={() => {
                if (gameSource === 'custom') {
                  const selectedList = lists.find(l => l.id === selectedListId);
                  if (!selectedList) {
                    toast.error('Please select a playlist');
                    return;
                  }
                  // Store custom list game settings
                  localStorage.setItem('gameMode', 'customList');
                  localStorage.setItem('gameListId', selectedListId);
                  localStorage.setItem('gameListName', selectedList.name);
                  localStorage.setItem('gameRounds', playlistRounds || '10');
                  toast.success(`Starting game with "${selectedList.name}"!`);
                  router.push('/');
                } else {
                  if (!playlistUrl) {
                    toast.error('Please enter a playlist URL');
                    return;
                  }
                  // Store external playlist settings
                  localStorage.setItem('gameMode', 'playlist');
                  localStorage.setItem('gameQuery', playlistUrl);
                  localStorage.setItem('gameRounds', playlistRounds || '10');
                  toast.success('Starting playlist game!');
                  router.push('/');
                }
              }}
            >
              <Play className="h-4 w-4" />
              Start Game
            </Button>
          </CardContent>
        </Card>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium">Total Lists</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{lists.length}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium">Active Lists</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {lists.filter(l => l.is_active).length}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium">Total Songs</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {lists.reduce((sum, l) => sum + l.song_count, 0)}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium">Games Played</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {lists.reduce((sum, l) => sum + l.times_played, 0)}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Lists Grid */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent"></div>
            <p className="mt-4 text-muted-foreground">Loading lists...</p>
          </div>
        ) : error ? (
          <Card>
            <CardContent className="py-8 text-center">
              <p className="text-red-500">{error}</p>
              <Button onClick={loadLists} className="mt-4">
                Try Again
              </Button>
            </CardContent>
          </Card>
        ) : lists.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <Music className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
              <h3 className="text-lg font-semibold mb-2">No Custom Lists Yet</h3>
              <p className="text-muted-foreground mb-4">
                Create your first custom song list to get started!
              </p>
              <Button onClick={() => router.push('/admin/lists/new')} className="gap-2">
                <Plus className="h-4 w-4" />
                Create Your First List
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {lists.map((list) => (
              <Card key={list.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-xl mb-1">{list.name}</CardTitle>
                      {list.description && (
                        <CardDescription className="line-clamp-2">
                          {list.description}
                        </CardDescription>
                      )}
                    </div>
                    {!list.is_active && (
                      <Badge variant="secondary">Inactive</Badge>
                    )}
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {/* Metadata */}
                    <div className="flex flex-wrap gap-2">
                      {list.primary_decade && (
                        <Badge variant="outline" className="gap-1">
                          <Calendar className="h-3 w-3" />
                          {list.primary_decade}
                        </Badge>
                      )}
                      {list.primary_genre && (
                        <Badge variant="outline" className="gap-1">
                          <Music className="h-3 w-3" />
                          {list.primary_genre}
                        </Badge>
                      )}
                      {list.target_audience && (
                        <Badge variant="outline" className="gap-1">
                          <Users className="h-3 w-3" />
                          {list.target_audience}
                        </Badge>
                      )}
                    </div>

                    {/* Stats */}
                    <div className="flex items-center justify-between text-sm text-muted-foreground">
                      <span>{list.song_count} songs</span>
                      <span className="flex items-center gap-1">
                        <TrendingUp className="h-3 w-3" />
                        {list.times_played} plays
                      </span>
                    </div>

                    {/* Date */}
                    <div className="text-xs text-muted-foreground">
                      Updated {formatDate(list.updated_at)}
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2 pt-2">
                      <Button
                        size="sm"
                        variant="default"
                        className="flex-1 gap-2"
                        onClick={() => router.push(`/admin/lists/${list.id}`)}
                      >
                        <Edit className="h-3 w-3" />
                        Edit
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        className="gap-2"
                        onClick={() => {
                          // Start game with this custom list
                          localStorage.setItem('gameMode', 'customList');
                          localStorage.setItem('gameListId', list.id);
                          localStorage.setItem('gameListName', list.name);
                          localStorage.setItem('gameRounds', Math.min(list.song_count, 10).toString());
                          toast.success(`Starting game with "${list.name}"!`);
                          router.push('/');
                        }}
                      >
                        <Play className="h-3 w-3" />
                        Play
                      </Button>
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
