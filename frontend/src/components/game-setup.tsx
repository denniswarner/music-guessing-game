"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Music } from 'lucide-react';
import type { MusicProviderCredentials, MusicProvider, GameMode } from '@/lib/types';

interface GameSetupProps {
  onStart: (provider: MusicProvider, credentials: MusicProviderCredentials, mode: GameMode, query: string, rounds: number, demoMode: boolean, customListId?: string) => void;
  isLoading?: boolean;
}

export function GameSetup({ onStart, isLoading = false }: GameSetupProps) {
  const [provider, setProvider] = useState<MusicProvider>('deezer');
  const [clientId, setClientId] = useState('');
  const [clientSecret, setClientSecret] = useState('');
  const [mode, setMode] = useState<GameMode>('genre');
  const [query, setQuery] = useState('');
  const [rounds, setRounds] = useState(10);
  const [demoMode, setDemoMode] = useState(false);
  
  // Custom list state
  const [customListId, setCustomListId] = useState<string | null>(null);
  const [customListName, setCustomListName] = useState<string | null>(null);

  // Load provider settings from localStorage on mount
  useEffect(() => {
    const savedProvider = localStorage.getItem('musicProvider') as MusicProvider;
    const savedClientId = localStorage.getItem('spotifyClientId');
    const savedClientSecret = localStorage.getItem('spotifyClientSecret');
    
    if (savedProvider) {
      setProvider(savedProvider);
      setDemoMode(savedProvider === 'demo');
    }
    if (savedClientId) setClientId(savedClientId);
    if (savedClientSecret) setClientSecret(savedClientSecret);

    // Check for persistent active playlist (set by admin, persists until changed)
    const activeListId = localStorage.getItem('activePlaylistId');
    const activeListName = localStorage.getItem('activePlaylistName');
    const activeRounds = localStorage.getItem('activePlaylistRounds');
    
    if (activeListId && activeListName) {
      // Admin has set an active playlist - use it
      setMode('custom');
      setCustomListId(activeListId);
      setCustomListName(activeListName);
      if (activeRounds) setRounds(parseInt(activeRounds));
    } else {
      // Check for one-time game triggers (e.g., external playlist)
      const gameMode = localStorage.getItem('gameMode');
      const gameQuery = localStorage.getItem('gameQuery');
      const gameRounds = localStorage.getItem('gameRounds');
      
      if (gameMode === 'playlist' && gameQuery) {
        // External playlist mode (one-time)
        setMode('playlist');
        setQuery(gameQuery);
        if (gameRounds) setRounds(parseInt(gameRounds));
        // Clear one-time triggers
        localStorage.removeItem('gameMode');
        localStorage.removeItem('gameQuery');
        localStorage.removeItem('gameRounds');
      }
    }
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const credentials: MusicProviderCredentials = {
      client_id: (demoMode || provider === 'deezer') ? '' : clientId,
      client_secret: (demoMode || provider === 'deezer') ? '' : clientSecret,
    };
    
    onStart(provider, credentials, mode, query, rounds, demoMode, customListId || undefined);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
      <Card className="w-full max-w-2xl">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="p-4 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full">
              <Music className="h-12 w-12 text-white" />
            </div>
          </div>
          <CardTitle className="text-3xl font-bold">Music Guessing Game</CardTitle>
          <CardDescription className="text-lg">
            Test your music knowledge with audio preview clips!
          </CardDescription>
          
          {/* Admin Link */}
          <div className="mt-4">
            <Button
              variant="link"
              onClick={() => window.location.href = '/admin'}
              className="text-sm"
            >
              🎨 Admin Dashboard
            </Button>
          </div>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Show playlist info if in playlist mode from admin */}
            {mode === 'playlist' && (
              <div className="p-4 bg-blue-100 dark:bg-blue-900/20 rounded-lg">
                <h3 className="font-semibold text-sm mb-1">🎵 Playlist Mode</h3>
                <p className="text-xs text-muted-foreground">
                  Starting game with external playlist configured from Admin Dashboard
                </p>
              </div>
            )}

            {/* Show custom list info if playing a custom list */}
            {customListId && customListName && (
              <div className="p-4 bg-purple-100 dark:bg-purple-900/20 rounded-lg">
                <h3 className="font-semibold text-sm mb-1">🎶 Custom Playlist</h3>
                <p className="text-sm font-medium">{customListName}</p>
                <p className="text-xs text-muted-foreground mt-1">
                  Playing songs from your curated playlist
                </p>
              </div>
            )}

            {/* Search Input - Only show in normal game mode (no custom list or playlist) */}
            {!customListId && mode !== 'playlist' && (
              <div className="space-y-2">
                <Label htmlFor="query">Search Songs</Label>
                <Input
                  id="query"
                  type="text"
                  placeholder="Search by artist, genre, or era (e.g., Queen, 80s rock, jazz)"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
                <p className="text-xs text-muted-foreground">
                  Try: "Beatles", "90s", "hip hop", "Michael Jackson", etc.
                </p>
              </div>
            )}

            {/* Number of Rounds */}
            <div className="space-y-2">
              <Label htmlFor="rounds">Number of Rounds</Label>
              <Input
                id="rounds"
                type="number"
                min="1"
                max="50"
                value={rounds}
                onChange={(e) => setRounds(parseInt(e.target.value) || 10)}
              />
              {demoMode && rounds > 20 && (
                <p className="text-xs text-amber-600 dark:text-amber-400">
                  Note: Demo mode has only 20 songs. Rounds will be adjusted automatically.
                </p>
              )}
            </div>

            {/* Start Button */}
            <Button
              type="submit"
              className="w-full"
              size="lg"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-background border-t-transparent" />
                  Starting Game...
                </>
              ) : (
                'Start Game'
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
