import joblib

model = joblib.load("disease_model.pkl")
vectorizer = joblib.load("disease_vectorizer.pkl")

def predict_disease(symptoms: str) -> str:
    X = vectorizer.transform([symptoms])
    return model.predict(X)[0]

