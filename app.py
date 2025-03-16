from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Get API Key from Environment Variables
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

if not REPLICATE_API_KEY:
    print("⚠️ Warning: REPLICATE_API_KEY is missing! Ensure it's set in .env or Render.")

# ✅ Initialize Flask App
app = Flask(__name__)

# ✅ Fix CORS - Allow Netlify to communicate with Flask
CORS(app, resources={r"/api/*": {"origins": ["https://museevirtuel.netlify.app", "http://localhost:5173"]}})

# ✅ Debugging - Log API Calls
@app.before_request
def log_request():
    print(f"📥 Incoming Request: {request.method} {request.path}")

# 🔹 API Health Check Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask API is running!", "status": "OK"})

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "healthy",
        "api_key_configured": bool(REPLICATE_API_KEY),
        "message": "Using Replicate API for AI image generation."
    })

# 🔹 AI Image Generation Route
@app.route("/api/generate", methods=["POST"])
def generate_image():
    if not REPLICATE_API_KEY:
        return jsonify({"error": "API key missing"}), 500

    data = request.json
    prompt = data.get("prompt", "A beautiful AI-generated artwork")

    # ✅ Replicate API Request
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "version": "db21e12372a7e68a007fe1b8e7b3f4e4b4b29268e47339c14716fba24880a12b",  # Stable Diffusion 2.1
        "input": {
            "prompt": prompt,
            "width": 512,
            "height": 512
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    # ✅ Debugging - Log API Response
    print("📥 Replicate API Response:", response.status_code, response.text)

    if response.status_code == 200:
        try:
            json_data = response.json()
            if "urls" in json_data and "get" in json_data["urls"]:
                return jsonify({"imageUrl": json_data["urls"]["get"]})
            else:
                return jsonify({"error": "No image URL returned from Replicate", "response": json_data}), 500
        except Exception as e:
            return jsonify({"error": "Failed to parse AI response", "details": str(e)}), 500
    else:
        return jsonify({"error": "AI image generation failed", "details": response.text}), response.status_code

# ✅ Ensure Flask Runs Properly
if __name__ == "__main__":
    print("🚀 Using Replicate API for AI Image Generation")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=True)
