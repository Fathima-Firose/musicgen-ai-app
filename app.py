from flask import Flask, request, jsonify, send_from_directory
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
import os

app = Flask(__name__)

# --- AI Model Setup (Smaller Model) ---
device = "cpu"
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(device)
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(device)

# Load speaker embeddings
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
# --- End Model Setup ---

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
        # Duration is not controllable with this model, it depends on the text length.

        inputs = processor(text=prompt, return_tensors="pt").to(device)
        
        speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
        
        output_filename = f"speech_{hash(prompt)}.wav"
        output_path = os.path.join('static/music', output_filename)
        
        sf.write(output_path, speech.cpu().numpy(), samplerate=16000)

        file_url = f"/static/music/{output_filename}"
        return jsonify({'url': file_url})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Failed to generate speech'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
