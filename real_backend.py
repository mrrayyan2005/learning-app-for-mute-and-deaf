from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import base64
import io
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

# Initialize models
try:
    # Load alphabet model
    alphabet_classifier = Classifier("model1/keras_model.h5", "model1/labels.txt")
    alphabet_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
    
    # Load words model  
    words_classifier = Classifier("Model2/keras_model.h5", "Model2/labels.txt")
    words_labels = ["Bye", "Hello", "No", "Perfect", "Thank You", "Yes"]
    
    detector = HandDetector(maxHands=1)
    
    models_loaded = True
    print("✅ AI Models loaded successfully!")
except Exception as e:
    models_loaded = False
    print(f"❌ Error loading models: {e}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "🤖 SignLearn REAL AI Backend",
        "status": "success",
        "models_loaded": models_loaded,
        "available_endpoints": {
            "health": "/api/health",
            "labels_words": "/api/labels?type=words", 
            "labels_alphabet": "/api/labels?type=alphabet",
            "predict": "/api/predict (POST)"
        },
        "note": "Real AI-powered gesture recognition using your trained models"
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "success",
        "message": "SignLearn REAL AI API is running!",
        "models_status": "loaded" if models_loaded else "failed",
        "version": "2.0.0"
    })

@app.route('/api/labels', methods=['GET'])
def get_labels():
    label_type = request.args.get('type', 'words')
    
    if label_type == 'alphabet':
        labels = alphabet_labels
    else:
        labels = words_labels
        
    return jsonify({
        "status": "success",
        "type": label_type,
        "labels": labels,
        "count": len(labels),
        "model_file": f"{'model1' if label_type == 'alphabet' else 'Model2'}/keras_model.h5"
    })

def process_hand_image(img, detector, classifier, labels):
    """Process image with real hand detection and AI prediction"""
    offset = 20
    imgSize = 300
    
    # Detect hands
    hands, img = detector.findHands(img, draw=False)
    
    if not hands:
        return None, 0, "No hands detected"
    
    hand = hands[0]
    x, y, w, h = hand['bbox']
    
    # Create white background
    imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
    
    # Crop hand region
    imgCrop = img[max(0, y - offset):y + h + offset, max(0, x - offset):x + w + offset]
    
    if imgCrop.size == 0:
        return None, 0, "Failed to crop hand region"
    
    # Resize maintaining aspect ratio
    aspectRatio = h / w
    
    if aspectRatio > 1:
        k = imgSize / h
        wCal = math.ceil(k * w)
        if wCal > 0:
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
    else:
        k = imgSize / w
        hCal = math.ceil(k * h)
        if hCal > 0:
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
    
    # Get prediction using your trained model
    try:
        prediction, index = classifier.getPrediction(imgWhite, draw=False)
        predicted_label = labels[index]
        confidence = float(np.max(prediction)) * 100
        
        return predicted_label, confidence, "Success"
    except Exception as e:
        return None, 0, f"Prediction error: {str(e)}"

@app.route('/api/predict', methods=['POST'])
def predict():
    if not models_loaded:
        return jsonify({
            "status": "error",
            "message": "AI models not loaded. Check model files."
        }), 500
    
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"status": "error", "message": "No image data"}), 400
            
        prediction_type = data.get('type', 'words')
        
        # Decode base64 image
        image_data = data['image'].split(',')[1]  # Remove data:image/jpeg;base64,
        image_bytes = base64.b64decode(image_data)
        
        # Convert to OpenCV format
        pil_image = Image.open(io.BytesIO(image_bytes))
        img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Select appropriate model and labels
        if prediction_type == 'alphabet':
            classifier = alphabet_classifier
            labels = alphabet_labels
        else:
            classifier = words_classifier
            labels = words_labels
        
        # Process with real AI
        predicted_label, confidence, message = process_hand_image(img, detector, classifier, labels)
        
        if predicted_label is None:
            return jsonify({
                "status": "no_hands",
                "prediction": "No gesture detected",
                "confidence": 0,
                "message": message
            })
        
        return jsonify({
            "status": "success",
            "prediction": predicted_label,
            "confidence": round(confidence, 2),
            "model_type": prediction_type,
            "message": "Real AI prediction using your trained models"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Error processing image: {str(e)}"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
