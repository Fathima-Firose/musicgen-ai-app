from flask import Flask, render_template, request, jsonify, send_from_directory
import os, time

app = Flask(__name__)

# Serve homepage
@app.route('/')
def index():
    return render_template('index.html')

# Generate music (simulate AI delay + keyword-based choice)
@app.route('/generate-music', methods=['POST'])
def generate_music():
    data = request.get_json()
    prompt = data.get('prompt', '').lower()

    # Fake processing delay (simulate AI generating music)
    time.sleep(8)

    # Choose file based on keyword
    if "happy" in prompt:
        filename = "musicgen-1.wav"
    elif "sad" in prompt:
        filename = "musicgen-2.wav"
    elif "pop" in prompt:
        filename = "musicgen-3.wav"
    else:
        filename = "musicgen-1.wav"  # default

    file_url = f"/static/music/{filename}"
    return jsonify({"url": file_url})

# Route to serve music files
@app.route('/static/music/<path:filename>')
def serve_music(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/music'), filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
