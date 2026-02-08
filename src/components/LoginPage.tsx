import { useState } from 'react';
import { Heart, Sparkles } from 'lucide-react';
import cuteBearsImage from 'figma:asset/8f666fdd981681a06410827992514812b953070c.png';

interface LoginPageProps {
  onLogin: () => void;
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [shake, setShake] = useState(false);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (username && password) {
      onLogin();
    } else {
      setShake(true);
      setTimeout(() => setShake(false), 500);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-pink-200 via-rose-100 to-red-100">
      {/* Cute bears decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
        <img 
          src={cuteBearsImage} 
          alt="" 
          className="absolute top-10 left-10 w-24 h-24 animate-float"
        />
        <img 
          src={cuteBearsImage} 
          alt="" 
          className="absolute bottom-10 right-10 w-24 h-24 animate-float"
          style={{ animationDelay: '1s' }}
        />
      </div>
      
      <div className="relative">
        {/* Decorative stickers */}
        <div className="absolute -top-12 -left-12 w-20 h-20">
          <img src={cuteBearsImage} alt="" className="w-full h-full animate-pulse" />
        </div>
        <div className="absolute -top-8 -right-16 text-5xl">✨</div>
        <div className="absolute -bottom-10 -left-16 text-5xl">💝</div>
        <div className="absolute -bottom-8 -right-12 w-20 h-20">
          <img src={cuteBearsImage} alt="" className="w-full h-full animate-pulse" style={{ animationDelay: '0.5s' }} />
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

          <form onSubmit={handleLogin} className="space-y-6">
            <div className="relative">
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Your name ✨"
                className="w-full px-6 py-4 rounded-2xl border-2 border-pink-300 focus:border-pink-500 focus:outline-none focus:ring-2 focus:ring-pink-200 bg-pink-50/50 text-gray-800 placeholder-pink-400"
              />
            </div>

            <div className="relative">
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Secret word 🔒"
                className="w-full px-6 py-4 rounded-2xl border-2 border-pink-300 focus:border-pink-500 focus:outline-none focus:ring-2 focus:ring-pink-200 bg-pink-50/50 text-gray-800 placeholder-pink-400"
              />
            </div>

            <button
              type="submit"
              className="w-full py-4 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 text-white rounded-2xl font-semibold hover:shadow-lg hover:scale-105 transition-all duration-300 flex items-center justify-center gap-2"
            >
              <Heart className="w-5 h-5 fill-white" />
              Enter the Love Zone
              <Heart className="w-5 h-5 fill-white" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}