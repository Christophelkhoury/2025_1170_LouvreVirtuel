import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS to allow Netlify domains
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "https://*.netlify.app",  # Allow all Netlify subdomains
            "https://*.netlify.com"   # Allow all Netlify domains
        ],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Constants
STABILITY_API_KEY = os.getenv('STABILITY_AI_API_KEY')
API_ENDPOINT = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

@app.before_request
def verify_api_key():
    """Verify API key is present before processing requests"""
    if request.path.startswith('/api/'):
        if not STABILITY_AI_API_KEY:
            return jsonify({
                'error': 'API Configuration Error',
                'details': 'Stability AI API key is not configured'
            }), 500

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint with enhanced status information"""
    return jsonify({
        "status": "healthy",
        "message": "AI Art Generator API is running",
        "config": {
            "api_key_configured": bool(STABILITY_AI_API_KEY),
            "cors_enabled": True,
            "allowed_origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "https://*.netlify.app",
                "https://*.netlify.com"
            ]
        }
    })

@app.route("/api/generate", methods=["POST"])
def generate_image():
    """Generate image using Stability AI API with enhanced error handling"""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'error': 'Invalid request',
                'details': 'Request must be JSON'
            }), 400

        # Get style from request
        data = request.json
        if 'style' not in data:
            return jsonify({
                'error': 'Missing parameter',
                'details': 'Style parameter is required'
            }), 400

        style = data['style']
        
        # Log request details
        print(f"Generating image for style: {style}")
        
        # Prepare request
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {STABILITY_AI_API_KEY}"
        }
        
        payload = {
            "prompt": f"Create a {style} style painting. The image should be highly detailed and artistic, following the characteristics of {style} art movement.",
            "output_format": "jpeg"
        }

        # Make API request with timeout
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=30
        )

        # Log response status
        print(f"Stability AI API Response Status: {response.status_code}")

        # Handle successful response
        if response.status_code == 200:
            result = response.json()
            if "image_url" not in result:
                print("Error: Response missing image_url")
                return jsonify({
                    'error': 'Invalid API response',
                    'details': 'Response did not contain image URL'
                }), 502

            return jsonify({
                "imageUrl": result["image_url"],
                "prompt": f"{style} style painting"
            })
        
        # Handle API error with detailed logging
        try:
            error_data = response.json()
            error_message = error_data.get('message', response.text)
            print(f"API Error: {error_message}")
        except ValueError:
            error_message = response.text
            print(f"Failed to parse error response: {error_message}")

        return jsonify({
            "error": "Stability AI API Error",
            "details": error_message,
            "status_code": response.status_code
        }), response.status_code

    except requests.Timeout:
        print("Request timeout error")
        return jsonify({
            "error": "Request timeout",
            "details": "The API request timed out after 30 seconds"
        }), 504

    except requests.ConnectionError:
        print("Connection error to Stability AI API")
        return jsonify({
            "error": "Connection error",
            "details": "Failed to connect to Stability AI API"
        }), 503

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({
            "error": "Server error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    # Verify environment variables before starting
    if not STABILITY_AI_API_KEY:
        print("ERROR: STABILITY_AI_API_KEY environment variable is not set")
        print("Please ensure you have a .env file with the required API key")
        exit(1)

    # Start server with enhanced logging
    port = int(os.getenv('PORT', 3001))
    print(f"Starting server on port {port}")
    print(f"API Key configured: {bool(STABILITY_AI_API_KEY)}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # Disable debug mode in production
    )