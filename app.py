import os
from flask import Flask, request, jsonify, send_from_directory
import numpy as np
import scipy.io.wavfile as wavfile
import time

# Set HuggingFace cache path
os.environ["HF_HOME"] = "/opt/render/.cache/huggingface"
os.makedirs(os.environ["HF_HOME"], exist_ok=True)
os.makedirs("static/music", exist_ok=True)

# Initialize Flask app
app = Flask(__name__)

# Load lightweight MusicGen pipeline at startup
print("Loading lightweight MusicGen pipeline (tiny, CPU-friendly)...", flush=True)
from transformers import pipeline

try:
    pipe = pipeline("text-to-audio", "facebook/musicgen-tiny", device=-1)  # CPU
    print("Pipeline loaded successfully.", flush=True)
except Exception as e:
    print("Failed to load MusicGen pipeline:", e, flush=True)
    pipe = None

# Routes
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/music/<path:filename>')
def serve_music(filename):
    return send_from_directory('static/music', filename)

@app.route('/generate-music', methods=['POST'])
def generate_music():
    if pipe is None:
        return jsonify({"error": "MusicGen pipeline not loaded"}), 500

    try:
        data = request.json or {}
        prompt = data.get('prompt', '').strip()
        duration = int(min(int(data.get('duration', 10)), 10))  # max 10s for CPU

        if not prompt:
            return jsonify({"error": "Empty prompt"}), 400

        # Music generation
        max_new_tokens = int(duration * 50)
        music = pipe(prompt, forward_params={"max_new_tokens": max_new_tokens})

        sampling_rate = music["sampling_rate"]
        audio_numpy = music["audio"][0].T

        # Save as WAV
        output_filename = f"music_{abs(hash(prompt))}_{int(time.time())}.wav"
        output_path = os.path.join("static/music", output_filename)
        audio_int16 = np.int16(audio_numpy * 32767)
        wavfile.write(output_path, rate=sampling_rate, data=audio_int16)

        return jsonify({"url": f"/static/music/{output_filename}"})

    except Exception as e:
        print("Error generating music:", e, flush=True)
        return jsonify({"error": str(e)}), 500

# Local test server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
