'use client';

import { useState } from 'react';
import { Heart, Sparkles } from 'lucide-react';

interface LoginPageProps {
  onLogin: () => void;
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [shake, setShake] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!username.trim() || !password.trim()) {
      setShake(true);
      setTimeout(() => setShake(false), 500);
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('/.netlify/functions/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username.trim(), password }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || 'Login failed');
        setShake(true);
        setTimeout(() => setShake(false), 500);
        setLoading(false);
        return;
      }

      if (data.success) {
        onLogin();
      } else {
        setError(data.message || 'Login failed');
        setShake(true);
        setTimeout(() => setShake(false), 500);
        setLoading(false);
      }
    } catch (err) {
      setError('Network error. Please try again.');
      setShake(true);
      setTimeout(() => setShake(false), 500);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-pink-200 via-rose-100 to-red-100">
      {/* Heart stickers decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
        <div 
          className="absolute top-10 left-10 w-24 h-24 text-5xl animate-float"
        >
          💗
        </div>
        <div 
          className="absolute bottom-10 right-10 w-24 h-24 text-5xl animate-float"
          style={{ animationDelay: '1s' }}
        >
          ❤️
        </div>
      </div>
      
      <div className="relative">
        {/* Decorative stickers */}
        <div className="absolute -top-12 -left-12 text-6xl animate-pulse">
          💕
        </div>
        <div className="absolute -top-8 -right-16 text-5xl">✨</div>
        <div className="absolute -bottom-10 -left-16 text-5xl">💝</div>
        <div className="absolute -bottom-8 -right-12 text-6xl animate-pulse" style={{ animationDelay: '0.5s' }}>
          💖
        </div>
        
        {/* Login card */}
        <div className={`bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-8 w-full max-w-md border-4 border-pink-200 ${shake ? 'animate-shake' : ''}`}>
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-pink-400 to-red-400 rounded-full mb-4 animate-pulse">
              <Heart className="w-10 h-10 text-white fill-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 bg-clip-text text-transparent mb-2">
              Something Special 💌
            </h1>
            <p className="text-pink-600 flex items-center justify-center gap-2">
              <Sparkles className="w-4 h-4" />
              Enter to unlock magic
              <Sparkles className="w-4 h-4" />
            </p>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border-2 border-red-200 rounded-xl text-red-600 text-sm text-center">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-6">
            <div className="relative">
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Your name ✨"
                disabled={loading}
                className="w-full px-6 py-4 rounded-2xl border-2 border-pink-300 focus:border-pink-500 focus:outline-none focus:ring-2 focus:ring-pink-200 bg-pink-50/50 text-gray-800 placeholder-pink-400 disabled:opacity-50 disabled:cursor-not-allowed"
              />
            </div>

            <div className="relative">
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Secret word 🔒"
                disabled={loading}
                className="w-full px-6 py-4 rounded-2xl border-2 border-pink-300 focus:border-pink-500 focus:outline-none focus:ring-2 focus:ring-pink-200 bg-pink-50/50 text-gray-800 placeholder-pink-400 disabled:opacity-50 disabled:cursor-not-allowed"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 text-white rounded-2xl font-semibold hover:shadow-lg hover:scale-105 transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Checking...</span>
                </>
              ) : (
                <>
                  <Heart className="w-5 h-5 fill-white" />
                  Enter the Love Zone
                  <Heart className="w-5 h-5 fill-white" />
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
