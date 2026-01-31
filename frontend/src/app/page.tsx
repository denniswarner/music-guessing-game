"use client";

import { useState } from 'react';
import { GameSetup } from '@/components/game-setup';
import { GameBoard } from '@/components/game-board';
import { startGame } from '@/lib/api';
import type { MusicProviderCredentials, MusicProvider, GameMode, GameSession } from '@/lib/types';

export default function Home() {
  const [gameSession, setGameSession] = useState<GameSession | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleStartGame = async (
    provider: MusicProvider,
    credentials: MusicProviderCredentials,
    mode: GameMode,
    query: string,
    rounds: number,
    demoMode: boolean,
    customListId?: string
  ) => {
    setIsLoading(true);
    setError(null);

    try {
      const session = await startGame(provider, credentials, mode, query, rounds, demoMode, customListId);
      setGameSession(session);
    } catch (err: any) {
      console.error('Failed to start game:', err);
      setError(
        err.response?.data?.detail || 
        'Failed to start game. Please check your credentials and try again.'
      );
      alert(error || 'Failed to start game');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestart = () => {
    setGameSession(null);
    setError(null);
  };

  if (gameSession) {
    return <GameBoard session={gameSession} onRestart={handleRestart} />;
  }

  return <GameSetup onStart={handleStartGame} isLoading={isLoading} />;
}
