# backend/emotion_utils.py
from transformers import pipeline
from config import CRITICAL_PHRASES

text_emotion = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
tone_emotion = pipeline("audio-classification", model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition")

def detect_emotions(transcript, audio_path=None):
    text_result = text_emotion(transcript)[0]
    text_top = max(text_result, key=lambda x: x['score'])

    tone_result = {"label": "neutral", "score": 0}
    if audio_path:
        tone_result = tone_emotion(audio_path)[0]

    return text_top, tone_result

def is_critical(transcript, text_emotion_result):
    return (
        any(p in transcript.lower() for p in CRITICAL_PHRASES) or
        (text_emotion_result['label'].lower() in ['sadness', 'fear', 'depression'] and text_emotion_result['score'] > 0.6)
    )
