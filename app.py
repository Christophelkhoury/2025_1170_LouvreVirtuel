from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import requests
import time
from dotenv import load_dotenv
import replicate

# Load environment variables from .env file
load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Validate API token format
def is_valid_token(token):
    """Check if the token has the correct format"""
    return token and isinstance(token, str) and len(token) > 20

if not REPLICATE_API_TOKEN:
    print("🚨 Warning: REPLICATE_API_TOKEN is missing!")
    print("Please get your API token from https://replicate.com/account/api-tokens")
elif not is_valid_token(REPLICATE_API_TOKEN):
    print("🚨 Warning: REPLICATE_API_TOKEN format appears invalid!")
    print("Token should be a long string starting with 'r8_'")

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
    Status endpoint that checks if the API token is valid and has remaining credits
    """
    if not REPLICATE_API_TOKEN:
        return jsonify({
            "status": "error",
            "message": "API token missing",
            "details": "Please set REPLICATE_API_TOKEN in your environment variables"
        }), 500

    if not is_valid_token(REPLICATE_API_TOKEN):
        return jsonify({
            "status": "error",
            "message": "Invalid API token format",
            "details": "Token should be a long string starting with 'r8_'"
        }), 500

    try:
        # Test the API token with a simple model query
        response = requests.get(
            "https://api.replicate.com/v1/models",
            headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"}
        )
        
        if response.status_code == 200:
            # Check remaining credits
            credits_response = requests.get(
                "https://api.replicate.com/v1/credits",
                headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"}
            )
            
            if credits_response.status_code == 200:
                credits_data = credits_response.json()
                remaining_seconds = credits_data.get("remaining_seconds", 0)
                api_status = "valid"
            else:
                remaining_seconds = None
                api_status = f"valid but can't check credits (status: {credits_response.status_code})"
        else:
            api_status = f"invalid (status: {response.status_code})"
            remaining_seconds = None

    except Exception as e:
        api_status = f"error ({str(e)})"
        remaining_seconds = None

    return jsonify({
        "status": "healthy",
        "api_status": api_status,
        "remaining_seconds": remaining_seconds,
        "message": "Using Replicate API for AI image generation"
    })

# AI Image Generation Route
@app.route("/api/generate", methods=["POST"])
def generate_image():
    """
    Main endpoint for generating images using Replicate API.
    Expects a JSON payload with:
    - style: string describing the art style
    - seed: string for reproducible generation
    - timestamp: number for uniqueness
    - randomFactor: number for variation selection
    """
    if not REPLICATE_API_TOKEN:
        print("🚨 API Token MISSING!")
        return jsonify({"error": "API token missing"}), 401

    if not is_valid_token(REPLICATE_API_TOKEN):
        print("🚨 Invalid API Token format!")
        return jsonify({"error": "Invalid API token format"}), 401

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

        # Generate image using Replicate API
        print("🎨 Generating image...")
        start_time = time.time()
        
        output = replicate.run(
            "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
            input={
                "prompt": prompt,
                "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy, frame, border, background, text, watermark",
                "num_inference_steps": 30,
                "guidance_scale": 7.5,
                "seed": abs(hash(seed)) % (2**32) if seed else None
            }
        )

        generation_time = time.time() - start_time
        print(f"⏱️ Generation took {generation_time:.2f} seconds")

        # Get the image URL from the output
        image_url = output[0]
        
        # Download the image and convert to base64
        response = requests.get(image_url)
        if response.status_code == 200:
            base64_image = base64.b64encode(response.content).decode('utf-8')
            image_url = f"data:image/jpeg;base64,{base64_image}"
            
            print("✅ Image generated successfully")
            return jsonify({
                "imageUrl": image_url,
                "prompt": prompt,
                "generationTime": f"{generation_time:.2f}s"
            })
        else:
            raise Exception(f"Failed to download image: {response.status_code}")

    except Exception as e:
        print(f"🚨 Error generating image: {str(e)}")
        return jsonify({
            "error": "Image generation failed",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    print("🚀 Using Replicate API for AI Image Generation")
    print(f"🔑 API Token Status: {'Valid' if REPLICATE_API_TOKEN and is_valid_token(REPLICATE_API_TOKEN) else 'Invalid'}")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=True)
