import { Sparkles } from 'lucide-react';
import cuteBearsImage from 'figma:asset/8f666fdd981681a06410827992514812b953070c.png';

interface CelebrationProps {
  onNext: () => void;
}

export function Celebration({ onNext }: CelebrationProps) {
  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-gradient-to-br from-yellow-200 via-pink-200 to-rose-200">
      {/* Confetti effect */}
      <div className="absolute inset-0 pointer-events-none">
        {[...Array(50)].map((_, i) => (
          <div
            key={i}
            className="absolute animate-confetti"
            style={{
              left: `${Math.random() * 100}%`,
              top: `-20px`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${3 + Math.random() * 2}s`,
            }}
          >
            {['💖', '💕', '💗', '💓', '💝', '✨', '⭐', '🎉'][Math.floor(Math.random() * 8)]}
          </div>
        ))}
      </div>

      <div className="text-center max-w-4xl relative z-10">
        <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-12 border-4 border-pink-300">
          {/* Celebration with cute bears */}
          <div className="mb-8 relative">
            <div className="w-64 h-64 mx-auto bg-gradient-to-br from-pink-200 via-purple-200 to-red-200 rounded-3xl flex items-center justify-center overflow-hidden">
              <img src={cuteBearsImage} alt="" className="w-48 h-48 animate-pulse-scale" />
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