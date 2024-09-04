from flask import Flask, request, jsonify, redirect, url_for,send_from_directory
from cvzone.ClassificationModule import Classifier
import threading

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize model globally if needed
model_path = 'model1/keras_model.h5'
labels_path = 'model1/labels.txt'
classifier = Classifier(model_path, labels_path)

# Import functions from your scripts
from testing import run_testing
from testing import run_testing_words

# Use a flag to indicate whether testing is running
testing_running = {
    'alphabets': False,
    'words': False
}

# Define a function to run testing asynchronously
def run_testing_async(testing_function, category):
    def wrapper():
        if testing_running[category]:
            print(f"{category} testing already running.")
            return
        testing_running[category] = True
        result = testing_function()
        testing_running[category] = False
    thread = threading.Thread(target=wrapper)
    thread.start()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/learn-alphabets', methods=['POST'])
def learn_alphabets():
    try:
        run_testing_async(run_testing, 'alphabets')
        return redirect('/learning-start')
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/learn-words', methods=['POST'])
def learn_words():
    try:
        run_testing_async(run_testing_words, 'words')
        return redirect('/learning-start')
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/learning-start')
def learning_start():
    return send_from_directory('static', 'learning_start.html')

if __name__ == '__main__':
    app.run(debug=True)
