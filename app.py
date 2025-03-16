from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import base64
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    print("🚨 Warning: HUGGINGFACE_API_KEY is missing!")

# Initialize Flask App
app = Flask(__name__)

# Fix CORS for Netlify communication
CORS(app, resources={r"/api/*": {"origins": ["https://museevirtuel.netlify.app", "http://localhost:5173"]}})

# API Health Check Route
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

# AI Image Generation Route
@app.route("/api/generate", methods=["POST"])
def generate_image():
    if not HUGGINGFACE_API_KEY:
        print("🚨 API Key MISSING in Flask!")
        return jsonify({"error": "API key missing"}), 401

    print(f"✅ Using API Key: {HUGGINGFACE_API_KEY[:6]}**********")

    data = request.json
    style = data.get("style", "")
    
    # Create a more detailed prompt for better results
    prompt = f"A masterpiece painting in the style of {style}, highly detailed, artistic, professional quality"

    # Using a more reliable model for art generation
    url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "num_inference_steps": 50,
            "guidance_scale": 7.5,
            "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy"
        }
    }

    print("📤 Sending request to Hugging Face API...")
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"📥 Hugging Face API Response Status: {response.status_code}")

        if response.status_code == 200:
            # Convert binary image data to base64
            image_bytes = response.content
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            image_url = f"data:image/jpeg;base64,{base64_image}"
            
            return jsonify({
                "imageUrl": image_url,
                "prompt": prompt
            })
        else:
            error_message = response.text
            print(f"🚨 API Error: {error_message}")
            return jsonify({
                "error": "AI image generation failed",
                "details": error_message
            }), response.status_code

    except Exception as e:
        print(f"🚨 Exception: {str(e)}")
        return jsonify({
            "error": "Server error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    print("🚀 Using Hugging Face API for AI Image Generation")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=True)
