import os
from flask import Flask, request, jsonify, send_from_directory

# Ensure static/music exists
os.makedirs("static/music", exist_ok=True)

app = Flask(__name__)

# Route for home page
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Serve music files
@app.route('/static/music/<path:filename>')
def serve_music(filename):
    return send_from_directory('static/music', filename)

# Demo "generate music" endpoint
@app.route('/generate-music', methods=['POST'])
def generate_music():
    try:
        # Ignore prompt/duration — always return demo file
        demo_file = "musicgen-1.wav"
        return jsonify({"url": f"/static/music/{demo_file}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Local testing
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
