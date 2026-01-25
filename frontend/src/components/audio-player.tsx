"use client";

import { useEffect, useRef, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Play, Pause, Volume2, VolumeX } from 'lucide-react';

interface AudioPlayerProps {
  previewUrl: string;
  duration?: number;
  autoPlay?: boolean;
  onEnded?: () => void;
}

export function AudioPlayer({ 
  previewUrl, 
  duration = 10,
  autoPlay = false,
  onEnded 
}: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [isMuted, setIsMuted] = useState(false);
  const [hasEnded, setHasEnded] = useState(false);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateTime = () => {
      setCurrentTime(audio.currentTime);
      
      // Stop at specified duration (default 10s)
      if (audio.currentTime >= duration) {
        audio.pause();
        setIsPlaying(false);
        setHasEnded(true);
        if (onEnded) onEnded();
      }
    };

    const handleEnded = () => {
      setIsPlaying(false);
      setHasEnded(true);
      if (onEnded) onEnded();
    };

    audio.addEventListener('timeupdate', updateTime);
    audio.addEventListener('ended', handleEnded);

    if (autoPlay) {
      audio.play().catch(console.error);
      setIsPlaying(true);
    }

    return () => {
      audio.removeEventListener('timeupdate', updateTime);
      audio.removeEventListener('ended', handleEnded);
    };
  }, [previewUrl, duration, autoPlay, onEnded]);

  const togglePlay = async () => {
    const audio = audioRef.current;
    if (!audio) return;

    if (hasEnded) {
      audio.currentTime = 0;
      setHasEnded(false);
    }

    if (isPlaying) {
      audio.pause();
      setIsPlaying(false);
    } else {
      try {
        await audio.play();
        setIsPlaying(true);
      } catch (error) {
        console.error('Error playing audio:', error);
      }
    }
  };

  const toggleMute = () => {
    const audio = audioRef.current;
    if (!audio) return;
    
    audio.muted = !audio.muted;
    setIsMuted(!isMuted);
  };

  const progressPercentage = (currentTime / duration) * 100;

  return (
    <Card className="p-6">
      <audio ref={audioRef} src={previewUrl} preload="auto" />
      
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="text-sm text-muted-foreground">
            {Math.floor(currentTime)}s / {duration}s
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleMute}
            aria-label={isMuted ? "Unmute" : "Mute"}
          >
            {isMuted ? <VolumeX className="h-4 w-4" /> : <Volume2 className="h-4 w-4" />}
          </Button>
        </div>

        <Progress value={progressPercentage} className="w-full" />

        <Button
          onClick={togglePlay}
          className="w-full"
          size="lg"
          disabled={!previewUrl}
        >
          {isPlaying ? (
            <>
              <Pause className="mr-2 h-5 w-5" />
              Pause
            </>
          ) : (
            <>
              <Play className="mr-2 h-5 w-5" />
              {hasEnded ? 'Play Again' : 'Play 10s Preview'}
            </>
          )}
        </Button>
      </div>
    </Card>
  );
}
