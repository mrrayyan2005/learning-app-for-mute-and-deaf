import React, { useRef, useEffect, useState, useCallback } from 'react';
import './CameraCapture.css';

const CameraCapture = ({ onCapture, isCapturing, onError }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const captureIntervalRef = useRef(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [cameraError, setCameraError] = useState(null);

  // Initialize camera
  const startCamera = useCallback(async () => {
    try {
      setCameraError(null);
      
      const constraints = {
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user'
        }
      };

      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      streamRef.current = stream;
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        
        // Handle play() promise to avoid "interrupted by new load request" error
        const playPromise = videoRef.current.play();
        if (playPromise !== undefined) {
          playPromise
            .then(() => {
              setIsCameraActive(true);
            })
            .catch((error) => {
              console.log('Auto-play prevented:', error);
              // Auto-play was prevented, but that's okay for our use case
              setIsCameraActive(true);
            });
        } else {
          setIsCameraActive(true);
        }
      }
    } catch (err) {
      console.error('Error accessing camera:', err);
      let errorMessage = 'Camera access denied or not available';
      
      if (err.name === 'NotAllowedError') {
        errorMessage = 'Camera permission denied. Please allow camera access and refresh the page.';
      } else if (err.name === 'NotFoundError') {
        errorMessage = 'No camera found on this device.';
      } else if (err.name === 'NotSupportedError') {
        errorMessage = 'Camera not supported on this browser.';
      }
      
      setCameraError(errorMessage);
      onError && onError(errorMessage);
    }
  }, [onError]);

  // Stop camera
  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setIsCameraActive(false);
  }, []);

  // Capture image from video
  const captureImage = useCallback(() => {
    if (!videoRef.current || !canvasRef.current || !isCameraActive) {
      return null;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw video frame to canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert to base64 for API
    const imageData = canvas.toDataURL('image/jpeg', 0.8);
    return imageData;
  }, [isCameraActive]);

  // Handle continuous capture
  useEffect(() => {
    if (isCapturing && isCameraActive) {
      // Start continuous capture every 1 second for better performance
      captureIntervalRef.current = setInterval(() => {
        const imageData = captureImage();
        if (imageData && onCapture) {
          onCapture(imageData);
        }
      }, 1000);
    } else {
      // Stop continuous capture
      if (captureIntervalRef.current) {
        clearInterval(captureIntervalRef.current);
        captureIntervalRef.current = null;
      }
    }

    return () => {
      if (captureIntervalRef.current) {
        clearInterval(captureIntervalRef.current);
      }
    };
  }, [isCapturing, isCameraActive, captureImage, onCapture]);

  // Initialize camera on component mount
  useEffect(() => {
    startCamera();
    
    return () => {
      stopCamera();
      if (captureIntervalRef.current) {
        clearInterval(captureIntervalRef.current);
      }
    };
  }, [startCamera, stopCamera]);

  // Manual capture button handler
  const handleManualCapture = () => {
    const imageData = captureImage();
    if (imageData && onCapture) {
      onCapture(imageData);
    }
  };

  return (
    <div className="camera-capture">
      <div className="camera-container">
        {/* Video Element */}
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="camera-video"
        />
        
        {/* Hidden Canvas for Capture */}
        <canvas
          ref={canvasRef}
          style={{ display: 'none' }}
        />

        {/* Camera Status Indicators */}
        <div className="camera-status">
          {!isCameraActive && !cameraError && (
            <div className="status-indicator loading">
              <div className="status-icon">📹</div>
              <span>Initializing camera...</span>
            </div>
          )}
          
          {isCameraActive && (
            <div className="status-indicator active">
              <div className="status-icon active-dot"></div>
              <span>Camera Active</span>
            </div>
          )}
          
          {isCapturing && (
            <div className="capture-indicator">
              <div className="capture-pulse"></div>
              <span>Recognizing...</span>
            </div>
          )}
        </div>

        {/* Camera Error */}
        {cameraError && (
          <div className="camera-error">
            <div className="error-content">
              <div className="error-icon">❌</div>
              <h3>Camera Error</h3>
              <p>{cameraError}</p>
              <button 
                className="retry-btn"
                onClick={startCamera}
              >
                Retry Camera Access
              </button>
            </div>
          </div>
        )}

        {/* Camera Controls Overlay */}
        {isCameraActive && (
          <div className="camera-controls-overlay">
            <div className="controls-bottom">
              <button
                className="manual-capture-btn"
                onClick={handleManualCapture}
                disabled={!isCameraActive}
              >
                📸 Capture Now
              </button>
            </div>
          </div>
        )}

        {/* Frame Guide */}
        {isCameraActive && (
          <div className="frame-guide">
            <div className="guide-corners">
              <div className="corner top-left"></div>
              <div className="corner top-right"></div>
              <div className="corner bottom-left"></div>
              <div className="corner bottom-right"></div>
            </div>
            <div className="guide-text">
              Position your hand within the frame
            </div>
          </div>
        )}
      </div>

      {/* Camera Info */}
      <div className="camera-info">
        <div className="info-item">
          <span className="info-label">Status:</span>
          <span className={`info-value ${isCameraActive ? 'active' : 'inactive'}`}>
            {isCameraActive ? 'Active' : 'Inactive'}
          </span>
        </div>
        <div className="info-item">
          <span className="info-label">Recognition:</span>
          <span className={`info-value ${isCapturing ? 'running' : 'stopped'}`}>
            {isCapturing ? 'Running' : 'Stopped'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default CameraCapture;
