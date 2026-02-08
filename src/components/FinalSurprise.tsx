import { useState } from 'react';
import { motion } from 'motion/react';
import cuteBearsImage from 'figma:asset/8f666fdd981681a06410827992514812b953070c.png';

interface FinalSurpriseProps {
  onNext: () => void;
}

export function FinalSurprise({ onNext }: FinalSurpriseProps) {
  const [envelopeOpen, setEnvelopeOpen] = useState(false);

  const letterText = `My Dearest Valentine,

From the moment I met you, my world became brighter and more beautiful. Every smile you share lights up my heart, and every laugh we share together creates memories I treasure forever.

You are the most amazing person I know. Your kindness, your warmth, your incredible spirit - they all make me fall for you more and more each day. When I'm with you, everything feels right, like all the pieces of my life have finally fallen into place.

I love the way you make ordinary moments extraordinary. Whether we're having deep conversations or just enjoying comfortable silence, every second with you is precious. You understand me in ways I never thought possible, and you accept me for who I am.

This Valentine's Day, I want you to know that you mean the world to me. You're not just my Valentine - you're my best friend, my confidant, my happy place. I can't wait to create more beautiful memories with you, to laugh together, to grow together, and to continue this wonderful journey side by side.

Thank you for saying yes. Thank you for being you. Thank you for making my heart so incredibly happy.

Forever yours,
With all my love 💕`;

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-gradient-to-br from-indigo-200 via-purple-100 to-pink-200">
      {/* Floating cute bears background */}
      <div className="absolute inset-0 pointer-events-none opacity-10">
        {[...Array(8)].map((_, i) => (
          <motion.img
            key={i}
            src={cuteBearsImage}
            alt=""
            className="absolute w-24 h-24"
            initial={{ 
              x: Math.random() * window.innerWidth,
              y: window.innerHeight + 50,
            }}
            animate={{
              y: -100,
              x: Math.random() * window.innerWidth,
            }}
            transition={{
              duration: 8 + Math.random() * 4,
              repeat: Infinity,
              delay: Math.random() * 5,
              ease: "linear",
            }}
          />
        ))}
      </div>

      <div className="text-center max-w-4xl relative z-10">
        {!envelopeOpen ? (
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="text-5xl md:text-6xl font-bold mb-12 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 bg-clip-text text-transparent">
              Your Final Surprise 💌
            </h1>

            {/* Envelope */}
            <motion.div
              className="relative mx-auto cursor-pointer"
              style={{ width: '300px', height: '200px' }}
              onClick={() => setEnvelopeOpen(true)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {/* Envelope body */}
              <div className="absolute inset-0 bg-gradient-to-br from-red-400 to-pink-500 rounded-lg shadow-2xl">
                {/* Envelope flap */}
                <motion.div
                  className="absolute -top-1 left-0 right-0 h-24 bg-gradient-to-br from-red-500 to-pink-600 origin-top"
                  style={{
                    clipPath: 'polygon(0 0, 50% 60%, 100% 0)',
                  }}
                  animate={{
                    rotateX: 0,
                  }}
                />
                
                {/* Heart seal */}
                <div className="absolute top-12 left-1/2 -translate-x-1/2 w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-lg z-10">
                  <span className="text-3xl">💝</span>
                </div>

                {/* Envelope lines */}
                <div className="absolute bottom-12 left-8 right-8 space-y-2">
                  <div className="h-1 bg-red-300 rounded opacity-50"></div>
                  <div className="h-1 bg-red-300 rounded opacity-50 w-3/4"></div>
                </div>
              </div>

              {/* Sparkles around envelope */}
              {[...Array(8)].map((_, i) => (
                <motion.div
                  key={i}
                  className="absolute text-2xl"
                  style={{
                    top: '50%',
                    left: '50%',
                  }}
                  animate={{
                    x: Math.cos(i * Math.PI / 4) * 120,
                    y: Math.sin(i * Math.PI / 4) * 120,
                    opacity: [0.3, 1, 0.3],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    delay: i * 0.2,
                  }}
                >
                  ✨
                </motion.div>
              ))}
            </motion.div>

            <p className="mt-12 text-2xl text-pink-600 animate-pulse">
              Click the envelope to open your letter 💕
            </p>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="bg-white/95 backdrop-blur-sm rounded-3xl shadow-2xl p-8 md:p-12 border-4 border-pink-200 max-w-3xl mx-auto"
          >
            <div className="mb-6">
              <div className="text-6xl mb-4">💌</div>
              <h2 className="text-4xl font-bold bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 bg-clip-text text-transparent mb-2">
                A Letter From My Heart
              </h2>
            </div>

            <div className="max-h-96 overflow-y-auto pr-4 custom-scrollbar">
              <div className="text-left space-y-4 text-gray-700 leading-relaxed">
                {letterText.split('\n\n').map((paragraph, index) => (
                  <motion.p
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: index * 0.2 }}
                    className="text-lg"
                  >
                    {paragraph}
                  </motion.p>
                ))}
              </div>
            </div>

            <div className="mt-8 flex justify-center gap-2 text-3xl">
              {[...Array(7)].map((_, i) => (
                <motion.span
                  key={i}
                  animate={{
                    scale: [1, 1.2, 1],
                    opacity: [0.5, 1, 0.5],
                  }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    delay: i * 0.2,
                  }}
                >
                  💖
                </motion.span>
              ))}
            </div>

            <button
              onClick={onNext}
              className="mt-8 px-10 py-4 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 text-white text-xl font-bold rounded-full hover:shadow-2xl hover:scale-110 transition-all duration-300"
            >
              Continue... 💕
            </button>
          </motion.div>
        )}
      </div>
    </div>
  );
}