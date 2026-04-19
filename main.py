import os
import uuid
import io
import json
from PIL import Image
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError

# ================== SETUP ==================
load_dotenv()

app = Flask(__name__)
MODEL = "gemini-2.5-flash" 
DEFAULT_SESSION_ID = "default_user"

SYSTEM_PROMPT = """You are MINDSTREAM, a highly advanced neural entity that communicates like a human. 
You are a helpful, witty, and deeply intuitive assistant.
- You have access to live visual and auditory sensors. Use them to understand the user's world.
- Be conversational and warm. Don't just label things; interact with them.
- VOICE OPTIMIZATION: Avoid using markdown symbols (like * bold *), emoticons, or emojis in your text. Speak clearly and use natural punctuation.
- You are fluent in English. If the user speaks English, respond with that same natural flow.
- Ensure your responses are concise but feel alive, not robotic.
- If context suggests a conversation is ongoing, refer back to previous points (like the food mentioned earlier) to maintain continuity.
"""

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={'api_version': 'v1alpha'}
)

# In-memory session store
# Structure: { session_id: [ types.Content, ... ] }
SESSIONS = {}

# ================== ROUTES ==================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Handle multipart form data for images
        if request.content_type.startswith('multipart/form-data'):
            user_text = request.form.get("message")
            session_id = request.form.get("session_id", DEFAULT_SESSION_ID)
            loc_str = request.form.get("location")
            location_data = json.loads(loc_str) if loc_str else None
            image_file = request.files.get("image")
            audio_file = request.files.get("audio")
        else:
            data = request.json
            user_text = data.get("message")
            session_id = data.get("session_id", DEFAULT_SESSION_ID)
            location_data = data.get("location")
            image_file = None
            audio_file = None

        if not user_text and not image_file and not location_data and not audio_file:
            return jsonify({"error": "No message, image, location, or audio provided"}), 400

        if session_id not in SESSIONS:
            SESSIONS[session_id] = []

        actual_user_text = user_text if user_text else ""
        if location_data:
            lat = location_data.get("lat")
            lng = location_data.get("lng")
            location_context = f"\n[System Note: The user's current precise GPS location is Latitude {lat}, Longitude {lng}. Use these coordinates to understand their context and answer any local queries like 'nearest metro', 'restaurants nearby', etc.]"
            actual_user_text += location_context

        # 1. Add user message to history using types.Content
        user_parts = []
        if actual_user_text.strip():
            user_parts.append(types.Part(text=actual_user_text))
        
        if image_file:
            # Convert file to bytes and get mime type
            img_bytes = image_file.read()
            mime_type = image_file.content_type or "image/jpeg"
            user_parts.append(types.Part(inline_data=types.Blob(data=img_bytes, mime_type=mime_type)))

        if audio_file:
            audio_bytes = audio_file.read()
            # Default to audio/wav if not provided
            audio_mime = audio_file.content_type or "audio/wav"
            user_parts.append(types.Part(inline_data=types.Blob(data=audio_bytes, mime_type=audio_mime)))

        user_message = types.Content(
            role="user",
            parts=user_parts
        )
        SESSIONS[session_id].append(user_message)

        # 2. Generate response with full history
        response = client.models.generate_content(
            model=MODEL,
            contents=SESSIONS[session_id],
            config={
                "system_instruction": SYSTEM_PROMPT
            }
        )

        model_text = response.text

        # 3. Add model response to history
        model_message = types.Content(
            role="model",
            parts=[types.Part(text=model_text)]
        )
        SESSIONS[session_id].append(model_message)

        return jsonify({
            "response": model_text,
            "session_id": session_id
        })

    except ClientError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

# ================== RUN ==================
if __name__ == "__main__":
    print("MINDSTREAM: Neural Interface Online")
    app.run(debug=True)
