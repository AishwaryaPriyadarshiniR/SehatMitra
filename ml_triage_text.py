import joblib

model = joblib.load("text_triage_model.pkl")
vectorizer = joblib.load("text_vectorizer.pkl")

def predict_level(symptoms: str) -> str:
    X = vectorizer.transform([symptoms])
    return model.predict(X)[0]
