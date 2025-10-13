from flask import Flask, request, jsonify
from flask_cors import CORS
from cvzone.ClassificationModule import Classifier
import cv2
import numpy as np
import base64
import io
from PIL import Image
import math

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize models
alphabet_classifier = Classifier("model1/keras_model.h5", "model1/labels.txt")
words_classifier = Classifier("Model2/keras_model.h5", "Model2/labels.txt")

# Labels
alphabet_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
words_labels = ["Bye", "Hello", "No", "Perfect", "Thank You", "Yes"]

def detect_hands_in_image(cv_image):
    """Simple hand/gesture detection using OpenCV image analysis"""
    try:
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection to find contours
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area and shape
        significant_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            # Hand-like shapes should have reasonable area
            if 500 < area < 15000:  # Adjust these values based on your camera setup
                # Calculate contour properties
                hull = cv2.convexHull(contour)
                hull_area = cv2.contourArea(hull)
                if hull_area > 0:
                    solidity = area / hull_area
                    # Hands typically have solidity between 0.7-0.95
                    if 0.6 < solidity < 0.98:
                        significant_contours.append(contour)
        
        # Calculate image variance (helps detect if there's actual content vs empty background)
        image_variance = np.var(gray)
        
        # Detect skin-like colors in HSV space
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        
        # Define skin color range in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Create mask for skin-like colors
        skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
        skin_pixels = np.sum(skin_mask > 0)
        total_pixels = cv_image.shape[0] * cv_image.shape[1]
        skin_ratio = skin_pixels / total_pixels
        
        # Combine multiple detection criteria
        has_contours = len(significant_contours) > 0
        has_variance = image_variance > 100  # Not a plain background
        has_skin = skin_ratio > 0.01  # At least 1% skin-like pixels
        
        hands_detected = has_contours and has_variance and has_skin
        
        if hands_detected:
            print(f"✅ Hand/gesture detected: {len(significant_contours)} significant shapes, variance: {image_variance:.1f}, skin: {skin_ratio:.3f}")
            return True, len(significant_contours)
        else:
            print(f"❌ No hands detected: shapes={len(significant_contours)}, variance={image_variance:.1f}, skin={skin_ratio:.3f}")
            return False, 0
            
    except Exception as e:
        print(f"Error in hand detection: {e}")
        return False, 0

def preprocess_image(image_data):
    """Preprocess image and check for hands before prediction"""
    try:
        # Decode base64 image
        image_data = image_data.split(',')[1]  # Remove data:image/jpeg;base64,
        image_bytes = base64.b64decode(image_data)
        
        # Convert to PIL Image
        pil_image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to OpenCV format
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # First check if hands are present
        hands_detected, hand_count = detect_hands_in_image(cv_image)
        
        if not hands_detected:
            return None, False, hand_count
        
        # Resize to model input size only if hands detected
        imgSize = 300
        img_resized = cv2.resize(cv_image, (imgSize, imgSize))
        
        return img_resized, True, hand_count
        
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None, False, 0

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "SignLearn API is running"
    })

@app.route('/api/predict/alphabet', methods=['POST'])
def predict_alphabet():
    """Predict alphabet sign from image"""
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({
                "status": "error",
                "message": "No image data provided"
            }), 400
        
        # Preprocess image and check for hands
        processed_image, has_hands, hand_count = preprocess_image(image_data)
        if not has_hands:
            return jsonify({
                "status": "no_hands",
                "message": "No hands detected in image",
                "prediction": "No gesture detected",
                "confidence": 0,
                "hand_count": hand_count
            }), 200
        
        if processed_image is None:
            return jsonify({
                "status": "error",
                "message": "Failed to process image"
            }), 400
        
        # Get prediction
        prediction, index = alphabet_classifier.getPrediction(processed_image, draw=False)
        
        # Debug prediction format
        print(f"Prediction type: {type(prediction)}, shape: {getattr(prediction, 'shape', 'No shape')}")
        print(f"Index: {index}, type: {type(index)}")
        
        # Handle different prediction formats
        if hasattr(prediction, 'shape') and len(prediction.shape) > 1:
            # Multi-dimensional array
            confidence = float(np.max(prediction)) * 100
            pred_array = prediction[0] if len(prediction.shape) == 2 else prediction
        else:
            # Single prediction or 1D array
            confidence = float(prediction) * 100 if np.isscalar(prediction) else float(np.max(prediction)) * 100
            pred_array = prediction if hasattr(prediction, '__len__') else [prediction]
        
        # Ensure index is within bounds
        if 0 <= index < len(alphabet_labels):
            predicted_letter = alphabet_labels[index]
        else:
            predicted_letter = "Unknown"
            confidence = 0
        
        # Create all_predictions safely
        all_predictions = {}
        try:
            if hasattr(pred_array, '__len__') and len(pred_array) >= len(alphabet_labels):
                all_predictions = {
                    alphabet_labels[i]: float(pred_array[i]) * 100 
                    for i in range(len(alphabet_labels))
                }
        except Exception as e:
            print(f"Error creating all_predictions: {e}")
            all_predictions = {predicted_letter: confidence}
        
        return jsonify({
            "status": "success",
            "prediction": predicted_letter,
            "confidence": round(confidence, 2),
            "all_predictions": all_predictions
        })
        
    except Exception as e:
        print(f"Error in alphabet prediction: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/predict/words', methods=['POST'])
def predict_words():
    """Predict word sign from image"""
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({
                "status": "error",
                "message": "No image data provided"
            }), 400
        
        # Preprocess image and check for hands
        processed_image, has_hands, hand_count = preprocess_image(image_data)
        if not has_hands:
            return jsonify({
                "status": "no_hands",
                "message": "No hands detected in image",
                "prediction": "No gesture detected",
                "confidence": 0,
                "hand_count": hand_count
            }), 200
        
        if processed_image is None:
            return jsonify({
                "status": "error",
                "message": "Failed to process image"
            }), 400
        
        # Get prediction
        prediction, index = words_classifier.getPrediction(processed_image, draw=False)
        
        # Debug prediction format
        print(f"Words Prediction type: {type(prediction)}, shape: {getattr(prediction, 'shape', 'No shape')}")
        print(f"Words Index: {index}, type: {type(index)}")
        
        # Handle different prediction formats
        if hasattr(prediction, 'shape') and len(prediction.shape) > 1:
            # Multi-dimensional array
            confidence = float(np.max(prediction)) * 100
            pred_array = prediction[0] if len(prediction.shape) == 2 else prediction
        else:
            # Single prediction or 1D array
            confidence = float(prediction) * 100 if np.isscalar(prediction) else float(np.max(prediction)) * 100
            pred_array = prediction if hasattr(prediction, '__len__') else [prediction]
        
        # Ensure index is within bounds
        if 0 <= index < len(words_labels):
            predicted_word = words_labels[index]
        else:
            predicted_word = "Unknown"
            confidence = 0
        
        # Create all_predictions safely
        all_predictions = {}
        try:
            if hasattr(pred_array, '__len__') and len(pred_array) >= len(words_labels):
                all_predictions = {
                    words_labels[i]: float(pred_array[i]) * 100 
                    for i in range(len(words_labels))
                }
        except Exception as e:
            print(f"Error creating words all_predictions: {e}")
            all_predictions = {predicted_word: confidence}
        
        return jsonify({
            "status": "success",
            "prediction": predicted_word,
            "confidence": round(confidence, 2),
            "all_predictions": all_predictions
        })
        
    except Exception as e:
        print(f"Error in words prediction: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/labels/alphabet', methods=['GET'])
def get_alphabet_labels():
    """Get available alphabet labels"""
    return jsonify({
        "status": "success",
        "labels": alphabet_labels
    })

@app.route('/api/labels/words', methods=['GET'])
def get_words_labels():
    """Get available word labels"""
    return jsonify({
        "status": "success",
        "labels": words_labels
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
