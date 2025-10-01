from flask import Flask, request, jsonify, send_from_directory
from transformers import pipeline
import torch
import scipy.io.wavfile
import numpy as np
import os

app = Flask(__name__)

# --- AI Model Setup ---
device = "cpu"
pipe = pipeline("text-to-audio", "facebook/musicgen-small", device=device)

# --- Ensure static/music directory exists ---
if not os.path.exists('static/music'):
    os.makedirs('static/music')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/music/<path:filename>')
def serve_music(filename):
    return send_from_directory('static/music', filename)

@app.route('/generate-music', methods=['POST'])
def generate_music():
    try:
        data = request.json
        prompt = data.get('prompt')
        duration = data.get('duration', 15)

        max_new_tokens = int(duration * 50)
        music = pipe(prompt, forward_params={"max_new_tokens": max_new_tokens})
        
        sampling_rate = music["sampling_rate"]
        audio_numpy = music["audio"][0].T
        
        output_filename = f"music_{hash(prompt)}.wav"
        output_path = os.path.join('static/music', output_filename)
        
        audio_int16 = np.int16(audio_numpy * 32767)
        scipy.io.wavfile.write(output_path, rate=sampling_rate, data=audio_int16)

        file_url = f"/static/music/{output_filename}"
        return jsonify({'url': file_url})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Failed to generate music'}), 500

if __name__ == '__main__':
    # Render uses port 10000 by default
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))