import pandas as pd

# Load Kaggle disease–symptom dataset
df = pd.read_csv("dataset.csv", sep=",")

# Clean column names (important)
df.columns = df.columns.str.strip()

# Collect all symptom columns
symptom_cols = [c for c in df.columns if c.lower().startswith("symptom")]

rows = []

for _, row in df.iterrows():
    disease = row["Disease"]

    # Combine all symptoms into one text string
    symptoms = []
    for col in symptom_cols:
        if isinstance(row[col], str) and row[col].strip() != "":
            symptoms.append(row[col].strip())

    symptom_text = ", ".join(symptoms)

    # Simple, explainable mapping from disease → urgency label
    if disease in [
        "Heart attack", "Pneumonia", "Tuberculosis", "Malaria", "Dengue"
    ]:
        label = "emergency"
    elif disease in [
        "Typhoid", "Hepatitis", "Jaundice", "Migraine", "Hypertension"
    ]:
        label = "doctor-soon"
    else:
        label = "home-care"

    rows.append({"symptoms": symptom_text, "label": label})

# Create and save new dataset
new_df = pd.DataFrame(rows)
new_df.to_csv("text_triage_dataset.csv", index=False)

print("Created text_triage_dataset.csv successfully!")
