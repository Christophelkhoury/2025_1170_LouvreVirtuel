from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    print("🚨 Warning: HUGGINGFACE_API_KEY is missing!")

# ✅ Initialize Flask Ap
app = Flask(__name__)

# ✅ Fix CORS for Netlify communication
CORS(app, resources={r"/api/*": {"origins": ["https://museevirtuel.netlify.app", "http://localhost:5173"]}})

# 🔹 API Health Check Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask API is running!", "status": "OK"})

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "healthy",
        "api_key_configured": bool(HUGGINGFACE_API_KEY),
        "message": "Using Hugging Face API for AI image generation."
    })

# 🔹 AI Image Generation Route
@app.route("/api/generate", methods=["POST"])
def generate_image():
    if not HUGGINGFACE_API_KEY:
        print("🚨 API Key MISSING in Flask!")
        return jsonify({"error": "API key missing"}), 401

    print(f"✅ Using API Key: {HUGGINGFACE_API_KEY[:6]}**********")  # Hides most of the key for security

    data = request.json
    prompt = data.get("prompt", "A beautiful AI-generated artwork")

    url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": prompt}

    print("📤 Sending request to Hugging Face API...")
    response = requests.post(url, headers=headers, json=payload)
    print("📥 Hugging Face API Response:", response.status_code, response.text)

    if response.status_code == 200:
        return jsonify({"imageUrl": response.content.decode("utf-8")})
    else:
        return jsonify({"error": "AI image generation failed", "details": response.text}), response.status_code

if __name__ == "__main__":
    print("🚀 Using Hugging Face API for AI Image Generation")
    app.run(host="0.0.0.0", port=10000, debug=True)
