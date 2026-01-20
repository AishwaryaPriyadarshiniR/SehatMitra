from flask import Flask, render_template, request, jsonify

from symptom_normalizer import normalize_symptoms
from ml_triage_text import predict_level
from disease_predictor import predict_disease
from knowledge_loader import get_precautions, get_description
from llm_helper import make_friendly_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    symptoms = request.form.get("symptoms")

    if not symptoms:
        return jsonify({
            "reply": "Please describe your symptoms.",
            "level": "home-care",
            "remedies": []
        })

    # 🔹 STEP 1: Normalize user text
    normalized_symptoms = normalize_symptoms(symptoms)
    s = normalized_symptoms.lower()

    # 🔹 STEP 2: Predict urgency (ML triage)
    try:
        level = predict_level(normalized_symptoms)
    except Exception as e:
        print("Triage error:", e)
        level = "doctor-soon"   # safe fallback

    # 🔹 STEP 3: Predict disease WITH common-case overrides
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

    # 🔹 STEP 4: Get precautions + description
    remedies = get_precautions(disease)
    description = get_description(disease)

    result = {
        "level": level,
        "message": f"Based on patterns, this resembles: {disease}. {description}",
        "remedies": remedies
    }

    # 🔹 STEP 5: Polish with LLM (optional)
    try:
        polished_reply = make_friendly_response(symptoms, result)
    except Exception as e:
        print("LLM error:", e)
        polished_reply = result["message"]

    return jsonify({
        "reply": polished_reply,
        "level": level,
        "remedies": remedies
    })

if __name__ == "__main__":
    app.run(debug=True)
