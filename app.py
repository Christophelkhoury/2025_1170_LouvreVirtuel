from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import requests
import time

# Get API key directly from environment variables
STABLE_DIFFUSION_API_KEY = os.environ.get("MODELSLAB_API_KEY")

# Debug logging for environment variables
print("🔍 Environment Variables Check:")
print(f"MODELSLAB_API_KEY exists: {'Yes' if STABLE_DIFFUSION_API_KEY else 'No'}")
if STABLE_DIFFUSION_API_KEY:
    print(f"MODELSLAB_API_KEY length: {len(STABLE_DIFFUSION_API_KEY)}")

# Validate API token format
def is_valid_token(token):
    """Check if the token has the correct format"""
    return (token and 
            isinstance(token, str) and 
            len(token) > 20)  # ModelsLab tokens are longer than 20 chars

if not STABLE_DIFFUSION_API_KEY:
    print("🚨 Warning: MODELSLAB_API_KEY is missing!")
    print("Please set MODELSLAB_API_KEY in Render environment variables")
elif not is_valid_token(STABLE_DIFFUSION_API_KEY):
    print("🚨 Warning: MODELSLAB_API_KEY format appears invalid!")
    print(f"Token length: {len(STABLE_DIFFUSION_API_KEY)}")

# Initialize Flask App
app = Flask(__name__)

# Configure CORS to allow requests from our frontend domains
CORS(app, resources={r"/api/*": {"origins": ["https://museevirtuel.netlify.app", "http://localhost:5173", "http://localhost:4173"]}})

# API Health Check Route
@app.route("/", methods=["GET"])
def home():
    """Simple health check endpoint"""
    return jsonify({"message": "Flask API is running!", "status": "OK"})

@app.route("/api/status", methods=["GET"])
def status():
    """
    Status endpoint that checks if the API token is valid
    """
    if not STABLE_DIFFUSION_API_KEY:
        return jsonify({
            "status": "error",
            "message": "API key missing",
            "details": "Please set MODELSLAB_API_KEY in Render environment variables"
        }), 500

    if not is_valid_token(STABLE_DIFFUSION_API_KEY):
        return jsonify({
            "status": "error",
            "message": "Invalid API key format"
        }), 500

    return jsonify({
        "status": "healthy",
        "api_status": "valid",
        "message": "Using ModelsLab API for AI image generation"
    })

# AI Image Generation Route
@app.route("/api/generate", methods=["POST"])
def generate_image():
    """
    Main endpoint for generating images using ModelsLab API.
    Expects a JSON payload with:
    - style: string describing the art style
    - seed: string for reproducible generation
    - timestamp: number for uniqueness
    - randomFactor: number for variation selection
    """
    if not STABLE_DIFFUSION_API_KEY:
        print("🚨 API Key MISSING!")
        return jsonify({"error": "API key missing"}), 401

    if not is_valid_token(STABLE_DIFFUSION_API_KEY):
        print("🚨 Invalid API Key format!")
        return jsonify({"error": "Invalid API key format"}), 401

    try:
        # Extract parameters from request
        data = request.json
        style = data.get("style", "")
        seed = data.get("seed", "")
        timestamp = data.get("timestamp", 0)
        random_factor = data.get("randomFactor", 0)
        
        print(f"🎲 Received parameters: seed={seed}, timestamp={timestamp}, factor={random_factor}")
        
        # Create base prompt describing the artwork
        base_prompt = f"A masterpiece painting in the style of {style}, highly detailed, artistic, professional quality"
        
        # List of possible variations to make each generation unique
        variations = [
            "with dramatic lighting",
            "with vibrant colors",
            "with subtle tones",
            "with bold composition",
            "with intricate details",
            "with atmospheric effects"
        ]
        
        # Select a variation based on the random factor
        variation_index = random_factor % len(variations)
        prompt = f"{base_prompt}, {variations[variation_index]}, no frame, no border, no background, pure artwork"
        
        print(f"📝 Generated prompt: {prompt}")

        # Generate image using ModelsLab API
        print("🎨 Generating image...")
        start_time = time.time()
        
        # Make request to ModelsLab API
        response = requests.post(
            "https://modelslab.com/api/v1/stability/text2img",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {STABLE_DIFFUSION_API_KEY}"
            },
            json={
                "prompt": prompt,
                "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy, frame, border, background, text, watermark",
                "width": 1024,
                "height": 1024,
                "samples": 1,
                "num_inference_steps": 30,
                "seed": abs(hash(seed)) % (2**32) if seed else None,
                "guidance_scale": 7.5,
                "safety_checker": True,
                "model": "stable-diffusion-xl-1024-v1-0"
            }
        )
        
        print(f"🔍 API response status: {response.status_code}")
        print(f"🔍 API response: {response.text}")
        
        if response.status_code != 200:
            raise Exception(f"Failed to generate image: {response.text}")

        data = response.json()
        
        if not data.get("output") or not data["output"][0]:
            raise Exception("No image data in response")

        image_url = data["output"][0]
        generation_time = time.time() - start_time
        print(f"⏱️ Generation took {generation_time:.2f} seconds")
            
        print("✅ Image generated successfully")
        return jsonify({
            "imageUrl": image_url,
            "prompt": prompt,
            "generationTime": f"{generation_time:.2f}s"
        })

    except Exception as e:
        print(f"🚨 Error generating image: {str(e)}")
        return jsonify({
            "error": "Image generation failed",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    print("🚀 Using ModelsLab API for AI Image Generation")
    print(f"🔑 API Key Status: {'Valid' if STABLE_DIFFUSION_API_KEY and is_valid_token(STABLE_DIFFUSION_API_KEY) else 'Invalid'}")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=True)
