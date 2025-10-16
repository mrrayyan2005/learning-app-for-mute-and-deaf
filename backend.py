from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import time
import os

app = Flask(__name__)
CORS(app)

# Demo labels (same as your real models)
alphabet_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
words_labels = ["Bye", "Hello", "No", "Perfect", "Thank You", "Yes"]

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "🚀 SignLearn Backend API Only",
        "status": "success",
        "type": "backend_api",
        "available_endpoints": {
            "health": "/api/health",
            "labels_words": "/api/labels?type=words", 
            "labels_alphabet": "/api/labels?type=alphabet",
            "predict": "/api/predict (POST)"
        },
        "note": "This is backend API only - use with your Vercel frontend"
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "success",
        "message": "SignLearn Backend API is running!",
        "version": "1.0.0",
        "port": os.environ.get('PORT', '5000'),
        "endpoints": [
            "/api/health",
            "/api/labels?type=words",
            "/api/labels?type=alphabet", 
            "/api/predict"
        ]
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
        "count": len(labels)
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No JSON data"}), 400
            
        image_data = data.get('image')
        prediction_type = data.get('type', 'words')
        
        if not image_data:
            return jsonify({"status": "error", "message": "No image data"}), 400
        
        # Choose labels based on type
        if prediction_type == 'alphabet':
            labels = alphabet_labels
        else:
            labels = words_labels
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Simulate realistic behavior
        # 20% chance of "no hands detected" for realism
        if random.random() < 0.2:
            return jsonify({
                "status": "no_hands",
                "prediction": "No gesture detected",
                "confidence": 0,
                "message": "No hands detected - position your hand clearly in camera view"
            })
        
        # Generate realistic prediction
        predicted_label = random.choice(labels)
        confidence = random.uniform(75, 95)
        
        return jsonify({
            "status": "success",
            "prediction": predicted_label,
            "confidence": round(confidence, 2),
            "demo": True,
            "message": "Demo mode - simulated prediction"
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
