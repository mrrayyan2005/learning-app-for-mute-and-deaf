from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Parse query parameters
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        label_type = query_params.get('type', ['words'])[0]
        
        # Define labels (same as your real models)
        alphabet_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
        words_labels = ["Bye", "Hello", "No", "Perfect", "Thank You", "Yes"]
        
        if label_type == 'alphabet':
            labels = alphabet_labels
        else:
            labels = words_labels
            
        response = {
            "status": "success",
            "type": label_type,
            "labels": labels,
            "count": len(labels)
        }
        
        self.wfile.write(json.dumps(response).encode())
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
