/**
 * API Client for Music Guessing Game Backend
 */

import axios from 'axios';
import type {
  GameSession,
  GameStartRequest,
  GuessRequest,
  GuessResponse,
  GameStats,
  Track,
  SpotifyCredentials,
  GameMode
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Start a new game session
 */
export async function startGame(
  credentials: SpotifyCredentials,
  mode: GameMode,
  query: string,
  numRounds: number = 10
): Promise<GameSession> {
  const response = await api.post<GameSession>('/api/game/start', {
    credentials,
    mode,
    query,
    num_rounds: numRounds,
  });
  return response.data;
}

/**
 * Submit a guess for the current round
 */
export async function submitGuess(
  sessionId: string,
  guess: string,
  roundNumber: number
): Promise<GuessResponse> {
  const response = await api.post<GuessResponse>('/api/game/guess', {
    session_id: sessionId,
    guess,
    round_number: roundNumber,
  });
  return response.data;
}

/**
 * Get current session information
 */
export async function getSessionInfo(sessionId: string): Promise<any> {
  const response = await api.get(`/api/game/session/${sessionId}`);
  return response.data;
}

/**
 * Get final game statistics
 */
export async function getGameStats(sessionId: string): Promise<GameStats> {
  const response = await api.get<GameStats>(`/api/game/stats/${sessionId}`);
  return response.data;
}

/**
 * End a game session
 */
export async function endGame(sessionId: string): Promise<void> {
  await api.delete(`/api/game/session/${sessionId}`);
}

/**
 * Search for songs
 */
export async function searchSongs(
  credentials: SpotifyCredentials,
  mode: GameMode,
  query: string
): Promise<Track[]> {
  const response = await api.post<Track[]>('/api/songs/search', {
    credentials,
    mode,
    query,
  });
  return response.data;
}

/**
 * Check API health
 */
export async function healthCheck(): Promise<{ status: string }> {
  const response = await api.get('/health');
  return response.data;
}
