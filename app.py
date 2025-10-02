from flask import Flask, render_template_string, request, send_file
import time
import os

app = Flask(__name__)

# Load index.html directly (since it's in root folder, not templates/)
@app.route('/')
def index():
    with open("index.html", "r") as f:
        html_content = f.read()
    return render_template_string(html_content)

@app.route('/generate-music', methods=['POST'])
def generate_music():
    prompt = request.form.get("prompt", "").lower()

    # Add artificial loading delay (8–10 secs)
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

    if os.path.exists(filename):
        return {"file": f"/get-music/{filename}"}
    else:
        return {"error": f"{filename} not found!"}, 404

@app.route('/get-music/<filename>')
def get_music(filename):
    if os.path.exists(filename):
        return send_file(filename, mimetype="audio/wav", as_attachment=False)
    else:
        return "File not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
