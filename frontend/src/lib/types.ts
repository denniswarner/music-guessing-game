/**
 * TypeScript type definitions for the Music Guessing Game
 */

export interface SpotifyCredentials {
  client_id: string;
  client_secret: string;
}

export interface Artist {
  name: string;
}

export interface Album {
  name: string;
  release_date: string;
}

export interface Track {
  id: string;
  name: string;
  artists: Artist[];
  album: Album;
  preview_url: string | null;
}

export interface GameSession {
  session_id: string;
  total_rounds: number;
  current_round: number;
  score: number;
  songs: Track[];
}

export interface GuessResponse {
  correct: boolean;
  points_earned: number;
  correct_answer: string | null;
  artist_hint: string | null;
  total_score: number;
  is_final_guess: boolean;
}

export interface GameStats {
  total_rounds: number;
  score: number;
  percentage: number;
  rank: string;
}

export type GameMode = "genre" | "playlist" | "artist" | "demo";

export interface GameStartRequest {
  credentials: SpotifyCredentials;
  mode: GameMode;
  query: string;
  num_rounds: number;
  demo_mode?: boolean;
}

export interface GuessRequest {
  session_id: string;
  guess: string;
  round_number: number;
}
