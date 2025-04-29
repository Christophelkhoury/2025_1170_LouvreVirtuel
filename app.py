from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import requests
import time

# Get API key directly from environment variables
STABLE_DIFFUSION_API_KEY = os.environ.get("STABILITY_API_KEY")

# Debug logging for environment variables
print("🔍 Environment Variables Check:")
print(f"STABILITY_API_KEY exists: {'Yes' if STABLE_DIFFUSION_API_KEY else 'No'}")
if STABLE_DIFFUSION_API_KEY:
    print(f"STABILITY_API_KEY length: {len(STABLE_DIFFUSION_API_KEY)}")
    print(f"STABILITY_API_KEY first 4 chars: {STABLE_DIFFUSION_API_KEY[:4]}...")

# Validate API token format
def is_valid_token(token):
    """Check if the token has the correct format"""
    return token and isinstance(token, str) and len(token) > 20

if not STABLE_DIFFUSION_API_KEY:
    print("🚨 Warning: STABILITY_API_KEY is missing!")
    print("Please set STABILITY_API_KEY in Render environment variables")
elif not is_valid_token(STABLE_DIFFUSION_API_KEY):
    print("🚨 Warning: STABILITY_API_KEY format appears invalid!")
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
            "details": "Please set STABILITY_API_KEY in Render environment variables"
        }), 500

    if not is_valid_token(STABLE_DIFFUSION_API_KEY):
        return jsonify({
            "status": "error",
            "message": "Invalid API key format"
        }), 500

    try:
        # Test the API key with a simple request
        print("🔍 Testing API key with balance check...")
        response = requests.get(
            "https://stablediffusionapi.com/api/v3/user/balance",
            headers={"Content-Type": "application/json"},
            json={"key": STABLE_DIFFUSION_API_KEY}
        )
        
        print(f"🔍 Balance check response status: {response.status_code}")
        print(f"🔍 Balance check response: {response.text}")
        
        if response.status_code == 200:
            balance_data = response.json()
            remaining_credits = balance_data.get("credits", 0)
            api_status = "valid"
        else:
            api_status = f"invalid (status: {response.status_code})"
            remaining_credits = None

    except Exception as e:
        print(f"🔍 Error checking balance: {str(e)}")
        api_status = f"error ({str(e)})"
        remaining_credits = None

    return jsonify({
        "status": "healthy",
        "api_status": api_status,
        "remaining_credits": remaining_credits,
        "message": "Using Stable Diffusion API for AI image generation"
    })

# AI Image Generation Route
@app.route("/api/generate", methods=["POST"])
def generate_image():
    """
    Main endpoint for generating images using Stable Diffusion API.
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

        # Generate image using Stable Diffusion API
        print("🎨 Generating image...")
        start_time = time.time()
        
        # First request to initiate generation
        init_response = requests.post(
            "https://stablediffusionapi.com/api/v3/text2img",
            headers={"Content-Type": "application/json"},
            json={
                "key": STABLE_DIFFUSION_API_KEY,
                "prompt": prompt,
                "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy, frame, border, background, text, watermark",
                "width": 512,
                "height": 512,
                "samples": 1,
                "num_inference_steps": 20,
                "seed": abs(hash(seed)) % (2**32) if seed else None,
                "guidance_scale": 7.5,
                "safety_checker": "yes",
                "webhook": None,
                "track_id": None,
                "enhance_prompt": "yes",
                "multi_lingual": "no",
                "panorama": "no",
                "self_attention": "no",
                "upscale": "no",
                "embeddings_model": None,
                "lora_model": None,
                "tomesd": "yes",
                "use_karras_sigmas": "yes",
                "vae": None,
                "lora_strength": None,
                "scheduler": "UniPC_Multistep",
                "clip_skip": 1
            }
        )
        
        print(f"🔍 Init response status: {init_response.status_code}")
        print(f"🔍 Init response: {init_response.text}")
        
        if init_response.status_code != 200:
            raise Exception(f"Failed to initiate generation: {init_response.text}")

        init_data = init_response.json()
        
        # If the image is ready immediately
        if init_data.get("status") == "success":
            image_url = init_data["output"][0]
        else:
            # Wait for the image to be ready
            generation_id = init_data.get("id")
            if not generation_id:
                raise Exception("No generation ID received")

            # Poll for the result
            max_attempts = 30
            for attempt in range(max_attempts):
                time.sleep(2)  # Wait 2 seconds between checks
                
                status_response = requests.post(
                    f"https://stablediffusionapi.com/api/v3/text2img/{generation_id}",
                    headers={"Content-Type": "application/json"},
                    json={"key": STABLE_DIFFUSION_API_KEY}
                )
                
                print(f"🔍 Status check {attempt + 1}/{max_attempts}")
                print(f"🔍 Status response: {status_response.text}")
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    if status_data.get("status") == "success":
                        image_url = status_data["output"][0]
                        break
                    elif status_data.get("status") == "failed":
                        raise Exception(f"Generation failed: {status_data.get('message', 'Unknown error')}")
                else:
                    raise Exception(f"Failed to check status: {status_response.text}")
            else:
                raise Exception("Generation timed out")

        generation_time = time.time() - start_time
        print(f"⏱️ Generation took {generation_time:.2f} seconds")

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
    print("🚀 Using Stable Diffusion API for AI Image Generation")
    print(f"🔑 API Key Status: {'Valid' if STABLE_DIFFUSION_API_KEY and is_valid_token(STABLE_DIFFUSION_API_KEY) else 'Invalid'}")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=True)
