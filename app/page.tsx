'use client';

import { Suspense } from 'react';
import App from '@/src/App';

function LoadingFallback() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-100 via-red-50 to-purple-100">
      <div className="text-center">
        <div className="text-6xl mb-4 animate-bounce">💖</div>
        <p className="text-2xl text-pink-600">Loading your special moment...</p>
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <Suspense fallback={<LoadingFallback />}>
      <App />
    </Suspense>
  );
}
