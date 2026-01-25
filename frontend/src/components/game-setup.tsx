"use client";

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Music } from 'lucide-react';
import type { SpotifyCredentials, GameMode } from '@/lib/types';

interface GameSetupProps {
  onStart: (credentials: SpotifyCredentials, mode: GameMode, query: string, rounds: number, demoMode: boolean) => void;
  isLoading?: boolean;
}

export function GameSetup({ onStart, isLoading = false }: GameSetupProps) {
  const [clientId, setClientId] = useState('');
  const [clientSecret, setClientSecret] = useState('');
  const [mode, setMode] = useState<GameMode>('genre');
  const [query, setQuery] = useState('');
  const [rounds, setRounds] = useState(10);
  const [demoMode, setDemoMode] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const credentials: SpotifyCredentials = {
      client_id: demoMode ? '' : clientId,
      client_secret: demoMode ? '' : clientSecret,
    };
    
    onStart(credentials, mode, query, rounds, demoMode);
  };

  const modeDescriptions: Record<GameMode, string> = {
    genre: demoMode ? 'Try: rock, pop, 80s, 70s, 60s' : 'Search by genre or era (e.g., "rock", "90s", "jazz")',
    playlist: demoMode ? 'Not available in demo mode' : 'Use any public Spotify playlist URL',
    artist: demoMode ? 'Try: Beatles, Queen, Michael Jackson, Nirvana' : 'Play songs from a specific artist',
    demo: 'Demo mode with classic songs',
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
            Test your music knowledge with 10-second preview clips!
          </CardDescription>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Demo Mode Toggle */}
            <div className="p-4 bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-lg">🎮 Demo Mode</h3>
                  <p className="text-sm text-muted-foreground">
                    Play with 20 classic songs - no Spotify credentials needed!
                  </p>
                </div>
                <Button
                  type="button"
                  variant={demoMode ? 'default' : 'outline'}
                  onClick={() => setDemoMode(!demoMode)}
                >
                  {demoMode ? 'Enabled' : 'Enable'}
                </Button>
              </div>
            </div>

            {/* Spotify Credentials - Hidden in Demo Mode */}
            {!demoMode && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="clientId">Spotify Client ID</Label>
                  <Input
                    id="clientId"
                    type="text"
                    placeholder="Your Spotify Client ID"
                    value={clientId}
                    onChange={(e) => setClientId(e.target.value)}
                    required={!demoMode}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="clientSecret">Spotify Client Secret</Label>
                  <Input
                    id="clientSecret"
                    type="password"
                    placeholder="Your Spotify Client Secret"
                    value={clientSecret}
                    onChange={(e) => setClientSecret(e.target.value)}
                    required={!demoMode}
                  />
                </div>

                <div className="text-sm text-muted-foreground">
                  Get your credentials from{' '}
                  <a
                    href="https://developer.spotify.com/dashboard"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary hover:underline"
                  >
                    Spotify Developer Dashboard
                  </a>
                </div>
              </div>
            )}

            {/* Game Mode Selection */}
            <div className="space-y-3">
              <Label>Game Mode</Label>
              <div className="grid grid-cols-3 gap-2">
                {(['genre', 'playlist', 'artist'] as GameMode[]).map((m) => (
                  <Button
                    key={m}
                    type="button"
                    variant={mode === m ? 'default' : 'outline'}
                    onClick={() => setMode(m)}
                    className="capitalize"
                    disabled={demoMode && m === 'playlist'}
                  >
                    {m}
                  </Button>
                ))}
              </div>
              <p className="text-sm text-muted-foreground">
                {modeDescriptions[mode]}
              </p>
            </div>

            {/* Query Input */}
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
                  mode === 'playlist' ? 'https://open.spotify.com/playlist/...' :
                  demoMode ? 'e.g., Beatles, Queen (or leave blank for all)' : 'e.g., The Beatles, Taylor Swift'
                }
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                required={!demoMode}
                disabled={demoMode && mode === 'playlist'}
              />
            </div>

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
