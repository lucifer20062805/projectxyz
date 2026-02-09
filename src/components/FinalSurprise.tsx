'use client';

import { useState } from 'react';

interface FinalSurpriseProps {
  onNext: () => void;
}

export function FinalSurprise({ onNext }: FinalSurpriseProps) {
  const [envelopeOpen, setEnvelopeOpen] = useState(false);

  const letterText = `Hello Harshika,

The moment I saw you at the club , i was like "Damnn , she is so gorgeous". At first ,i was so jealous that you were talking to Shivang and was not even looking at me both in club or at Rock Beach. But when we got the chance to talk at Auroville Beach , I was sooooo happyyyy that you were interested me tooo...then the drinks we shared , the moments we had , the sunrise we get to see together was all so much dreamy and special for me that I can't even put that feeling in words.

I feel veryyy veryyyy happyyyy and emotionally comfortable with you. I really don't know that you like me or are you even a bit interested in talking to me but i know one thing for sure that i like you and I really wanna know more about you !!!

I am not proposing...ik we need more time to know each other and I will definitely be interested in that...only if you want to then.

I just wanna ask you that ,Will you be my Valentine, Harshika!!!???

Hope that the answer will be yes 👀👀

Forever yours,
With all my love 💕`;

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-gradient-to-br from-indigo-200 via-purple-100 to-pink-200">
      <div className="text-center max-w-4xl relative z-10">
        {!envelopeOpen ? (
          <div className="animate-fade-in">
            <h1 className="text-5xl md:text-6xl font-bold mb-12 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 bg-clip-text text-transparent">
              Your Final Surprise 💌
            </h1>

            <div
              className="relative mx-auto cursor-pointer hover:scale-105 transition-transform duration-300"
              style={{ width: '300px', height: '200px' }}
              onClick={() => setEnvelopeOpen(true)}
            >
              <div className="absolute inset-0 bg-gradient-to-br from-red-400 to-pink-500 rounded-lg shadow-2xl">
                <div
                  className="absolute -top-1 left-0 right-0 h-24 bg-gradient-to-br from-red-500 to-pink-600 origin-top"
                  style={{ clipPath: 'polygon(0 0, 50% 60%, 100% 0)' }}
                />

                <div className="absolute top-12 left-1/2 -translate-x-1/2 w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-lg z-10">
                  <span className="text-3xl">💝</span>
                </div>

                <div className="absolute bottom-12 left-8 right-8 space-y-2">
                  <div className="h-1 bg-red-300 rounded opacity-50" />
                  <div className="h-1 bg-red-300 rounded opacity-50 w-3/4" />
                </div>
              </div>

              <div className="absolute inset-0 pointer-events-none">
                <span className="absolute text-2xl left-4 top-4 animate-pulse">✨</span>
                <span className="absolute text-2xl right-6 top-6 animate-pulse">✨</span>
                <span className="absolute text-2xl left-10 bottom-6 animate-pulse">✨</span>
                <span className="absolute text-2xl right-8 bottom-4 animate-pulse">✨</span>
              </div>
            </div>

            <p className="mt-12 text-2xl text-pink-600 animate-pulse">
              Click the envelope to open your letter 💕
            </p>
          </div>
        ) : (
          <div className="bg-white/95 backdrop-blur-sm rounded-3xl shadow-2xl p-8 md:p-12 border-4 border-pink-200 max-w-3xl mx-auto animate-fade-in">
            <div className="mb-6">
              <div className="text-6xl mb-4">💌</div>
              <h2 className="text-4xl font-bold bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 bg-clip-text text-transparent mb-2">
                A Letter From My Heart
              </h2>
            </div>

            <div className="max-h-96 overflow-y-auto pr-4 custom-scrollbar">
              <div className="text-left space-y-4 text-gray-700 leading-relaxed">
                {letterText.split('\\n\\n').map((paragraph, index) => (
                  <p key={index} className="text-lg animate-fade-in-delay">
                    {paragraph}
                  </p>
                ))}
              </div>
            </div>

            <div className="mt-8 flex justify-center gap-2 text-3xl">
              {[...Array(7)].map((_, i) => (
                <span key={i} className="animate-pulse-gentle">
                  💖
                </span>
              ))}
            </div>

            <button
              onClick={onNext}
              className="mt-8 px-10 py-4 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 text-white text-xl font-bold rounded-full hover:shadow-2xl hover:scale-110 transition-all duration-300"
            >
              Continue... 💕
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

