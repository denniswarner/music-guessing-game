"use client";

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Music } from 'lucide-react';

interface GameCountdownProps {
  onComplete: () => void;
}

export function GameCountdown({ onComplete }: GameCountdownProps) {
  const [count, setCount] = useState(3);

  useEffect(() => {
    if (count === 0) {
      // Small delay before transitioning to game
      const timer = setTimeout(() => {
        onComplete();
      }, 500);
      return () => clearTimeout(timer);
    }

    const timer = setTimeout(() => {
      setCount(count - 1);
    }, 1000);

    return () => clearTimeout(timer);
  }, [count, onComplete]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-600 to-blue-600">
      <div className="text-center">
        <AnimatePresence mode="wait">
          {count > 0 ? (
            <motion.div
              key={count}
              initial={{ scale: 0.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 1.5, opacity: 0 }}
              transition={{ duration: 0.5 }}
              className="relative"
            >
              {/* Pulsing ring */}
              <motion.div
                className="absolute inset-0 flex items-center justify-center"
                initial={{ scale: 1, opacity: 0.5 }}
                animate={{ scale: 1.5, opacity: 0 }}
                transition={{ duration: 1, repeat: Infinity }}
              >
                <div className="w-48 h-48 rounded-full border-4 border-white/30" />
              </motion.div>
              
              {/* Number */}
              <div className="w-48 h-48 flex items-center justify-center">
                <span className="text-9xl font-bold text-white drop-shadow-2xl">
                  {count}
                </span>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="go"
              initial={{ scale: 0.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 1.5, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="flex flex-col items-center gap-4"
            >
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 0.5 }}
              >
                <Music className="h-24 w-24 text-white" />
              </motion.div>
              <span className="text-5xl font-bold text-white">GO!</span>
            </motion.div>
          )}
        </AnimatePresence>
        
        {/* Get Ready text */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 text-xl text-white/80"
        >
          {count > 0 ? 'Get Ready...' : 'Listen carefully!'}
        </motion.p>
      </div>
    </div>
  );
}
