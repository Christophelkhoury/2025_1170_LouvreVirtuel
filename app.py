from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()
STABILITY_AI_API_KEY = os.getenv("STABILITY_AI_API_KEY")

# ✅ Fix CORS for Netlify
CORS(app, resources={r"/*": {"origins": ["https://museevirtuel.netlify.app", "http://localhost:5173"]}}, supports_credentials=True)

# 🔹 API Health Check
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "healthy",
        "api_key_configured": bool(STABILITY_AI_API_KEY),
        "message": "CORS fixed, AI API running."
    })

# 🔹 AI Image Generation Route
@app.route("/api/generate", methods=["POST"])
def generate_image():
    if not STABILITY_AI_API_KEY:
        return jsonify({"error": "API key missing"}), 500

    data = request.json
    prompt = data.get("prompt", "A beautiful AI-generated artwork")

    # ✅ Fix: Use `multipart/form-data` instead of JSON
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"
    headers = {
        "Authorization": f"Bearer {STABILITY_AI_API_KEY}",
        "Accept": "application/json",  # ✅ Fix: Ensure API expects JSON response
    }
    
    # ✅ Stability AI API requires `multipart/form-data`
    files = {
        "prompt": (None, prompt),
        "width": (None, "512"),
        "height": (None, "512"),
        "steps": (None, "30")
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "AI image generation failed", "details": response.text}), response.status_code

# 🔹 Main Run Condition
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=False)
