from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import base64
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    print("🚨 Warning: HUGGINGFACE_API_KEY is missing!")
elif not HUGGINGFACE_API_KEY.startswith("hf_"):
    print("🚨 Warning: HUGGINGFACE_API_KEY format appears invalid!")

# Initialize Flask App
app = Flask(__name__)

# Fix CORS for development and production
CORS(app, resources={r"/api/*": {"origins": ["https://museevirtuel.netlify.app", "http://localhost:5173", "http://localhost:4173"]}})

# API Health Check Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask API is running!", "status": "OK"})

@app.route("/api/status", methods=["GET"])
def status():
    # Test the API key with a simple model query
    if HUGGINGFACE_API_KEY:
        try:
            test_response = requests.get(
                "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
                headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
            )
            api_status = "valid" if test_response.status_code == 200 else f"invalid (status: {test_response.status_code})"
        except Exception as e:
            api_status = f"error ({str(e)})"
    else:
        api_status = "missing"

    return jsonify({
        "status": "healthy",
        "api_key_status": api_status,
        "api_key_format": "valid" if HUGGINGFACE_API_KEY and HUGGINGFACE_API_KEY.startswith("hf_") else "invalid",
        "message": "Using Hugging Face API for AI image generation."
    })

# AI Image Generation Route
@app.route("/api/generate", methods=["POST"])
def generate_image():
    if not HUGGINGFACE_API_KEY:
        print("🚨 API Key MISSING in Flask!")
        return jsonify({"error": "API key missing"}), 401

    if not HUGGINGFACE_API_KEY.startswith("hf_"):
        print("🚨 Invalid API Key format!")
        return jsonify({"error": "Invalid API key format"}), 401

    print(f"✅ Using API Key: {HUGGINGFACE_API_KEY[:6]}**********")

    data = request.json
    style = data.get("style", "")
    seed = data.get("seed", "")
    timestamp = data.get("timestamp", 0)
    random_factor = data.get("randomFactor", 0)
    
    print(f"🎲 Received randomization parameters: seed={seed}, timestamp={timestamp}, factor={random_factor}")
    
    # Create a more detailed prompt with randomization
    base_prompt = f"A masterpiece painting in the style of {style}, highly detailed, artistic, professional quality"
    variations = [
        "with dramatic lighting",
        "with vibrant colors",
        "with subtle tones",
        "with bold composition",
        "with intricate details",
        "with atmospheric effects"
    ]
    
    # Use the random factor to select a variation
    variation_index = random_factor % len(variations)
    prompt = f"{base_prompt}, {variations[variation_index]}, no frame, no border, no background, pure artwork"
    
    print(f"📝 Generated prompt: {prompt}")

    # Using a more reliable model for art generation
    url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "num_inference_steps": 30,  # Reduced for faster generation
            "guidance_scale": 7.5,
            "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy, frame, border, background, text, watermark",
            "seed": abs(hash(seed)) % (2**32) if seed else None  # Convert string seed to numerical
        }
    }

    print("📤 Sending request to Hugging Face API...")
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"📥 Hugging Face API Response Status: {response.status_code}")
        print(f"📥 Hugging Face API Response Headers: {dict(response.headers)}")
        print(f"📥 Hugging Face API Response Body: {response.text[:200]}...")

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
    print(f"🔑 API Key Status: {'Valid format' if HUGGINGFACE_API_KEY and HUGGINGFACE_API_KEY.startswith('hf_') else 'Invalid format'}")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=True)
