'use client';

import { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import { Calendar, Heart, Sparkles } from 'lucide-react';

export function SeeYouSoon() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-gradient-to-br from-rose-200 via-red-100 to-pink-200">
      {/* Floating hearts background */}
      {mounted && (
        <div className="absolute inset-0 pointer-events-none opacity-15">
          {[...Array(6)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute text-6xl"
              initial={{ 
                x: (i * 20) % 100 + '%',
                y: window.innerHeight + 50,
              }}
              animate={{
                y: -100,
                rotate: 360,
              }}
              transition={{
                duration: 10 + Math.random() * 5,
                repeat: Infinity,
                delay: Math.random() * 5,
                ease: "linear",
              }}
            >
              {'💗❤️💕💖💓💞'[i]}
            </motion.div>
          ))}
        </div>
      )}

      <div className="text-center max-w-4xl relative z-10">
        <motion.div
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.8, ease: "backOut" }}
          className="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-12 md:p-16 border-4 border-red-300"
        >
          {/* Calendar Icon */}
          <motion.div
            className="inline-flex items-center justify-center w-32 h-32 bg-gradient-to-br from-red-400 via-pink-500 to-rose-500 rounded-full mb-8 shadow-xl"
            animate={{
              scale: [1, 1.1, 1],
              rotate: [0, 5, -5, 0],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          >
            <Calendar className="w-16 h-16 text-white" strokeWidth={2.5} />
          </motion.div>

          {/* Main heading */}
          <motion.h1
            className="text-6xl md:text-8xl font-bold mb-6 bg-gradient-to-r from-red-500 via-pink-500 to-rose-500 bg-clip-text text-transparent"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.6 }}
          >
            February 13th
          </motion.h1>

          {/* Subheading */}
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.6 }}
            className="mb-8"
          >
            <p className="text-4xl md:text-5xl text-red-600 font-semibold mb-4 flex items-center justify-center gap-3">
              <Heart className="w-10 h-10 fill-red-500 text-red-500 animate-heartbeat" />
              See You Soon!
              <Heart className="w-10 h-10 fill-red-500 text-red-500 animate-heartbeat" />
            </p>
            <p className="text-2xl text-pink-600">
              I can't wait for our special day together 💕
            </p>
          </motion.div>

          {/* Decorative elements */}
          <motion.div
            className="flex justify-center items-center gap-6 mb-8"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.8, duration: 0.5, type: "spring" }}
          >
            <motion.span
              className="text-5xl"
              animate={{
                y: [0, -15, 0],
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            >
              💗
            </motion.span>
            <span className="text-5xl">💝</span>
            <motion.span
              className="text-5xl"
              animate={{
                y: [0, -15, 0],
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                delay: 0.3,
                ease: "easeInOut",
              }}
            >
              💖
            </motion.span>
            <span className="text-5xl">✨</span>
            <motion.span
              className="text-5xl"
              animate={{
                y: [0, -15, 0],
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                delay: 0.6,
                ease: "easeInOut",
              }}
            >
              ❤️
            </motion.span>
          </motion.div>

          {/* Message box */}
          <motion.div
            className="bg-gradient-to-br from-red-50 to-pink-50 rounded-2xl p-8 border-2 border-red-200"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1, duration: 0.6 }}
          >
            <p className="text-2xl text-gray-700 mb-4">
              Mark your calendar! 📅
            </p>
            <p className="text-xl text-gray-600 leading-relaxed">
              Get ready for an unforgettable day filled with love, laughter, and beautiful moments together. This is just the beginning of our amazing journey! 💖
            </p>
          </motion.div>

          {/* Countdown-style decoration */}
          <motion.div
            className="mt-10 text-xl text-red-500 font-semibold"
            animate={{
              opacity: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          >
            ✨ Can't wait to see you ✨
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
