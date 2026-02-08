import { Heart } from 'lucide-react';
import cuteBearsImage from '../assets/8f666fdd981681a06410827992514812b953070c.png';

interface AskPermissionProps {
  onNext: () => void;
}

export function AskPermission({ onNext }: AskPermissionProps) {
  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-purple-200 via-pink-100 to-fuchsia-100">
      {/* Cute bears decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-15">
        <img 
          src={cuteBearsImage} 
          alt="" 
          className="absolute top-20 right-20 w-32 h-32 animate-float"
        />
        <img 
          src={cuteBearsImage} 
          alt="" 
          className="absolute bottom-20 left-20 w-32 h-32 animate-float"
          style={{ animationDelay: '2s' }}
        />
      </div>
      
      <div className="text-center max-w-2xl relative z-10">
        {/* Floating decoration */}
        <div className="mb-8 flex justify-center gap-4">
          <img src={cuteBearsImage} alt="" className="w-20 h-20 animate-float" />
          <span className="text-6xl animate-float" style={{ animationDelay: '0.5s' }}>💖</span>
          <img src={cuteBearsImage} alt="" className="w-20 h-20 animate-float" style={{ animationDelay: '1s' }} />
        </div>

        {/* Main content */}
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-2xl p-12 border-4 border-pink-300">
          <div className="mb-8">
            <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-pink-400 to-red-500 rounded-full mb-6 animate-pulse-scale">
              <Heart className="w-12 h-12 text-white fill-white" />
            </div>
          </div>

          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 bg-clip-text text-transparent animate-fade-in">
            I Wanna Ask You Something...
          </h1>

          <p className="text-2xl text-pink-600 mb-8 animate-fade-in-delay">
            Something really important 💕
          </p>

          <div className="flex justify-center gap-3 text-4xl mb-10">
            <span className="animate-wiggle">😊</span>
            <span className="animate-wiggle" style={{ animationDelay: '0.2s' }}>💗</span>
            <span className="animate-wiggle" style={{ animationDelay: '0.4s' }}>✨</span>
          </div>

          <button
            onClick={onNext}
            className="px-12 py-5 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 text-white text-2xl font-bold rounded-full hover:shadow-2xl hover:scale-110 transition-all duration-300 animate-bounce-gentle"
          >
            ASK!!! 💌
          </button>
        </div>
      </div>
    </div>
  );
}
