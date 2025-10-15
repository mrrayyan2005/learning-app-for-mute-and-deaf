import React, { useState, useEffect, useCallback } from 'react';
import CameraCapture from './CameraCapture';
import './LearningInterface.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5004/api';

const LearningInterface = ({ mode, onGoHome, onSwitchMode }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [isCapturing, setIsCapturing] = useState(false);
  const [captureInterval, setCaptureInterval] = useState(null);
  const [labels, setLabels] = useState([]);

  // Fetch available labels on component mount
  useEffect(() => {
    const fetchLabels = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/labels?type=${mode}`);
        const data = await response.json();
        if (data.status === 'success') {
          setLabels(data.labels);
        }
      } catch (err) {
        console.error('Error fetching labels:', err);
      }
    };

    fetchLabels();
  }, [mode]);

  const sendPredictionRequest = useCallback(async (imageData) => {
    if (!imageData) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          image: imageData,
          type: mode 
        }),
      });

      const data = await response.json();

      if (data.status === 'success') {
        setPrediction({
          letter: data.prediction,
          confidence: data.confidence,
          allPredictions: data.all_predictions
        });
      } else {
        setError(data.message || 'Prediction failed');
      }
    } catch (err) {
      setError('Network error: Could not connect to server');
      console.error('Prediction error:', err);
    } finally {
      setIsLoading(false);
    }
  }, [mode]);

  const startContinuousCapture = useCallback(() => {
    setIsCapturing(true);
    // Start capturing every 500ms for real-time predictions
    const interval = setInterval(() => {
      // This will be called by the CameraCapture component
    }, 500);
    setCaptureInterval(interval);
  }, []);

  const stopContinuousCapture = useCallback(() => {
    setIsCapturing(false);
    if (captureInterval) {
      clearInterval(captureInterval);
      setCaptureInterval(null);
    }
  }, [captureInterval]);

  const handleCapture = useCallback((imageData) => {
    if (imageData && isCapturing) {
      sendPredictionRequest(imageData);
    }
  }, [sendPredictionRequest, isCapturing]);

  const modeConfig = {
    alphabet: {
      title: 'Learn Sign Language Alphabets',
      description: 'Practice sign language letters A through H',
      icon: '🔤',
      color: '#667eea'
    },
    words: {
      title: 'Learn Sign Language Words',
      description: 'Practice common words and greetings',
      icon: '💬',
      color: '#48bb78'
    }
  };

  const currentConfig = modeConfig[mode];

  return (
    <div className="learning-interface">
      {/* Header */}
      <div className="learning-header">
        <div className="header-content">
          <button className="back-btn" onClick={onGoHome}>
            ← Back to Home
          </button>
          <div className="header-info">
            <h1 className="learning-title">
              <span className="title-icon">{currentConfig.icon}</span>
              {currentConfig.title}
            </h1>
            <p className="learning-description">{currentConfig.description}</p>
          </div>
          <div className="mode-switch">
            <button 
              className={`mode-btn ${mode === 'alphabet' ? 'active' : ''}`}
              onClick={() => onSwitchMode('alphabet')}
            >
              🔤 Alphabets
            </button>
            <button 
              className={`mode-btn ${mode === 'words' ? 'active' : ''}`}
              onClick={() => onSwitchMode('words')}
            >
              💬 Words
            </button>
          </div>
        </div>
      </div>

      {/* Main Learning Area */}
      <div className="learning-main">
        {/* Camera Section */}
        <div className="camera-section">
          <CameraCapture 
            onCapture={handleCapture}
            isCapturing={isCapturing}
            onError={setError}
          />
          
          {/* Prediction Overlay */}
          {prediction && (
            <div className="prediction-overlay">
              <div className="prediction-result">
                <div className="predicted-sign">{prediction.letter}</div>
                <div className="confidence-score">
                  {prediction.confidence.toFixed(1)}% confident
                </div>
              </div>
            </div>
          )}

          {/* Loading Indicator */}
          {isLoading && (
            <div className="loading-overlay">
              <div className="loading-spinner"></div>
            </div>
          )}
        </div>

        {/* Controls Section */}
        <div className="controls-section">
          <div className="capture-controls">
            <h3>Camera Controls</h3>
            <div className="control-buttons">
              {!isCapturing ? (
                <button 
                  className="control-btn start-btn"
                  onClick={startContinuousCapture}
                >
                  🎯 Start Recognition
                </button>
              ) : (
                <button 
                  className="control-btn stop-btn"
                  onClick={stopContinuousCapture}
                >
                  ⏹️ Stop Recognition
                </button>
              )}
            </div>
            
            {error && (
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                {error}
              </div>
            )}
          </div>

          {/* Learning Guide */}
          <div className="learning-guide">
            <h3>Available Signs</h3>
            <div className="labels-grid">
              {labels.map((label, index) => (
                <div 
                  key={index} 
                  className={`label-badge ${prediction?.letter === label ? 'active' : ''}`}
                >
                  {label}
                </div>
              ))}
            </div>
          </div>

          {/* Prediction Details */}
          {prediction && prediction.allPredictions && (
            <div className="prediction-details">
              <h3>All Predictions</h3>
              <div className="predictions-list">
                {Object.entries(prediction.allPredictions)
                  .sort(([,a], [,b]) => b - a)
                  .slice(0, 5)
                  .map(([label, confidence]) => (
                    <div key={label} className="prediction-item">
                      <span className="prediction-label">{label}</span>
                      <div className="confidence-bar">
                        <div 
                          className="confidence-fill"
                          style={{ width: `${confidence}%` }}
                        ></div>
                      </div>
                      <span className="prediction-percentage">
                        {confidence.toFixed(1)}%
                      </span>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Instructions */}
      <div className="instructions-section">
        <div className="instructions">
          <h3>📋 Instructions</h3>
          <ol>
            <li>Click "Start Recognition" to begin</li>
            <li>Position your hand clearly in front of the camera</li>
            <li>Make the sign gesture you want to practice</li>
            <li>Watch the real-time predictions and confidence scores</li>
            <li>Practice until you achieve high confidence scores!</li>
          </ol>
        </div>
      </div>
    </div>
  );
};

export default LearningInterface;
