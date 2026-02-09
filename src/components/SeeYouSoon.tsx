'use client';

import { Calendar, Heart } from 'lucide-react';

export function SeeYouSoon() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-gradient-to-br from-rose-200 via-red-100 to-pink-200">
      <div className="text-center max-w-4xl relative z-10">
        <div className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-12 md:p-16 border-4 border-red-300 animate-fade-in">
          <div className="inline-flex items-center justify-center w-32 h-32 bg-gradient-to-br from-red-400 via-pink-500 to-rose-500 rounded-full mb-8 shadow-xl animate-pulse-scale">
            <Calendar className="w-16 h-16 text-white" strokeWidth={2.5} />
          </div>

          <h1 className="text-6xl md:text-8xl font-bold mb-6 bg-gradient-to-r from-red-500 via-pink-500 to-rose-500 bg-clip-text text-transparent">
            February 13th
          </h1>

          <div className="mb-8 animate-fade-in-delay">
            <p className="text-4xl md:text-5xl text-red-600 font-semibold mb-4 flex items-center justify-center gap-3">
              <Heart className="w-10 h-10 fill-red-500 text-red-500 animate-heartbeat" />
              See You Soon!
              <Heart className="w-10 h-10 fill-red-500 text-red-500 animate-heartbeat" />
            </p>
            <p className="text-2xl text-pink-600">
              I can't wait for our special day together 💕
            </p>
          </div>

          <div className="flex justify-center items-center gap-6 mb-8">
            <span className="text-5xl animate-bounce">💗</span>
            <span className="text-5xl">💝</span>
            <span className="text-5xl animate-bounce">💖</span>
            <span className="text-5xl">✨</span>
            <span className="text-5xl animate-bounce">❤️</span>
          </div>

          <div className="bg-gradient-to-br from-red-50 to-pink-50 rounded-2xl p-8 border-2 border-red-200 animate-fade-in">
            <p className="text-2xl text-gray-700 mb-4">
              Mark your calendar! 📅
            </p>
            <p className="text-xl text-gray-600 leading-relaxed">
              Get ready for an unforgettable day filled with love, laughter, and beautiful moments together. This is just the beginning of our amazing journey! 💖
            </p>
          </div>

          <div className="mt-10 text-xl text-red-500 font-semibold animate-pulse-gentle">
            ✨ Can't wait to see you ✨
          </div>
        </div>
      </div>
    </div>
  );
}
