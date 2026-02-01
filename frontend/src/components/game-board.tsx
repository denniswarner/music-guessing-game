"use client";

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { AudioPlayer } from './audio-player';
import { Check, X, Music, Trophy, Home, Timer } from 'lucide-react';
import { submitGuess } from '@/lib/api';
import type { GameSession, Track, GuessResponse } from '@/lib/types';

interface GameBoardProps {
  session: GameSession;
  onRestart: () => void;
}

type GameState = 'playing-audio' | 'guessing' | 'showing-result' | 'between-rounds' | 'game-over';

interface RoundResult {
  correct: boolean;
  userGuess: string;
  correctAnswer: string;
  songTitle: string;
  points: number;
}

export function GameBoard({ session, onRestart }: GameBoardProps) {
  const [currentRound, setCurrentRound] = useState(0);
  const [guess, setGuess] = useState('');
  const [gameState, setGameState] = useState<GameState>('playing-audio');
  const [totalScore, setTotalScore] = useState(0);
  const [guessTimeLeft, setGuessTimeLeft] = useState(10);
  const [hasGuessed, setHasGuessed] = useState(false);
  const [roundResults, setRoundResults] = useState<RoundResult[]>([]);
  const [currentResult, setCurrentResult] = useState<RoundResult | null>(null);
  const [betweenRoundsCount, setBetweenRoundsCount] = useState(3);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const currentSong = session.songs[currentRound];
  const progressPercentage = ((currentRound + 1) / session.total_rounds) * 100;

  // Start guessing timer after audio finishes
  useEffect(() => {
    if (gameState === 'playing-audio') {
      const audioTimer = setTimeout(() => {
        setGameState('guessing');
        setGuessTimeLeft(10);
      }, 10000); // 10 seconds for audio
      
      return () => clearTimeout(audioTimer);
    }
  }, [gameState, currentRound]);

  // Countdown timer during guessing phase
  useEffect(() => {
    if (gameState === 'guessing' && guessTimeLeft > 0 && !hasGuessed) {
      timerRef.current = setTimeout(() => {
        setGuessTimeLeft(guessTimeLeft - 1);
      }, 1000);
      
      return () => {
        if (timerRef.current) clearTimeout(timerRef.current);
      };
    } else if (gameState === 'guessing' && guessTimeLeft === 0 && !hasGuessed) {
      // Time's up!
      handleTimeUp();
    }
  }, [gameState, guessTimeLeft, hasGuessed]);

  // Between-rounds countdown
  useEffect(() => {
    if (gameState === 'between-rounds') {
      if (betweenRoundsCount > 0) {
        const timer = setTimeout(() => {
          setBetweenRoundsCount(betweenRoundsCount - 1);
        }, 1000);
        return () => clearTimeout(timer);
      } else {
        // Countdown finished, start playing audio
        setGameState('playing-audio');
      }
    }
  }, [gameState, betweenRoundsCount]);

  // Get artist name from current song
  const getArtistName = () => {
    return currentSong.artists?.[0]?.name || 'Unknown Artist';
  };

  const handleTimeUp = async () => {
    if (hasGuessed) return;
    
    setHasGuessed(true);
    
    const result: RoundResult = {
      correct: false,
      userGuess: '(No answer)',
      correctAnswer: getArtistName(),
      songTitle: currentSong.name,
      points: 0
    };
    
    setCurrentResult(result);
    setRoundResults([...roundResults, result]);
    setGameState('showing-result');
    
    // Move to next round after showing result
    setTimeout(() => {
      moveToNextRound();
    }, 2000);
  };

  const handleSubmitGuess = async () => {
    if (!guess.trim() || hasGuessed) return;

    setHasGuessed(true);
    
    try {
      const response = await submitGuess(
        session.session_id,
        guess.trim(),
        currentRound
      );

      const points = response.correct ? 2 : 0;
      const result: RoundResult = {
        correct: response.correct,
        userGuess: guess.trim(),
        correctAnswer: getArtistName(),
        songTitle: currentSong.name,
        points: points
      };

      if (response.correct) {
        setTotalScore(totalScore + points);
      }

      setCurrentResult(result);
      setRoundResults([...roundResults, result]);
      setGameState('showing-result');

      // Move to next round after showing result
      setTimeout(() => {
        moveToNextRound();
      }, 2000);
    } catch (error) {
      console.error('Error submitting guess:', error);
      setHasGuessed(false);
      alert('Failed to submit guess. Please try again.');
    }
  };

  const moveToNextRound = () => {
    if (currentRound + 1 >= session.total_rounds) {
      // Game over
      setGameState('game-over');
    } else {
      // Show between-rounds countdown
      setCurrentRound(currentRound + 1);
      setGuess('');
      setCurrentResult(null);
      setHasGuessed(false);
      setBetweenRoundsCount(3);
      setGameState('between-rounds');
      setGuessTimeLeft(10);
    }
  };

  if (gameState === 'game-over') {
    const correctCount = roundResults.filter(r => r.correct).length;
    const percentage = (correctCount / session.total_rounds) * 100;
    
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="w-full max-w-3xl"
        >
          <Card>
            <CardHeader className="text-center">
              <div className="flex justify-center mb-4">
                <div className="p-4 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-full">
                  <Trophy className="h-16 w-16 text-white" />
                </div>
              </div>
              <CardTitle className="text-3xl font-bold">Game Over!</CardTitle>
              <CardDescription className="text-lg">
                Final Score: {totalScore} points
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-4 text-center">
                <div className="p-6 bg-muted rounded-lg">
                  <div className="text-4xl font-bold text-primary">{correctCount}/{session.total_rounds}</div>
                  <div className="text-sm text-muted-foreground">Correct</div>
                </div>
                <div className="p-6 bg-muted rounded-lg">
                  <div className="text-4xl font-bold text-primary">{percentage.toFixed(0)}%</div>
                  <div className="text-sm text-muted-foreground">Accuracy</div>
                </div>
              </div>

              {/* All Answers */}
              <div className="space-y-3">
                <h3 className="font-semibold text-lg">All Answers:</h3>
                {roundResults.map((result, index) => (
                  <div
                    key={index}
                    className={`p-4 rounded-lg border-2 ${
                      result.correct
                        ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
                        : 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-semibold">Round {index + 1}:</span>
                          {result.correct ? (
                            <Check className="h-5 w-5 text-green-600" />
                          ) : (
                            <X className="h-5 w-5 text-red-600" />
                          )}
                        </div>
                        <div className="text-sm space-y-1">
                          <div>Your answer: <span className="font-medium">{result.userGuess}</span></div>
                          <div className="text-muted-foreground">
                            Artist: <span className="font-medium">{result.correctAnswer}</span>
                          </div>
                          <div className="text-muted-foreground text-xs">
                            Song: "{result.songTitle}"
                          </div>
                        </div>
                      </div>
                      {result.correct && (
                        <Badge variant="secondary">+{result.points} pts</Badge>
                      )}
                    </div>
                  </div>
                ))}
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

        {/* Between Rounds Countdown */}
        {gameState === 'between-rounds' && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-purple-600 to-blue-600"
          >
            <div className="text-center">
              <motion.div
                key={betweenRoundsCount}
                initial={{ scale: 0.5, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 1.5, opacity: 0 }}
                transition={{ duration: 0.3 }}
              >
                <div className="text-9xl font-bold text-white drop-shadow-2xl">
                  {betweenRoundsCount}
                </div>
              </motion.div>
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mt-6 text-xl text-white/80"
              >
                Next song coming up...
              </motion.p>
            </div>
          </motion.div>
        )}

        {/* Audio Player - Only shows during playing-audio state */}
        {gameState === 'playing-audio' && (
          <AudioPlayer
            key={`audio-${currentRound}-${currentSong.id}`}
            previewUrl={currentSong.preview_url || ''}
            duration={10}
            autoPlay={true}
            demoMode={currentSong.preview_url?.includes('mock')}
          />
        )}

        {/* Guessing Phase with Timer */}
        {gameState === 'guessing' && (
          <AnimatePresence>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              {/* Timer */}
              <Card className="bg-gradient-to-r from-blue-500 to-purple-500">
                <CardContent className="py-8">
                  <div className="text-center">
                    <Timer className="h-12 w-12 mx-auto mb-4 text-white" />
                    <div className="text-6xl font-bold text-white mb-2">
                      {guessTimeLeft}
                    </div>
                    <div className="text-white/80">seconds remaining</div>
                  </div>
                </CardContent>
              </Card>

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
                    <Input
                      type="text"
                      placeholder="Enter artist name..."
                      value={guess}
                      onChange={(e) => setGuess(e.target.value)}
                      disabled={hasGuessed}
                      autoFocus
                      className="text-lg py-6"
                    />

                    <Button
                      type="submit"
                      className="w-full"
                      size="lg"
                      disabled={!guess.trim() || hasGuessed}
                    >
                      Submit Guess
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </motion.div>
          </AnimatePresence>
        )}

        {/* Result Feedback */}
        {gameState === 'showing-result' && currentResult && (
          <AnimatePresence>
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
            >
              {currentResult.correct ? (
                <Card className="bg-green-100 dark:bg-green-900/20 border-green-200 dark:border-green-800">
                  <CardContent className="py-12 text-center">
                    <Check className="h-20 w-20 mx-auto mb-4 text-green-600" />
                    <div className="text-3xl font-bold text-green-900 dark:text-green-100 mb-2">
                      Correct!
                    </div>
                    <div className="text-xl text-green-700 dark:text-green-300">
                      +{currentResult.points} points
                    </div>
                  </CardContent>
                </Card>
              ) : (
                <Card className="bg-red-100 dark:bg-red-900/20 border-red-200 dark:border-red-800">
                  <CardContent className="py-12 text-center">
                    <X className="h-20 w-20 mx-auto mb-4 text-red-600" />
                    <div className="text-3xl font-bold text-red-900 dark:text-red-100 mb-2">
                      {currentResult.userGuess === '(No answer)' ? "Time's Up!" : 'Nope!'}
                    </div>
                    <div className="text-xl text-red-700 dark:text-red-300 mb-2">
                      The artist was:
                    </div>
                    <div className="text-2xl font-semibold text-red-900 dark:text-red-100 mb-2">
                      {currentResult.correctAnswer}
                    </div>
                    <div className="text-sm text-red-700 dark:text-red-300">
                      Song: "{currentResult.songTitle}"
                    </div>
                  </CardContent>
                </Card>
              )}
            </motion.div>
          </AnimatePresence>
        )}
      </div>
    </div>
  );
}
