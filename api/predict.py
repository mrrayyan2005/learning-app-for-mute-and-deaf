from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import time

app = Flask(__name__)
CORS(app)

# Demo labels (same as your real models)
alphabet_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
words_labels = ["Bye", "Hello", "No", "Perfect", "Thank You", "Yes"]

def simulate_prediction(prediction_type):
    """Simulate realistic predictions for demo purposes"""
    
    # Choose labels based on type
    if prediction_type == 'alphabet':
        labels = alphabet_labels
    else:
        labels = words_labels
    
    # Simulate processing time
    time.sleep(0.5)
    
    # Generate realistic prediction
    predicted_label = random.choice(labels)
    confidence = random.uniform(75, 95)  # Realistic confidence scores
    
    return predicted_label, confidence

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
        
        # Simulate realistic behavior
        # 20% chance of "no hands detected" for realism
        if random.random() < 0.2:
            return jsonify({
                "status": "no_hands",
                "prediction": "No gesture detected",
                "confidence": 0,
                "message": "No hands detected - position your hand clearly in camera view"
            }), 200
        
        # Generate prediction
        predicted_result, confidence = simulate_prediction(prediction_type)
        
        return jsonify({
            "status": "success",
            "prediction": predicted_result,
            "confidence": round(confidence, 2),
            "demo": True,
            "message": "Demo mode - simulated prediction"
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
