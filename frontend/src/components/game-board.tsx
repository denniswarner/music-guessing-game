"use client";

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { AudioPlayer } from './audio-player';
import { Check, X, Music, Trophy, Home } from 'lucide-react';
import { submitGuess, getGameStats } from '@/lib/api';
import type { GameSession, Track, GuessResponse, GameStats } from '@/lib/types';

interface GameBoardProps {
  session: GameSession;
  onRestart: () => void;
}

type GameState = 'playing' | 'waiting-hint' | 'game-over';

export function GameBoard({ session, onRestart }: GameBoardProps) {
  const [currentRound, setCurrentRound] = useState(0);
  const [guess, setGuess] = useState('');
  const [gameState, setGameState] = useState<GameState>('playing');
  const [totalScore, setTotalScore] = useState(0);
  const [lastResponse, setLastResponse] = useState<GuessResponse | null>(null);
  const [showHints, setShowHints] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [stats, setStats] = useState<GameStats | null>(null);

  const currentSong = session.songs[currentRound];
  const progressPercentage = ((currentRound + 1) / session.total_rounds) * 100;

  useEffect(() => {
    // Show hints after audio plays
    const timer = setTimeout(() => setShowHints(true), 1000);
    return () => clearTimeout(timer);
  }, [currentRound]);

  const handleSubmitGuess = async () => {
    if (!guess.trim() || isSubmitting) return;

    setIsSubmitting(true);

    try {
      const response = await submitGuess(
        session.session_id,
        guess.trim(),
        currentRound
      );

      setLastResponse(response);
      setTotalScore(response.total_score);

      if (response.is_final_guess) {
        // Move to next round or end game
        if (currentRound + 1 >= session.total_rounds) {
          // Game over
          const finalStats = await getGameStats(session.session_id);
          setStats(finalStats);
          setGameState('game-over');
        } else {
          // Next round
          setTimeout(() => {
            setCurrentRound(currentRound + 1);
            setGuess('');
            setLastResponse(null);
            setShowHints(false);
            setGameState('playing');
          }, 3000);
        }
      } else {
        // Waiting for second guess with artist hint
        setGameState('waiting-hint');
        setGuess('');
      }
    } catch (error) {
      console.error('Error submitting guess:', error);
      alert('Failed to submit guess. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (gameState === 'game-over' && stats) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <Card className="w-full max-w-2xl">
            <CardHeader className="text-center">
              <div className="flex justify-center mb-4">
                <div className="p-4 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-full">
                  <Trophy className="h-16 w-16 text-white" />
                </div>
              </div>
              <CardTitle className="text-3xl font-bold">Game Over!</CardTitle>
              <CardDescription className="text-lg">
                Here's how you did
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-4 text-center">
                <div className="p-6 bg-muted rounded-lg">
                  <div className="text-4xl font-bold text-primary">{stats.score}</div>
                  <div className="text-sm text-muted-foreground">Score</div>
                </div>
                <div className="p-6 bg-muted rounded-lg">
                  <div className="text-4xl font-bold text-primary">{stats.percentage.toFixed(0)}%</div>
                  <div className="text-sm text-muted-foreground">Accuracy</div>
                </div>
              </div>

              <div className="text-center p-6 bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg">
                <div className="text-2xl font-bold mb-2">
                  {stats.rank === 'MUSIC MASTER' && '🏆 MUSIC MASTER!'}
                  {stats.rank === 'Great job' && '🎵 Great job!'}
                  {stats.rank === 'Not bad' && '🎶 Not bad!'}
                  {stats.rank === 'Keep practicing' && '🎼 Keep practicing!'}
                </div>
                <div className="text-sm text-muted-foreground">
                  You got {stats.score} out of {stats.total_rounds} rounds
                </div>
              </div>

              <div className="flex gap-3">
                <Button onClick={onRestart} className="flex-1" size="lg">
                  <Home className="mr-2 h-5 w-5" />
                  New Game
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-4 bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
      <div className="max-w-4xl mx-auto space-y-6 py-8">
        {/* Header */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Round {currentRound + 1} of {session.total_rounds}</CardTitle>
                <CardDescription>Score: {totalScore} points</CardDescription>
              </div>
              <Badge variant="secondary" className="text-lg px-4 py-2">
                <Music className="mr-2 h-4 w-4" />
                {currentRound + 1}/{session.total_rounds}
              </Badge>
            </div>
            <Progress value={progressPercentage} className="mt-4" />
          </CardHeader>
        </Card>

        {/* Audio Player */}
        <AudioPlayer
          previewUrl={currentSong.preview_url || ''}
          duration={10}
          autoPlay={true}
        />

        {/* Hints */}
        <AnimatePresence>
          {showHints && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">💡 Hints</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Album:</span>
                    <span className="font-medium">{currentSong.album.name}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Released:</span>
                    <span className="font-medium">
                      {new Date(currentSong.album.release_date).getFullYear()}
                    </span>
                  </div>
                  {lastResponse?.artist_hint && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="flex justify-between pt-2 border-t"
                    >
                      <span className="text-muted-foreground">Artist:</span>
                      <span className="font-medium text-primary">{lastResponse.artist_hint}</span>
                    </motion.div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Guess Input */}
        <Card>
          <CardContent className="pt-6">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSubmitGuess();
              }}
              className="space-y-4"
            >
              <div className="space-y-2">
                <Label htmlFor="guess">
                  {lastResponse?.artist_hint ? 'Second Guess (1 point)' : 'Your Guess (2 points)'}
                </Label>
                <Input
                  id="guess"
                  type="text"
                  placeholder="Enter song title..."
                  value={guess}
                  onChange={(e) => setGuess(e.target.value)}
                  disabled={isSubmitting}
                  autoFocus
                />
              </div>

              <Button
                type="submit"
                className="w-full"
                size="lg"
                disabled={!guess.trim() || isSubmitting}
              >
                {isSubmitting ? 'Submitting...' : 'Submit Guess'}
              </Button>
            </form>

            {/* Response Feedback */}
            <AnimatePresence>
              {lastResponse && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="mt-4"
                >
                  {lastResponse.correct ? (
                    <div className="p-4 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center gap-3">
                      <Check className="h-6 w-6 text-green-600" />
                      <div>
                        <div className="font-semibold text-green-900 dark:text-green-100">
                          Correct! +{lastResponse.points_earned} points
                        </div>
                        {lastResponse.is_final_guess && (
                          <div className="text-sm text-green-700 dark:text-green-300">
                            Moving to next round...
                          </div>
                        )}
                      </div>
                    </div>
                  ) : lastResponse.correct_answer ? (
                    <div className="p-4 bg-red-100 dark:bg-red-900/20 rounded-lg flex items-center gap-3">
                      <X className="h-6 w-6 text-red-600" />
                      <div>
                        <div className="font-semibold text-red-900 dark:text-red-100">
                          Incorrect
                        </div>
                        <div className="text-sm text-red-700 dark:text-red-300">
                          The answer was: {lastResponse.correct_answer}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="p-4 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg flex items-center gap-3">
                      <X className="h-6 w-6 text-yellow-600" />
                      <div>
                        <div className="font-semibold text-yellow-900 dark:text-yellow-100">
                          Not quite! Try again with the artist hint
                        </div>
                      </div>
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
