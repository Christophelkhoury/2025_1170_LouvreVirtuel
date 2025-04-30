from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import requests
import time

# CHANGED: Switched from Hugging Face to Stability AI API
# Get API key directly from environment variables
STABLE_DIFFUSION_API_KEY = os.environ.get("STABILITY_API_KEY")

# CHANGED: Added debug logging for environment variables
print("🔍 Environment Variables Check:")
print(f"STABILITY_API_KEY exists: {'Yes' if STABLE_DIFFUSION_API_KEY else 'No'}")
if STABLE_DIFFUSION_API_KEY:
    print(f"STABILITY_API_KEY length: {len(STABLE_DIFFUSION_API_KEY)}")

# CHANGED: Added token validation function
def is_valid_token(token):
    """Check if the token has the correct format"""
    return (token and 
            isinstance(token, str) and 
            len(token) > 20)  # Stability AI tokens are longer than 20 chars

# CHANGED: Added API key validation checks
if not STABLE_DIFFUSION_API_KEY:
    print("🚨 Warning: STABILITY_API_KEY is missing!")
    print("Please set STABILITY_API_KEY in Render environment variables")
elif not is_valid_token(STABLE_DIFFUSION_API_KEY):
    print("🚨 Warning: STABILITY_API_KEY format appears invalid!")
    print(f"Token length: {len(STABLE_DIFFUSION_API_KEY)}")

# Initialize Flask App
app = Flask(__name__)

# CHANGED: Updated CORS configuration to allow Netlify domain
CORS(app, resources={r"/api/*": {"origins": ["https://museevirtuel.netlify.app", "http://localhost:5173", "http://localhost:4173"]}})

# CHANGED: Added basic health check endpoint
@app.route("/", methods=["GET"])
def home():
    """Simple health check endpoint"""
    return jsonify({"message": "Flask API is running!", "status": "OK"})

# CHANGED: Added detailed status endpoint
@app.route("/api/status", methods=["GET"])
def status():
    """
    Status endpoint that checks if the API token is valid
    """
    if not STABLE_DIFFUSION_API_KEY:
        return jsonify({
            "status": "error",
            "message": "API key missing",
            "details": "Please set STABILITY_API_KEY in Render environment variables"
        }), 500

    if not is_valid_token(STABLE_DIFFUSION_API_KEY):
        return jsonify({
            "status": "error",
            "message": "Invalid API key format"
        }), 500

    return jsonify({
        "status": "healthy",
        "api_status": "valid",
        "message": "Using Stability AI API for image generation"
    })

# CHANGED: Updated image generation endpoint for Stability AI
@app.route("/api/generate", methods=["POST"])
def generate_image():
    """
    Main endpoint for generating images using Stability AI API.
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
        
        # CHANGED: Improved prompt generation
        base_prompt = f"A masterpiece painting in the style of {style}, highly detailed, artistic, professional quality"
        
        # CHANGED: Added variations for more unique generations
        variations = [
            "with dramatic lighting",
            "with vibrant colors",
            "with subtle tones",
            "with bold composition",
            "with intricate details",
            "with atmospheric effects"
        ]
        
        variation_index = random_factor % len(variations)
        prompt = f"{base_prompt}, {variations[variation_index]}, no frame, no border, no background, pure artwork"
        
        print(f"📝 Generated prompt: {prompt}")

        # CHANGED: Added timing for performance monitoring
        print("🎨 Generating image...")
        start_time = time.time()
        
        # CHANGED: Updated API endpoint and parameters for Stability AI
        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {STABLE_DIFFUSION_API_KEY}"
            },
            json={
                "text_prompts": [
                    {
                        "text": prompt,
                        "weight": 1
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
                "seed": abs(hash(seed)) % (2**32) if seed else None
            }
        )
        
        # CHANGED: Added detailed error logging
        print(f"🔍 API response status: {response.status_code}")
        print(f"🔍 API response: {response.text}")
        
        if response.status_code != 200:
            raise Exception(f"Failed to generate image: {response.text}")

        data = response.json()
        
        if not data.get("artifacts") or not data["artifacts"][0] or not data["artifacts"][0].get("base64"):
            print("🔍 Full response data:", data)
            raise Exception("No image data in response. Response format: " + str(data))

        image_url = f"data:image/png;base64,{data['artifacts'][0]['base64']}"
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
    # CHANGED: Added startup logging
    print("🚀 Using Stability AI API for AI Image Generation")
    print(f"🔑 API Key Status: {'Valid' if STABLE_DIFFUSION_API_KEY and is_valid_token(STABLE_DIFFUSION_API_KEY) else 'Invalid'}")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=True)
