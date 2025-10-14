from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import base64
import io
import cv2
import numpy as np
from PIL import Image
import math
import os

# Import your proven approach
try:
    from cvzone.HandTrackingModule import HandDetector
    from cvzone.ClassificationModule import Classifier
    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False

app = Flask(__name__)
CORS(app)

# Initialize your proven approach (if dependencies available)
if DEPS_AVAILABLE:
    detector = HandDetector(maxHands=1)
    
    # Try to load models (check if they exist)
    try:
        alphabet_classifier = Classifier("model1/keras_model.h5", "model1/labels.txt")
        words_classifier = Classifier("Model2/keras_model.h5", "Model2/labels.txt")
        MODELS_LOADED = True
    except:
        MODELS_LOADED = False
else:
    MODELS_LOADED = False

# Your exact settings
offset = 20
imgSize = 300
alphabet_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
words_labels = ["Bye", "Hello", "No", "Perfect", "Thank You", "Yes"]

def process_image_like_your_code(cv_image, classifier, labels):
    """Process image exactly like your working testing code"""
    if not DEPS_AVAILABLE or not MODELS_LOADED:
        return "Dependencies not available", 0, False
        
    try:
        # Use YOUR proven hand detection approach
        hands, img = detector.findHands(cv_image)
        
        if hands:  # ONLY predict when hands are actually detected!
            # Your exact processing logic
            hand = hands[0]
            x, y, w, h = hand['bbox']
            
            # Create white background like your code
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            
            # Crop hand region like your code
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
            
            # Handle aspect ratio exactly like your code
            aspectRatio = h / w
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
            
            # Make prediction exactly like your code
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            
            # Get confidence
            if hasattr(prediction, '__len__'):
                confidence = float(np.max(prediction)) * 100
            else:
                confidence = float(prediction) * 100
            
            # Get label
            if 0 <= index < len(labels):
                predicted_label = labels[index]
            else:
                predicted_label = "Unknown"
                confidence = 0
            
            return predicted_label, confidence, True
        
        else:
            return "No gesture detected", 0, False
            
    except Exception as e:
        return "Error", 0, False

def preprocess_image(image_data):
    """Convert base64 to CV2 image"""
    try:
        # Decode base64 image
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Convert to PIL Image
        pil_image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to OpenCV format
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        return cv_image
        
    except Exception as e:
        return None

def handler(request):
    if request.method == 'OPTIONS':
        return '', 200
        
    if request.method != 'POST':
        return jsonify({"status": "error", "message": "Method not allowed"}), 405
    
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data"}), 400
            
        image_data = data.get('image')
        prediction_type = data.get('type', 'words')  # words or alphabet
        
        if not image_data:
            return jsonify({"status": "error", "message": "No image data"}), 400
        
        if not DEPS_AVAILABLE:
            return jsonify({
                "status": "error", 
                "message": "ML dependencies not available in serverless environment"
            }), 500
            
        if not MODELS_LOADED:
            return jsonify({
                "status": "error", 
                "message": "Models not loaded - check model files"
            }), 500
        
        # Convert image
        cv_image = preprocess_image(image_data)
        if cv_image is None:
            return jsonify({"status": "error", "message": "Image processing failed"}), 400
        
        # Process using YOUR proven approach
        if prediction_type == 'alphabet':
            predicted_result, confidence, has_hands = process_image_like_your_code(
                cv_image, alphabet_classifier, alphabet_labels)
        else:
            predicted_result, confidence, has_hands = process_image_like_your_code(
                cv_image, words_classifier, words_labels)
        
        if not has_hands:
            return jsonify({
                "status": "no_hands",
                "prediction": predicted_result,
                "confidence": confidence,
                "message": "No hands detected by HandDetector"
            }), 200
        
        return jsonify({
            "status": "success",
            "prediction": predicted_result,
            "confidence": round(confidence, 2)
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
