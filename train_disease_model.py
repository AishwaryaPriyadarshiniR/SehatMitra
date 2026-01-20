import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# ✅ IMPORTANT FIX: use comma, not tab
df = pd.read_csv("dataset.csv", sep=",")

# Clean any accidental spaces in column names
df.columns = df.columns.str.strip()

print("Fixed columns:", list(df.columns))

# Collect all symptom columns dynamically
symptom_cols = [c for c in df.columns if c.lower().startswith("symptom")]

# Combine all symptoms into one text field
df["all_symptoms"] = df[symptom_cols].apply(
    lambda row: " ".join(
        [str(x).strip() for x in row if isinstance(x, str) and x.strip() != ""]
    ),
    axis=1
)

X = df["all_symptoms"]
y = df["Disease"]   # now this WILL exist

# Text vectorization
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
X_vec = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression(max_iter=300)
model.fit(X_vec, y)

# Save artifacts
joblib.dump(model, "disease_model.pkl")
joblib.dump(vectorizer, "disease_vectorizer.pkl")

print("Disease model trained and saved successfully!")
