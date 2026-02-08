import { useState, useEffect } from 'react';
import { Heart, Sparkles, Loader2 } from 'lucide-react';
import cuteBearsImage from 'figma:asset/8f666fdd981681a06410827992514812b953070c.png';

interface LoginPageProps {
  onLogin: () => void;
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [shake, setShake] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [isSignup, setIsSignup] = useState(false);
  const [checkingSession, setCheckingSession] = useState(true);

  // Check for existing session on mount
  useEffect(() => {
    fetch('/api/me', { credentials: 'include' })
      .then((res) => {
        if (res.ok) {
          onLogin();
        }
      })
      .catch(() => {})
      .finally(() => setCheckingSession(false));
  }, [onLogin]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setShake(true);
      setTimeout(() => setShake(false), 500);
      return;
    }

    setLoading(true);

    try {
      const endpoint = isSignup ? '/api/register' : '/api/login';
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || 'Something went wrong');
        setShake(true);
        setTimeout(() => setShake(false), 500);
        return;
      }

      onLogin();
    } catch {
      setError('Could not connect to server');
      setShake(true);
      setTimeout(() => setShake(false), 500);
    } finally {
      setLoading(false);
    }
  };

  if (checkingSession) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-200 via-rose-100 to-red-100">
        <Loader2 className="w-10 h-10 text-pink-500 animate-spin" />
      </div>
    );
  }

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
        <div className="absolute -top-8 -right-16 text-5xl">{"✨"}</div>
        <div className="absolute -bottom-10 -left-16 text-5xl">{"💝"}</div>
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
              {'Something Special 💌'}
            </h1>
            <p className="text-pink-600 flex items-center justify-center gap-2">
              <Sparkles className="w-4 h-4" />
              {isSignup ? 'Create your magical account' : 'Enter to unlock magic'}
              <Sparkles className="w-4 h-4" />
            </p>
          </div>

          {error && (
            <div className="mb-4 p-3 rounded-2xl bg-red-50 border border-red-200 text-red-600 text-sm text-center">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="relative">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Your email ✨"
                className="w-full px-6 py-4 rounded-2xl border-2 border-pink-300 focus:border-pink-500 focus:outline-none focus:ring-2 focus:ring-pink-200 bg-pink-50/50 text-gray-800 placeholder-pink-400"
                disabled={loading}
              />
            </div>

            <div className="relative">
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Secret word 🔒"
                className="w-full px-6 py-4 rounded-2xl border-2 border-pink-300 focus:border-pink-500 focus:outline-none focus:ring-2 focus:ring-pink-200 bg-pink-50/50 text-gray-800 placeholder-pink-400"
                disabled={loading}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 bg-gradient-to-r from-pink-500 via-red-500 to-purple-500 text-white rounded-2xl font-semibold hover:shadow-lg hover:scale-105 transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-70 disabled:hover:scale-100"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <>
                  <Heart className="w-5 h-5 fill-white" />
                  {isSignup ? 'Create Account' : 'Enter the Love Zone'}
                  <Heart className="w-5 h-5 fill-white" />
                </>
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <button
              type="button"
              onClick={() => {
                setIsSignup(!isSignup);
                setError('');
              }}
              className="text-pink-500 hover:text-pink-700 text-sm font-medium transition-colors"
            >
              {isSignup
                ? 'Already have an account? Sign in'
                : "Don't have an account? Sign up"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
