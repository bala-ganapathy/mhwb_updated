# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_utils import *
from emotion_utils import detect_emotions, is_critical
from gpt_utils import generate_response

app = Flask(__name__)
CORS(app)

@app.route("/api/login", methods=["POST"])
def login_user():
    data = request.get_json()
    is_new = data.get("new")
    if is_new:
        new_id = generate_unique_user_id()
        create_user(new_id)
        return jsonify({"user_id": new_id})
    else:
        uid = data.get("user_id", "")
        if user_exists(uid):
            return jsonify({"user_id": uid})
        return jsonify({"error": "User not found"}), 404

@app.route("/api/message", methods=["POST"])
def handle_message():
    data = request.get_json()
    user_id = data["user_id"]
    input_text = data["message"]
    audio_path = None  # You can later extend to include audio upload

    # Emotion detection
    text_emotion, tone_emotion = detect_emotions(input_text, audio_path)

    # Fetch past messages
    history = get_recent_messages(user_id)

    # Generate GPT reply
    reply = generate_response(text_emotion['label'], input_text, history)

    # Save session
    save_message(user_id, input_text, text_emotion, tone_emotion, reply)

    return jsonify({
        "response": reply,
        "text_emotion": text_emotion,
        "tone_emotion": tone_emotion
    })

if __name__ == "__main__":
    app.run(debug=True)
