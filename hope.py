from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import librosa
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from main import find_time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins


# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files
    mic_links = {}
    file_paths = []

    for key in files:
        file = files[key]
        if file:
            # Save file to the upload folder
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            # Append the relative file path to the list
            file_paths.append(os.path.relpath(file_path))
            # Track which mic is linked with which file
            mic_id = key.replace('file', 'mic')  # Map file input name to mic id
            mic_link = request.form.get(mic_id)  # Get corresponding mic id from hidden input
            mic_links[file.filename] = mic_link
    result = find_time({
        'file_paths': file_paths
    })

    # Return result as JSON
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
