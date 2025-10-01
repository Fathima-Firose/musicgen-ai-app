import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Route for home page
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Serve music files (from root folder)
@app.route('/static/music/<path:filename>')
def serve_music(filename):
    # File is in the root folder, ignore 'music/' subpath
    file_path = filename.replace("music/", "")
    return send_from_directory('.', file_path)

# Demo "generate music" endpoint
@app.route('/generate-music', methods=['POST'])
def generate_music():
    try:
        # Always return the same demo file
        demo_file = "musicgen.wav"
        return jsonify({"url": f"/static/music/{demo_file}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run locally
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
