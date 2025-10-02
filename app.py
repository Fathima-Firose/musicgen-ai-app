from flask import Flask, render_template_string, request, send_from_directory, jsonify
import time
import os

app = Flask(__name__)

# Load index.html directly from root (no templates folder needed)
@app.route('/')
def index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return render_template_string(html_content)
    except Exception as e:
        return f"Error loading index.html: {e}", 500

# Handle music generation
@app.route('/generate-music', methods=['POST'])
def generate_music():
    prompt = request.form.get("prompt", "").lower()

    # Artificial loading delay (8–10 seconds)
    time.sleep(8)

    # Determine which music file to serve
    if "happy" in prompt:
        filename = "musicgen-1.wav"
    elif "sad" in prompt:
        filename = "musicgen-2.wav"
    elif "pop" in prompt:
        filename = "musicgen-3.wav"
    else:
        filename = "musicgen-1.wav"  # default

    music_path = os.path.join("static", "music", filename)
    if os.path.exists(music_path):
        # Return URL path for frontend to play/download
        return jsonify({"file": f"/get-music/{filename}"})
    else:
        return jsonify({"error": f"{filename} not found!"}), 404

# Serve music files from static/music folder
@app.route('/get-music/<filename>')
def get_music(filename):
    music_dir = os.path.join(app.root_path, "static", "music")
    if os.path.exists(os.path.join(music_dir, filename)):
        return send_from_directory(music_dir, filename, mimetype="audio/wav", as_attachment=False)
    else:
        return "File not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
