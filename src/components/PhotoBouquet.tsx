'use client';

import { useState } from 'react';
import { X } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface PhotoBouquetProps {
  onNext: () => void;
}

interface Photo {
  id: number;
  text: string;
}

export function PhotoBouquet({ onNext }: PhotoBouquetProps) {
  const [selectedPhoto, setSelectedPhoto] = useState<number | null>(null);
  const [flipped, setFlipped] = useState(false);

  const photos: Photo[] = [
    { id: 1, text: "Your smile brightens my darkest days 🌟" },
    { id: 2, text: "Every moment with you is a treasure 💎" },
    { id: 3, text: "You make my heart skip a beat 💓" },
    { id: 4, text: "Your laugh is my favorite sound 🎵" },
    { id: 5, text: "With you, every day feels like magic ✨" },
  ];

  const handlePhotoClick = (id: number) => {
    setSelectedPhoto(id);
    setFlipped(false);
  };

  const handleFlip = () => {
    setFlipped(!flipped);
  };

  const handleClose = () => {
    setSelectedPhoto(null);
    setFlipped(false);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 py-12 bg-gradient-to-br from-green-100 via-teal-50 to-cyan-100">
      {/* Heart stickers decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-15">
        {[...Array(5)].map((_, i) => (
          <div
            key={i}
            className="absolute text-5xl animate-float"
            style={{
              left: `${(i * 22) % 100}%`,
              top: `${(i * 25) % 80}%`,
              animationDelay: `${i * 1.2}s`,
            }}
          >
            {'💗❤️💕💖💓'[i]}
          </div>
        ))}
      </div>
      
      <div className="text-center mb-8 relative z-10">
        <h1 className="text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 bg-clip-text text-transparent">
          A Bouquet of Memories 💐
        </h1>
        <p className="text-2xl text-pink-600">
          Click on each flower to see a special moment ✨
        </p>
      </div>

      {/* Bouquet display */}
      <div className="relative w-full max-w-4xl mb-12">
        <div className="flex flex-wrap justify-center items-end gap-6 relative">
          {photos.map((photo, index) => (
            <div
              key={photo.id}
              onClick={() => handlePhotoClick(photo.id)}
              className="cursor-pointer transform hover:scale-110 transition-all duration-300 relative"
              style={{
                transform: `rotate(${(index - 2) * 8}deg)`,
                zIndex: selectedPhoto === photo.id ? 50 : 10,
              }}
            >
              {/* Flower stem */}
              <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-2 h-32 bg-gradient-to-b from-green-600 to-green-700 -z-10"></div>
              
              {/* Flower/Photo */}
              <div className="w-32 h-32 rounded-full border-8 border-pink-400 bg-white shadow-xl flex items-center justify-center overflow-hidden hover:border-pink-500 hover:shadow-2xl transition-all">
                <ImageWithFallback
                  src={`/memories/memory${photo.id}.jpg`}
                  alt={`Memory ${photo.id}`}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Flower petals decoration */}
              <div className="absolute -inset-2 pointer-events-none">
                {[...Array(8)].map((_, i) => (
                  <div
                    key={i}
                    className="absolute w-8 h-8 bg-pink-300 rounded-full"
                    style={{
                      top: '50%',
                      left: '50%',
                      transform: `rotate(${i * 45}deg) translateY(-50px)`,
                      opacity: 0.6,
                    }}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Vase */}
        <div className="mt-8 mx-auto w-48 h-24 bg-gradient-to-b from-purple-300 to-purple-400 rounded-b-full border-4 border-purple-500 flex items-center justify-center">
          <span className="text-2xl">💕</span>
        </div>
      </div>

      {/* Photo modal */}
      {selectedPhoto && (
        <div 
          className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
          onClick={handleClose}
        >
          <div 
            className="relative perspective-1000"
            onClick={(e) => e.stopPropagation()}
          >
            <div
              className={`relative w-80 h-96 transition-transform duration-700 transform-style-3d ${
                flipped ? 'rotate-y-180' : ''
              }`}
              onClick={handleFlip}
              style={{ transformStyle: 'preserve-3d' }}
            >
              {/* Front of photo */}
              <div
                className="absolute inset-0 backface-hidden"
                style={{ backfaceVisibility: 'hidden' }}
              >
                <div className="bg-white rounded-2xl shadow-2xl p-4 h-full border-8 border-pink-200">
                  <div className="w-full h-full rounded-lg overflow-hidden">
                    <ImageWithFallback
                      src={`/memories/memory${selectedPhoto}.jpg`}
                      alt={`Memory ${selectedPhoto}`}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <p className="text-center mt-2 text-pink-600 text-sm">Click to flip 💕</p>
                </div>
              </div>

              {/* Back of photo */}
              <div
                className="absolute inset-0 backface-hidden rotate-y-180"
                style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}
              >
                <div className="bg-gradient-to-br from-pink-100 to-purple-100 rounded-2xl shadow-2xl p-8 h-full flex items-center justify-center border-8 border-pink-200">
                  <div className="text-center">
                    <p className="text-2xl text-pink-700 font-semibold mb-4">
                      {photos.find(p => p.id === selectedPhoto)?.text}
                    </p>
                    <p className="text-pink-500 text-sm">Click to flip back 💝</p>
                  </div>
                </div>
              </div>
            </div>

            <button
              onClick={handleClose}
              className="absolute -top-4 -right-4 bg-pink-500 text-white rounded-full p-2 hover:bg-pink-600 transition-colors shadow-lg z-10"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>
      )}

      {/* Next button */}
      <button
        onClick={onNext}
        className="px-12 py-5 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 text-white text-2xl font-bold rounded-full hover:shadow-2xl hover:scale-110 transition-all duration-300 animate-pulse-gentle"
      >
        Ready for the FINAL SURPRISE!!!! 🎁✨
      </button>
    </div>
  );
}
