from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # allow frontend to connect

# Folder to store uploaded files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# Create uploads folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Home route
@app.route('/')
def home():
    return "Backend Running!"

# Upload file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file provided"}), 400

    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))

    return jsonify({"message": "File uploaded successfully"})

# Get all uploaded files
@app.route('/notes', methods=['GET'])
def get_notes():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

# Download file
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# Run app (ALWAYS LAST)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')