from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
from io import BytesIO
from dotenv import load_dotenv
import sys

# Load environment variables from .env file (if any)
load_dotenv()

# Initialize Flask App
app = Flask(__name__)

# Configure CORS to allow requests from our frontend domains
CORS(app, resources={r"/api/*": {"origins": ["https://museevirtuel.netlify.app", "http://localhost:5173", "http://localhost:4173"]}})

# Global variable to store our model pipeline
pipe = None

def check_dependencies():
    """
    Check if all required dependencies are available and compatible
    """
    try:
        import torch
        import numpy as np
        from diffusers import StableDiffusionPipeline
        from PIL import Image
        return True
    except ImportError as e:
        print(f"🚨 Missing dependency: {str(e)}")
        return False
    except Exception as e:
        print(f"🚨 Error checking dependencies: {str(e)}")
        return False

def initialize_model():
    """
    Initialize the Stable Diffusion model.
    This function is called once when the server starts.
    Returns the pipeline object that we'll use for generation.
    """
    global pipe
    try:
        # First check dependencies
        if not check_dependencies():
            print("🚨 Dependencies check failed")
            return False

        import torch
        from diffusers import StableDiffusionPipeline
        
        # Use the base Stable Diffusion 1.5 model
        model_id = "runwayml/stable-diffusion-v1-5"
        
        # Initialize the pipeline with float16 precision if CUDA is available
        if torch.cuda.is_available():
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16,  # Use float16 for better memory efficiency
                safety_checker=None  # Disable safety checker for better performance
            )
            pipe = pipe.to("cuda")  # Move to GPU
            print("✅ Model loaded on GPU with float16 precision")
        else:
            # Fall back to CPU with full precision
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                safety_checker=None
            )
            print("⚠️ GPU not available. Model loaded on CPU (this will be slow)")
        
        # Enable memory efficient attention if available
        if hasattr(pipe, 'enable_attention_slicing'):
            pipe.enable_attention_slicing()
            print("✅ Attention slicing enabled")
            
        return True
    except Exception as e:
        print(f"🚨 Error initializing model: {str(e)}")
        return False

# API Health Check Route
@app.route("/", methods=["GET"])
def home():
    """Simple health check endpoint"""
    return jsonify({"message": "Flask API is running!", "status": "OK"})

@app.route("/api/status", methods=["GET"])
def status():
    """
    Status endpoint that checks if the model is loaded and ready
    """
    global pipe
    try:
        import torch
        return jsonify({
            "status": "healthy",
            "model_loaded": pipe is not None,
            "device": "cuda" if torch.cuda.is_available() else "cpu",
            "message": "Using local Stable Diffusion for AI image generation"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Error checking status"
        }), 500

# AI Image Generation Route
@app.route("/api/generate", methods=["POST"])
def generate_image():
    """
    Main endpoint for generating images.
    Expects a JSON payload with:
    - style: string describing the art style
    - seed: string for reproducible generation
    - timestamp: number for uniqueness
    - randomFactor: number for variation selection
    """
    global pipe
    
    # Check if model is initialized
    if pipe is None:
        print("🚨 Model not initialized!")
        return jsonify({"error": "Model not initialized"}), 500

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

        # Set the random seed if provided
        generator = None
        if seed:
            import torch
            generator = torch.Generator("cuda" if torch.cuda.is_available() else "cpu")
            generator.manual_seed(abs(hash(seed)) % (2**32))

        # Generate the image
        print("🎨 Generating image...")
        image = pipe(
            prompt,
            num_inference_steps=30,  # Reduced for faster generation
            guidance_scale=7.5,  # Standard guidance scale
            negative_prompt="blurry, low quality, distorted, ugly, bad anatomy, frame, border, background, text, watermark",
            generator=generator
        ).images[0]
        
        # Convert the image to base64 for sending to frontend
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        image_url = f"data:image/jpeg;base64,{base64_image}"
        
        print("✅ Image generated successfully")
        return jsonify({
            "imageUrl": image_url,
            "prompt": prompt
        })

    except Exception as e:
        print(f"🚨 Error generating image: {str(e)}")
        return jsonify({
            "error": "Image generation failed",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    print("🚀 Initializing Stable Diffusion model...")
    if initialize_model():
        print("✅ Model initialized successfully")
        # Start the Flask server
        app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=True)
    else:
        print("🚨 Failed to initialize model")
        sys.exit(1)
