from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# ✅ Initialize Flask app at the start
app = Flask(__name__)

# ✅ Load environment variables
load_dotenv()
STABILITY_AI_API_KEY = os.getenv("STABILITY_AI_API_KEY")

# ✅ Fix CORS for Netlify
CORS(app, resources={r"/*": {"origins": ["https://museevirtuel.netlify.app", "http://localhost:5173"]}}, supports_credentials=True)

# ✅ Debugging - Print API Key Status
print("✅ Stability AI API Key Loaded:", bool(STABILITY_AI_API_KEY))

# ✅ Debugging - Log API Calls
@app.before_request
def log_request():
    print(f"📥 Incoming Request: {request.method} {request.path}")

# 🔹 API Health Check
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask API is running!", "status": "OK"})

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

    # ✅ Debugging - Log API Response
    print("📥 Stability AI Response:", response.status_code, response.text)

    if response.status_code == 200:
        try:
            json_data = response.json()
            print("✅ AI Generation Response:", json_data)  # Debugging
            if "image" in json_data:
                return jsonify({"imageUrl": json_data["image"]})  # Ensure correct field
            else:
                return jsonify({"error": "No image URL returned from Stability AI", "response": json_data}), 500
        except Exception as e:
            return jsonify({"error": "Failed to parse AI response", "details": str(e)}), 500
    else:
        return jsonify({"error": "AI image generation failed", "details": response.text}), response.status_code

# ✅ Ensure Render Server Works
if __name__ == "__main__":
    print("🚀 Starting Flask Server...")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=True)
