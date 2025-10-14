from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def handler(request):
    return jsonify({"status": "healthy", "message": "SignLearn API on Vercel!"})
