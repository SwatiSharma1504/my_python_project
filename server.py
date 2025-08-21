from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)
API_KEY = "AIzaSyAztgRSZCvK2Bpkp-iUad8lemZplDPL7UU"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    prompt = data.get('query', '')
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            reply = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": reply})
        else:
            print("❌ Gemini Error:", response.status_code, response.text)
            return jsonify({"reply": "Gemini API Error: " + response.text}), 500
    except Exception as e:
     print("❌ Exception:", e)
    return jsonify({"reply": "Internal Server Error"}), 500
if __name__ == '__main__':
    app.run(debug=True)