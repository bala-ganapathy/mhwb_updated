# backend/firebase_utils.py
import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from config import FIREBASE_CREDENTIAL_PATH

cred = credentials.Certificate(FIREBASE_CREDENTIAL_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

def generate_unique_user_id():
    docs = db.collection("conversations").stream()
    existing_ids = [doc.id for doc in docs]
    index = 1
    while True:
        new_id = f"user-{index:03d}"
        if new_id not in existing_ids:
            return new_id
        index += 1

def create_user(user_id):
    db.collection("conversations").document(user_id).set({
        "created_at": datetime.datetime.utcnow()
    })

def user_exists(user_id):
    doc = db.collection("conversations").document(user_id).get()
    return doc.exists

def save_message(user_id, transcript, text_emotion, tone_emotion, gpt_response):
    db.collection("conversations").document(user_id).collection("messages").add({
        "input_text": transcript,
        "text_emotion": text_emotion,
        "tone_emotion": tone_emotion,
        "gpt_response": gpt_response,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

def get_recent_messages(user_id, limit=5):
    docs = db.collection("conversations").document(user_id).collection("messages")\
        .order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit).stream()
    messages = []
    for doc in reversed(list(docs)):
        data = doc.to_dict()
        messages.append({"role": "user", "content": data.get("input_text", "")})
        messages.append({"role": "assistant", "content": data.get("gpt_response", "")})
    return messages
