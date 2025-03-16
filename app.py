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
