import os
os.environ["TRANSFORMERS_CACHE"] = "/opt/render/.cache/huggingface"

from flask import Flask, request, jsonify, send_from_directory
import numpy as np
import scipy.io.wavfile as wavfile
import time

app = Flask(__name__)

# lazy-loaded pipeline
pipe = None

def get_pipe():
    global pipe
    if pipe is None:
        # import here to avoid heavy import at module load
        from transformers import pipeline
        print("Loading MusicGen pipeline (this may take a while)...", flush=True)
        pipe = pipeline("text-to-audio", "facebook/musicgen-small", device=-1)  # -1 -> CPU
        print("Pipeline loaded.", flush=True)
    return pipe

# Ensure output dir exists
os.makedirs("static/music", exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/music/<path:filename>')
def serve_music(filename):
    return send_from_directory('static/music', filename)

@app.route('/generate-music', methods=['POST'])
def generate_music():
    try:
        data = request.json or {}
        prompt = data.get('prompt', '')
        duration = int(min(int(data.get('duration', 15)), 45))  # cap duration to 45s

        if not prompt.strip():
            return jsonify({"error": "Empty prompt"}), 400

        p = get_pipe()
        max_new_tokens = int(duration * 50)
        music = p(prompt, forward_params={"max_new_tokens": max_new_tokens})

        sampling_rate = music["sampling_rate"]
        audio_numpy = music["audio"][0].T

        output_filename = f"music_{abs(hash(prompt))}_{int(time.time())}.wav"
        output_path = os.path.join("static/music", output_filename)

        audio_int16 = np.int16(audio_numpy * 32767)
        wavfile.write(output_path, rate=sampling_rate, data=audio_int16)

        return jsonify({"url": f"/static/music/{output_filename}"})
    except Exception as e:
        print("Error in generate-music:", e, flush=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
