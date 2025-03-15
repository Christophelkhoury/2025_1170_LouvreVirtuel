import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env file
dotenv_path = Path(__file__).resolve().parent / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    print("⚠️ .env file not found, relying on system environment variables.")

# Initialize Flask app
app = Flask(__name__)

# Configure CORS to allow Netlify and localhost
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Load API Key
STABILITY_AI_API_KEY = os.getenv("STABILITY_AI_API_KEY")

# Check if API Key is loaded
if not STABILITY_AI_API_KEY:
    print("⚠️ STABILITY_AI_API_KEY is missing! Check Render environment variables.")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "healthy",
        "api_key_configured": bool(STABILITY_AI_API_KEY),
        "message": "AI Art Generator API is running."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=False)
