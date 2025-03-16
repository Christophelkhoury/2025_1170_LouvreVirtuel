from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API Key from Environment Variables
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

if not REPLICATE_API_KEY:
    print("⚠️ Warning: REPLICATE_API_KEY is missing! Ensure it's set in .env or Render.")

# Initialize Flask App
app = Flask(__name__)

# Fix CORS - Allow Netlify to communicate with Flask
CORS(app, resources={r"/api/*": {"origins": ["https://museevirtuel.netlify.app", "http://localhost:5173"]}})

# Debugging - Log API Calls
@app.before_request
def log_request():
    print(f"📥 Incoming Request: {request.method} {request.path}")

# API Health Check Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask API is running!", "status": "OK"})

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "healthy",
        "api_key_configured": bool(REPLICATE_API_KEY),
        "message": "Using Replicate API for image generation."
    })

# AI Image Generation Route
@app.route("/api/generate", methods=["POST"])
def generate_image():
    if not REPLICATE_API_KEY:
        return jsonify({"error": "API key missing"}), 500

    data = request.json
    prompt = data.get("prompt", "A beautiful AI-generated artwork")

    # Replicate API Request
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "version": "2b017d9b67edd2ee1401238df49d75da53c523f36e363881e057f5dc3ed3c5b2",
        "input": {
            "prompt": prompt,
            "negative_prompt": "",
            "width": 768,
            "height": 768,
            "num_outputs": 1,
            "scheduler": "K_EULER",
            "num_inference_steps": 50,
            "guidance_scale": 7.5,
            "seed": None
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    # Debugging - Log API Response
    print("📥 Replicate API Response:", response.status_code, response.text)

    if response.status_code == 201:
        try:
            json_data = response.json()
            if "urls" in json_data and "get" in json_data["urls"]:
                # Poll for the result
                get_url = json_data["urls"]["get"]
                for _ in range(30):  # Try for 30 seconds
                    result_response = requests.get(
                        get_url,
                        headers={"Authorization": f"Token {REPLICATE_API_KEY}"}
                    )
                    result_data = result_response.json()
                    if result_data["status"] == "succeeded":
                        if result_data["output"] and len(result_data["output"]) > 0:
                            return jsonify({"imageUrl": result_data["output"][0]})
                        break
                    elif result_data["status"] == "failed":
                        return jsonify({"error": "Image generation failed", "details": result_data.get("error", "Unknown error")}), 500
                    time.sleep(1)  # Wait before polling again
                
                return jsonify({"error": "Timeout waiting for image generation"}), 504
            else:
                return jsonify({"error": "Invalid response from Replicate", "response": json_data}), 500
        except Exception as e:
            return jsonify({"error": "Failed to parse API response", "details": str(e)}), 500
    else:
        return jsonify({"error": "AI image generation failed", "details": response.text}), response.status_code

# Ensure Flask Runs Properly
if __name__ == "__main__":
    print("🚀 Using Replicate API for Image Generation")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=True)
