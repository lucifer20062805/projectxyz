import { useState, useRef } from 'react';
import { Heart } from 'lucide-react';
import cuteBearsImage from 'figma:asset/8f666fdd981681a06410827992514812b953070c.png';

interface ValentineQuestionProps {
  onYes: () => void;
}

export function ValentineQuestion({ onYes }: ValentineQuestionProps) {
  const [noPosition, setNoPosition] = useState({ x: 0, y: 0 });
  const [yesSize, setYesSize] = useState(1);
  const [noClicks, setNoClicks] = useState(0);
  const noButtonRef = useRef<HTMLButtonElement>(null);

  const handleNoHover = () => {
    // Generate random position within viewport bounds
    const maxX = window.innerWidth - 300;
    const maxY = window.innerHeight - 200;
    const newX = (Math.random() - 0.5) * maxX;
    const newY = (Math.random() - 0.5) * maxY;
    
    setNoPosition({ x: newX, y: newY });
    setYesSize(prev => Math.min(prev + 0.15, 2.5));
    setNoClicks(prev => prev + 1);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 overflow-hidden bg-gradient-to-br from-red-200 via-pink-100 to-orange-100">
      {/* Cute bears decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-15">
        {[...Array(4)].map((_, i) => (
          <img
            key={i}
            src={cuteBearsImage}
            alt=""
            className="absolute w-28 h-28 animate-float"
            style={{
              left: `${(i * 25) % 100}%`,
              top: `${(i * 30) % 80}%`,
              animationDelay: `${i * 1.5}s`,
            }}
          />
        ))}
      </div>
      
      <div className="text-center max-w-3xl relative z-10">
        {/* Decorative hearts */}
        <div className="absolute -top-20 left-1/2 -translate-x-1/2 flex gap-4">
          <img src={cuteBearsImage} alt="" className="w-16 h-16" />
          <span className="text-6xl">❤️</span>
          <img src={cuteBearsImage} alt="" className="w-16 h-16" />
        </div>

        {/* Main card */}
        <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-12 border-4 border-pink-300 relative z-10">
          <div className="mb-8">
            <div className="inline-flex items-center justify-center w-32 h-32 bg-gradient-to-br from-pink-400 via-red-500 to-purple-500 rounded-full mb-6 animate-pulse-scale">
              <Heart className="w-16 h-16 text-white fill-white animate-heartbeat" />
            </div>
          </div>

          <h1 className="text-6xl md:text-7xl font-bold mb-8 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 bg-clip-text text-transparent">
            Will You Be My Valentine? 💝
          </h1>

          <p className="text-2xl text-pink-600 mb-12">
            Please say yes... 🥺💕
          </p>

          {/* Buttons */}
          <div className="flex flex-col items-center gap-6 relative min-h-[200px]">
            <button
              onClick={onYes}
              style={{ 
                transform: `scale(${yesSize})`,
                transition: 'transform 0.3s ease'
              }}
              className="px-16 py-6 bg-gradient-to-r from-green-400 to-emerald-500 text-white text-3xl font-bold rounded-full hover:shadow-2xl hover:scale-110 transition-all duration-300 z-20 relative"
            >
              YES! 💚✨
            </button>

            <button
              ref={noButtonRef}
              onMouseEnter={handleNoHover}
              onClick={handleNoHover}
              onTouchStart={handleNoHover}
              style={{
                transform: `translate(${noPosition.x}px, ${noPosition.y}px)`,
                transition: 'transform 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55)',
                position: 'fixed',
                left: '50%',
                top: '60%',
                marginLeft: '-80px',
              }}
              className="px-12 py-4 bg-gradient-to-r from-gray-400 to-gray-500 text-white text-xl font-bold rounded-full hover:shadow-lg cursor-pointer"
            >
              No 😢
            </button>
          </div>

          {noClicks > 0 && (
            <p className="mt-8 text-pink-500 animate-bounce">
              {noClicks < 3 && "Come on... give me a chance! 💕"}
              {noClicks >= 3 && noClicks < 6 && "Please? I promise to make you happy! 🥺"}
              {noClicks >= 6 && noClicks < 10 && "You can't catch the NO button! Just say YES! 💝"}
              {noClicks >= 10 && "The YES button is getting bigger for a reason! 😊💖"}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}