'use client';

import { useEffect, useState } from 'react';
import { Sparkles } from 'lucide-react';

interface CelebrationProps {
  onNext: () => void;
}

interface Confetti {
  id: number;
  left: number;
  delay: number;
  duration: number;
  emoji: string;
}

export function Celebration({ onNext }: CelebrationProps) {
  const [confetti, setConfetti] = useState<Confetti[]>([]);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const confettiPieces: Confetti[] = Array.from({ length: 50 }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      delay: Math.random() * 3,
      duration: 3 + Math.random() * 2,
      emoji: ['💖', '💕', '💗', '💓', '💝', '✨', '⭐', '🎉'][Math.floor(Math.random() * 8)],
    }));
    setConfetti(confettiPieces);
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-gradient-to-br from-yellow-200 via-pink-200 to-rose-200">
      {/* Confetti effect */}
      {mounted && (
        <div className="absolute inset-0 pointer-events-none">
          {confetti.map((piece) => (
            <div
              key={piece.id}
              className="absolute animate-confetti"
              style={{
                left: `${piece.left}%`,
                top: `-20px`,
                animationDelay: `${piece.delay}s`,
                animationDuration: `${piece.duration}s`,
              }}
            >
              {piece.emoji}
            </div>
          ))}
        </div>
      )}

      <div className="text-center max-w-4xl relative z-10">
        <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-12 border-4 border-pink-300">
          {/* Celebration with hearts */}
          <div className="mb-8 relative">
            <div className="w-64 h-64 mx-auto bg-gradient-to-br from-pink-200 via-purple-200 to-red-200 rounded-3xl flex items-center justify-center overflow-hidden">
              <span className="text-9xl animate-pulse-scale">💖</span>
            </div>
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className="text-9xl animate-spin-slow">✨</div>
            </div>
          </div>

          <h1 className="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 bg-clip-text text-transparent animate-bounce-gentle">
            Yeeeee You Finally Agreed! 🎊
          </h1>

          <p className="text-3xl text-pink-600 mb-4">
            This makes me so happy! 💕
          </p>

          <div className="flex justify-center gap-3 text-5xl mb-10">
            <span className="animate-bounce">🥳</span>
            <span className="animate-bounce" style={{ animationDelay: '0.1s' }}>💝</span>
            <span className="animate-bounce" style={{ animationDelay: '0.2s' }}>🎉</span>
            <span className="animate-bounce" style={{ animationDelay: '0.3s' }}>💖</span>
            <span className="animate-bounce" style={{ animationDelay: '0.4s' }}>✨</span>
          </div>

          <p className="text-2xl text-pink-500 mb-8">
            I have something special to show you... 🌸
          </p>

          <button
            onClick={onNext}
            className="px-12 py-5 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 text-white text-2xl font-bold rounded-full hover:shadow-2xl hover:scale-110 transition-all duration-300 flex items-center gap-3 mx-auto"
          >
            <Sparkles className="w-6 h-6" />
            Next Surprise
            <Sparkles className="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>
  );
}
