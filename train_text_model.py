import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load the text-based triage dataset you created earlier
df = pd.read_csv("text_triage_dataset.csv")

# Ensure columns exist
X = df["symptoms"].astype(str)
y = df["label"]

# Convert text to numerical features
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),      # uses single words + word pairs
    max_features=5000,       # limits vocabulary size
    stop_words="english"     # removes common words like "the", "and"
)

X_vec = vectorizer.fit_transform(X)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

# Train classifier
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# Evaluate model performance
preds = model.predict(X_test)
print("\nModel Performance:\n")
print(classification_report(y_test, preds))

# Save model and vectorizer
joblib.dump(model, "text_triage_model.pkl")
joblib.dump(vectorizer, "text_vectorizer.pkl")

print("\nText triage model trained and saved successfully!")
