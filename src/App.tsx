import { useState } from 'react';
import { LoginPage } from './components/LoginPage';
import { AskPermission } from './components/AskPermission';
import { ValentineQuestion } from './components/ValentineQuestion';
import { Celebration } from './components/Celebration';
import { PhotoBouquet } from './components/PhotoBouquet';
import { FinalSurprise } from './components/FinalSurprise';
import { SeeYouSoon } from './components/SeeYouSoon';
import cuteBearsImage from 'figma:asset/8f666fdd981681a06410827992514812b953070c.png';

export default function App() {
  const [currentTab, setCurrentTab] = useState(0);

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Animated background with cute bears */}
      <div className="fixed inset-0 -z-10 bg-gradient-to-br from-pink-100 via-red-50 to-purple-100">
        {/* Cute bear couples floating in background */}
        <div className="absolute inset-0 overflow-hidden opacity-10">
          {[...Array(6)].map((_, i) => (
            <img
              key={i}
              src={cuteBearsImage}
              alt=""
              className="absolute w-32 h-32 animate-float"
              style={{
                left: `${(i * 20) % 100}%`,
                top: `${(i * 30) % 80}%`,
                animationDelay: `${i * 1.5}s`,
                animationDuration: `${20 + i * 2}s`,
              }}
            />
          ))}
        </div>
      </div>

      {/* Tab content */}
      <div className="relative z-10">
        {currentTab === 0 && <LoginPage onLogin={() => setCurrentTab(1)} />}
        {currentTab === 1 && <AskPermission onNext={() => setCurrentTab(2)} />}
        {currentTab === 2 && <ValentineQuestion onYes={() => setCurrentTab(3)} />}
        {currentTab === 3 && <Celebration onNext={() => setCurrentTab(4)} />}
        {currentTab === 4 && <PhotoBouquet onNext={() => setCurrentTab(5)} />}
        {currentTab === 5 && <FinalSurprise onNext={() => setCurrentTab(6)} />}
        {currentTab === 6 && <SeeYouSoon />}
      </div>
    </div>
  );
}