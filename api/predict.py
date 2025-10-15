from http.server import BaseHTTPRequestHandler
import json
import random
import time

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            image_data = data.get('image')
            prediction_type = data.get('type', 'words')
            
            if not image_data:
                response = {"status": "error", "message": "No image data provided"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Demo labels (same as your real models)
            alphabet_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
            words_labels = ["Bye", "Hello", "No", "Perfect", "Thank You", "Yes"]
            
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
                response = {
                    "status": "no_hands",
                    "prediction": "No gesture detected",
                    "confidence": 0,
                    "message": "No hands detected - position your hand clearly in camera view"
                }
            else:
                # Generate realistic prediction
                predicted_label = random.choice(labels)
                confidence = random.uniform(75, 95)
                
                response = {
                    "status": "success",
                    "prediction": predicted_label,
                    "confidence": round(confidence, 2),
                    "demo": True,
                    "message": "Demo mode - simulated prediction"
                }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            response = {"status": "error", "message": str(e)}
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
