from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Your exact labels
alphabet_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
words_labels = ["Bye", "Hello", "No", "Perfect", "Thank You", "Yes"]

def handler(request):
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        # Get the type from query parameter
        label_type = request.args.get('type', 'words')
        
        if label_type == 'alphabet':
            labels = alphabet_labels
        else:
            labels = words_labels
            
        return jsonify({
            "status": "success", 
            "labels": labels
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
