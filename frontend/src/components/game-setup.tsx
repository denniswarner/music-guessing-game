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

    // Check if admin set up a game (playlist or custom list)
    const gameMode = localStorage.getItem('gameMode');
    const gameQuery = localStorage.getItem('gameQuery');
    const gameRounds = localStorage.getItem('gameRounds');
    const gameListId = localStorage.getItem('gameListId');
    const gameListName = localStorage.getItem('gameListName');
    
    if (gameMode === 'playlist' && gameQuery) {
      // External playlist mode
      setMode('playlist');
      setQuery(gameQuery);
      if (gameRounds) setRounds(parseInt(gameRounds));
      // Clear the stored settings after loading
      localStorage.removeItem('gameMode');
      localStorage.removeItem('gameQuery');
      localStorage.removeItem('gameRounds');
    } else if (gameMode === 'customList' && gameListId) {
      // Custom list mode
      setMode('custom');
      setCustomListId(gameListId);
      setCustomListName(gameListName);
      if (gameRounds) setRounds(parseInt(gameRounds));
      // Clear the stored settings after loading
      localStorage.removeItem('gameMode');
      localStorage.removeItem('gameListId');
      localStorage.removeItem('gameListName');
      localStorage.removeItem('gameRounds');
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

  const modeDescriptions: Record<GameMode, string> = {
    genre: demoMode ? 'Try: rock, pop, 80s, 70s, 60s' : 'Search by genre or era (e.g., "rock", "90s", "jazz")',
    playlist: demoMode ? 'Not available in demo mode' : provider === 'deezer' ? 'Use any public Deezer playlist URL or ID' : 'Use any public Spotify playlist URL',
    artist: demoMode ? 'Try: Beatles, Queen, Michael Jackson, Nirvana' : 'Play songs from a specific artist',
    demo: 'Demo mode with classic songs',
    custom: 'Play songs from your custom playlist',
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
            {/* Music Provider Selection - HIDDEN - Always uses Demo */}
            {/* Provider selection moved to Admin Dashboard */}
            
            {/* Game Mode Selection - Only show if not playlist mode from admin and not custom list */}
            {mode !== 'playlist' && !customListId && (
              <div className="space-y-3">
                <Label>Game Mode</Label>
                <div className="grid grid-cols-2 gap-2">
                  {(['genre', 'artist'] as GameMode[]).map((m) => (
                    <Button
                      key={m}
                      type="button"
                      variant={mode === m ? 'default' : 'outline'}
                      onClick={() => setMode(m)}
                      className="capitalize"
                    >
                      {m}
                    </Button>
                  ))}
                </div>
                <p className="text-sm text-muted-foreground">
                  {modeDescriptions[mode]}
                </p>
              </div>
            )}

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

            {/* Query Input - Hide when using custom list */}
            {!customListId && (
              <div className="space-y-2">
                <Label htmlFor="query">
                  {mode === 'genre' && (demoMode ? 'Genre or Era (Optional)' : 'Genre or Era')}
                  {mode === 'playlist' && 'Playlist URL'}
                  {mode === 'artist' && (demoMode ? 'Artist Name (Optional)' : 'Artist Name')}
                </Label>
                <Input
                  id="query"
                  type="text"
                  placeholder={
                    mode === 'genre' ? (demoMode ? 'e.g., rock, pop, 80s (or leave blank for all)' : 'e.g., rock, 90s, jazz') :
                    mode === 'playlist' ? 'Playlist URL from admin' :
                    demoMode ? 'e.g., Beatles, Queen (or leave blank for all)' : 'e.g., The Beatles, Taylor Swift'
                  }
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  required={!demoMode && mode !== 'genre'}
                  disabled={mode === 'playlist'}
                />
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
