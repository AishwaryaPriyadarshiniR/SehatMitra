from flask import Flask, render_template, request, jsonify, session
import os
import re

from symptom_normalizer import normalize_symptoms
from ml_triage_text import predict_level
from disease_predictor import predict_disease
from knowledge_loader import get_precautions, get_description
from llm_helper import make_friendly_response, make_conversational_response

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

HEALTH_KEYWORDS = {
    "pain", "ache", "fever", "cold", "cough", "vomit", "nausea", "diarrhea",
    "loose motion", "headache", "dizzy", "weak", "fatigue", "sore", "throat",
    "breath", "breathing", "chest", "stomach", "abdomen", "infection", "rash",
    "sugar", "bp", "pressure", "period", "cramp", "constipation", "urine",
    "burning", "swelling", "chills", "temperature", "allergy"
}

FOLLOWUP_PHRASES = {
    "what about", "and now", "is that okay", "what should i do", "can i", "should i",
    "same issue", "it got worse", "it is worse", "still same", "same symptoms",
    "what to eat", "any medicine", "next step", "then what"
}


def looks_like_health_query(text):
    t = text.lower().strip()
    if not t:
        return False
    if any(k in t for k in HEALTH_KEYWORDS):
        return True
    return bool(re.search(r"\b\d+\b", t) and re.search(r"\b(day|days|week|weeks|month|months)\b", t))


def looks_like_followup_query(text):
    t = text.lower().strip()
    return any(p in t for p in FOLLOWUP_PHRASES)


def get_history():
    return session.get("chat_history", [])


def push_history(role, content):
    history = get_history()
    history.append({"role": role, "content": content})
    session["chat_history"] = history[-8:]


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    symptoms = request.form.get("symptoms", "").strip()

    if not symptoms:
        return jsonify({
            "reply": "Please describe your symptoms.",
            "level": "home-care",
            "remedies": []
        })

    health_context = session.get("last_health_result")
    is_health_query = looks_like_health_query(symptoms)
    is_followup = looks_like_followup_query(symptoms)

    # Conversational path: small talk and non-symptom messages.
    if not is_health_query:
        history = get_history()
        push_history("user", symptoms)
        try:
            conversational_reply = make_conversational_response(
                symptoms,
                history=history,
                health_context=health_context if is_followup else None,
            )
        except Exception as e:
            print("Conversational LLM error:", e)
            if is_followup and health_context:
                conversational_reply = (
                    "Please continue hydration and rest, and monitor your symptoms closely. "
                    "If pain, fever, or weakness worsens, consult a doctor soon."
                )
            else:
                conversational_reply = (
                    "I can chat with you. If you want health guidance, share your current symptoms "
                    "and how long you've had them."
                )

        push_history("assistant", conversational_reply)
        return jsonify({
            "reply": conversational_reply,
            "level": health_context["level"] if (is_followup and health_context) else None,
            "remedies": health_context["remedies"] if (is_followup and health_context) else []
        })

    # Health path: keep the original triage + disease workflow.
    normalized_symptoms = normalize_symptoms(symptoms)
    s = normalized_symptoms.lower()

    try:
        level = predict_level(normalized_symptoms)
    except Exception as e:
        print("Triage error:", e)
        level = "doctor-soon"

    if "cold" in s or "cough" in s:
        disease = "Common cold"
    elif "loose motion" in s or "diarrhea" in s:
        disease = "Acute diarrhea"
    elif "fever" in s and ("3 day" in s or "three day" in s or "since 3" in s):
        disease = "Prolonged fever"
    else:
        try:
            disease = predict_disease(normalized_symptoms)
        except Exception as e:
            print("Disease model error:", e)
            disease = "Unknown condition"

    remedies = get_precautions(disease)
    description = get_description(disease)

    result = {
        "level": level,
        "message": f"Based on patterns, this resembles: {disease}. {description}",
        "remedies": remedies
    }
    session["last_health_result"] = result

    try:
        polished_reply = make_friendly_response(symptoms, result)
    except Exception as e:
        print("LLM error:", e)
        polished_reply = result["message"]

    push_history("user", symptoms)
    push_history("assistant", polished_reply)

    return jsonify({
        "reply": polished_reply,
        "level": level,
        "remedies": remedies
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
