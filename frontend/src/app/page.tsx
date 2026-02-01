"use client";

import { useState, useEffect } from 'react';
import { GameSetup } from '@/components/game-setup';
import { GameBoard } from '@/components/game-board';
import { GameCountdown } from '@/components/game-countdown';
import { startGame } from '@/lib/api';
import type { MusicProviderCredentials, MusicProvider, GameMode, GameSession } from '@/lib/types';

export default function Home() {
  const [gameSession, setGameSession] = useState<GameSession | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showCountdown, setShowCountdown] = useState(false);
  const [gameReady, setGameReady] = useState(false);

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
      setIsLoading(false);
      // Start countdown after game session is ready
      setShowCountdown(true);
    } catch (err: any) {
      console.error('Failed to start game:', err);
      setError(
        err.response?.data?.detail || 
        'Failed to start game. Please check your credentials and try again.'
      );
      alert(error || 'Failed to start game');
      setIsLoading(false);
    }
  };

  const handleCountdownComplete = () => {
    setShowCountdown(false);
    setGameReady(true);
  };

  const handleRestart = () => {
    setGameSession(null);
    setError(null);
    setShowCountdown(false);
    setGameReady(false);
  };

  // Show countdown after game loads
  if (showCountdown && gameSession) {
    return <GameCountdown onComplete={handleCountdownComplete} />;
  }

  // Show game board after countdown
  if (gameReady && gameSession) {
    return <GameBoard session={gameSession} onRestart={handleRestart} />;
  }

  return <GameSetup onStart={handleStartGame} isLoading={isLoading} />;
}
