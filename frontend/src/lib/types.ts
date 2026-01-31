/**
 * TypeScript type definitions for the Music Guessing Game
 */

export type MusicProvider = "spotify" | "deezer" | "demo" | "custom";

export interface MusicProviderCredentials {
  client_id: string;
  client_secret: string;
}

// Keep for backwards compatibility
export type SpotifyCredentials = MusicProviderCredentials;

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

export type GameMode = "genre" | "playlist" | "artist" | "demo" | "custom";

export interface GameStartRequest {
  provider: MusicProvider;
  credentials: MusicProviderCredentials;
  mode: GameMode;
  query: string;
  num_rounds: number;
  demo_mode?: boolean;
  custom_list_id?: string;
  custom_filters?: Record<string, string>;
}

export interface GuessRequest {
  session_id: string;
  guess: string;
  round_number: number;
}
