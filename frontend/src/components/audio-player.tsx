"use client";

import { useEffect, useRef, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Music, Volume2 } from 'lucide-react';

interface AudioPlayerProps {
  previewUrl: string;
  duration?: number;
  autoPlay?: boolean;
  onEnded?: () => void;
  demoMode?: boolean;
}

export function AudioPlayer({ 
  previewUrl, 
  duration = 10,
  autoPlay = false,
  onEnded,
  demoMode = false
}: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const hasStartedRef = useRef(false);
  const [currentTime, setCurrentTime] = useState(0);

  // Reset hasStarted when previewUrl changes
  useEffect(() => {
    hasStartedRef.current = false;
  }, [previewUrl]);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateTime = () => {
      setCurrentTime(audio.currentTime);
      
      // Stop at specified duration (default 10s)
      if (audio.currentTime >= duration) {
        audio.pause();
        if (onEnded) onEnded();
      }
    };

    const handleEnded = () => {
      if (onEnded) onEnded();
    };

    const startPlayback = () => {
      // Only start once per song
      if (hasStartedRef.current) return;
      hasStartedRef.current = true;
      
      audio.play()
        .catch((err) => {
          console.error('AutoPlay failed:', err);
          hasStartedRef.current = false; // Allow retry
        });
    };

    const handleCanPlay = () => {
      if (autoPlay) {
        startPlayback();
      }
    };

    const handleError = () => {
      // Silently handle audio load errors (e.g., no valid source)
      console.log('Audio load error - preview may not be available');
    };

    audio.addEventListener('timeupdate', updateTime);
    audio.addEventListener('ended', handleEnded);
    audio.addEventListener('canplaythrough', handleCanPlay);
    audio.addEventListener('error', handleError);

    // Try to play immediately if audio is already loaded
    if (autoPlay && audio.readyState >= 3) {
      startPlayback();
    }

    return () => {
      audio.removeEventListener('timeupdate', updateTime);
      audio.removeEventListener('ended', handleEnded);
      audio.removeEventListener('canplaythrough', handleCanPlay);
      audio.removeEventListener('error', handleError);
    };
  }, [previewUrl, duration, autoPlay, onEnded]);

  const progressPercentage = (currentTime / duration) * 100;
  const isDemoUrl = previewUrl?.includes('mock');
  const hasValidUrl = previewUrl && previewUrl.length > 0 && !isDemoUrl;

  return (
    <Card className="p-6">
      {(demoMode || !hasValidUrl) && (
        <div className="mb-4 p-3 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg text-sm">
          <p className="font-semibold text-yellow-900 dark:text-yellow-100">
            🎵 {demoMode ? 'Demo Mode' : 'Audio Unavailable'}
          </p>
          <p className="text-yellow-700 dark:text-yellow-300">
            {demoMode 
              ? 'Audio playback not available in demo mode. Use your music knowledge to guess the song!'
              : 'No audio preview available for this song.'}
          </p>
        </div>
      )}
      <audio ref={audioRef} src={hasValidUrl ? previewUrl : undefined} preload="auto" />
      
      <div className="space-y-4">
        {/* Now Playing indicator */}
        <div className="flex items-center justify-center gap-3 py-2">
          <Volume2 className="h-5 w-5 text-primary animate-pulse" />
          <span className="text-lg font-medium">Now Playing...</span>
        </div>
        
        <div className="flex items-center justify-between text-sm text-muted-foreground">
          <span>{Math.floor(currentTime)}s</span>
          <span>{duration}s</span>
        </div>

        <Progress value={progressPercentage} className="w-full h-3" />
      </div>
    </Card>
  );
}
