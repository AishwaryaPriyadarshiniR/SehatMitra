import pandas as pd

precautions_df = pd.read_csv("symptom_precaution.csv", sep=",")
desc_df = pd.read_csv("symptom_Description.csv", sep=",")

def get_precautions(disease):
    row = precautions_df[precautions_df["Disease"] == disease]

    if not row.empty:
        r = row.iloc[0]
        return [
            r["Precaution_1"],
            r["Precaution_2"],
            r["Precaution_3"],
            r["Precaution_4"]
        ]

    # ---- FALLBACK REMEDIES FOR COMMON CASES ----
    if disease == "Common cold":
        return [
            "Drink warm fluids",
            "Steam inhalation",
            "Rest well",
            "Avoid cold drinks"
        ]

    if disease == "Acute diarrhea":
        return [
            "Take ORS frequently",
            "Eat light food (curd rice, bananas)",
            "Avoid spicy/oily food",
            "Drink plenty of water"
        ]

    if disease == "Prolonged fever":
        return [
            "Drink plenty of fluids",
            "Take paracetamol if needed (as per label)",
            "Rest and monitor temperature",
            "Consult a doctor soon"
        ]

    return []

def get_description(disease):
    row = desc_df[desc_df["Disease"] == disease]
    if row.empty:
        return ""
    return row.iloc[0]["Description"]
