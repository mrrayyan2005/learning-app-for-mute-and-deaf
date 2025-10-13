import React, { useState } from 'react';
import './App.css';
import HomePage from './components/HomePage';
import LearningInterface from './components/LearningInterface';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [learningMode, setLearningMode] = useState('alphabet');

  const startLearning = (mode) => {
    setLearningMode(mode);
    setCurrentPage('learning');
  };

  const goHome = () => {
    setCurrentPage('home');
  };

  return (
    <div className="App">
      {currentPage === 'home' && (
        <HomePage onStartLearning={startLearning} />
      )}
      {currentPage === 'learning' && (
        <LearningInterface 
          mode={learningMode} 
          onGoHome={goHome}
          onSwitchMode={setLearningMode}
        />
      )}
    </div>
  );
}

export default App;
