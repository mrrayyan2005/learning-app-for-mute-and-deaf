from flask import Flask, request, jsonify
from flask_cors import CORS
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import cv2
import numpy as np
import base64
import io
from PIL import Image
import math
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize exactly like your working code
detector = HandDetector(maxHands=1)
alphabet_classifier = Classifier("model1/keras_model.h5", "model1/labels.txt")
words_classifier = Classifier("Model2/keras_model.h5", "Model2/labels.txt")

# Exact same settings as your working code
offset = 20
imgSize = 300
alphabet_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
words_labels = ["Bye", "Hello", "No", "Perfect", "Thank You", "Yes"]

def process_image_like_your_code(cv_image, classifier, labels):
    """Process image exactly like your working testing code"""
    try:
        # Use YOUR proven hand detection approach
        hands, img = detector.findHands(cv_image)
        
        if hands:  # ONLY predict when hands are actually detected!
            print("✅ REAL HANDS DETECTED by HandDetector!")
            
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
            
            print(f"🎯 REAL PREDICTION: {predicted_label} ({confidence:.1f}%)")
            
            return predicted_label, confidence, True
        
        else:
            print("❌ NO HANDS DETECTED by HandDetector - No prediction")
            return "No gesture detected", 0, False
            
    except Exception as e:
        print(f"❌ Processing error: {e}")
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
        print(f"❌ Image preprocessing error: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Correct API using YOUR proven approach!"})

@app.route('/api/predict/words', methods=['POST'])
def predict_words():
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({"status": "error", "message": "No image data"}), 400
        
        print("🔍 WORDS PREDICTION using YOUR proven HandDetector approach")
        
        # Convert image
        cv_image = preprocess_image(image_data)
        if cv_image is None:
            return jsonify({"status": "error", "message": "Image processing failed"}), 400
        
        # Process using YOUR proven approach
        predicted_word, confidence, has_hands = process_image_like_your_code(
            cv_image, words_classifier, words_labels)
        
        if not has_hands:
            return jsonify({
                "status": "no_hands",
                "prediction": predicted_word,
                "confidence": confidence,
                "message": "No hands detected by HandDetector"
            }), 200
        
        return jsonify({
            "status": "success",
            "prediction": predicted_word,
            "confidence": round(confidence, 2)
        })
        
    except Exception as e:
        print(f"❌ Words prediction error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/predict/alphabet', methods=['POST'])
def predict_alphabet():
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({"status": "error", "message": "No image data"}), 400
        
        print("🔍 ALPHABET PREDICTION using YOUR proven HandDetector approach")
        
        # Convert image
        cv_image = preprocess_image(image_data)
        if cv_image is None:
            return jsonify({"status": "error", "message": "Image processing failed"}), 400
        
        # Process using YOUR proven approach
        predicted_letter, confidence, has_hands = process_image_like_your_code(
            cv_image, alphabet_classifier, alphabet_labels)
        
        if not has_hands:
            return jsonify({
                "status": "no_hands",
                "prediction": predicted_letter,
                "confidence": confidence,
                "message": "No hands detected by HandDetector"
            }), 200
        
        return jsonify({
            "status": "success",
            "prediction": predicted_letter,
            "confidence": round(confidence, 2)
        })
        
    except Exception as e:
        print(f"❌ Alphabet prediction error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/labels/alphabet', methods=['GET'])
def get_alphabet_labels():
    return jsonify({"status": "success", "labels": alphabet_labels})

@app.route('/api/labels/words', methods=['GET'])
def get_words_labels():
    return jsonify({"status": "success", "labels": words_labels})

if __name__ == '__main__':
    # Get port from environment variable for deployment, default to 5004 for local development
    port = int(os.environ.get('PORT', 5004))
    
    print("🚀 Starting CORRECT APP using YOUR proven HandDetector approach!")
    print(f"📍 Running on port {port}")
    print("✅ Using cvzone.HandTrackingModule.HandDetector (like your working code)")
    print("✅ Only predicts when hands are ACTUALLY detected")
    print("✅ Same processing logic as your working testing code")
    
    # Use debug=False for production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
