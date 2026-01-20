def normalize_symptoms(text: str) -> str:
    s = text.lower()

    replacements = {
        "skin rash": "skin_rash",
        "rash": "skin_rash",
        "nodal eruptions": "nodal_skin_eruptions",
        "nodal eruption": "nodal_skin_eruptions",
        "itching": "itching",
        "continuous sneezing": "continuous_sneezing",
        "chills": "chills",
        "joint pain": "joint_pain",
        "cough": "cough",
        "cold": "cold",
        "runny nose": "cold"

    }

    for key, val in replacements.items():
        s = s.replace(key, val)

    return s
