from flask import Flask, render_template, request, send_from_directory, jsonify
import time
import os

app = Flask(__name__)

# Home page
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate-music', methods=['POST'])
def generate_music():
    prompt = request.form.get("prompt", "").lower()

    # Artificial delay 8–10 secs
    time.sleep(8)

    # Decide which file to play
    if "happy" in prompt:
        filename = "musicgen-1.wav"
    elif "sad" in prompt:
        filename = "musicgen-2.wav"
    elif "pop" in prompt:
        filename = "musicgen-3.wav"
    else:
        filename = "musicgen-1.wav"  # default

    music_dir = os.path.join(app.root_path, "static")
    file_path = os.path.join(music_dir, filename)

    if os.path.exists(file_path):
        return jsonify({"file": f"/static/{filename}"})
    else:
        return jsonify({"error": f"{filename} not found!"}), 404

# Serve files from static/music/
@app.route('/static/<filename>')
def get_music(filename):
    music_dir = os.path.join(app.root_path, "static")
    return send_from_directory(music_dir, filename, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)


