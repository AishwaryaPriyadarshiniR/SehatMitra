def triage(age, symptoms):
    s = symptoms.lower()
    age = int(age) if age and age.isdigit() else None

    # ---------------- RED FLAGS (EMERGENCY) ----------------
    if any(word in s for word in [
        "chest pain", "breath", "unconscious",
        "severe bleeding", "stroke", "poison",
        "can't breathe", "cannot breathe", "faint"
    ]):
        return {
            "level": "emergency",
            "message": (
                "🚨 <strong>This may be a medical emergency.</strong><br>"
                "Please go to the nearest emergency department or call local emergency services immediately."
            ),
            "remedies": []
        }

    # Severe dehydration signs
    if "no urine" in s or "not peeing" in s or "very weak" in s:
        return {
            "level": "emergency",
            "message": (
                "🚨 <strong>Possible severe dehydration.</strong><br>"
                "Please seek medical care immediately."
            ),
            "remedies": []
        }

    # ---------------- FEVER CASES ----------------

    # Fever lasting 3+ days
    if "fever" in s and ("3 day" in s or "three day" in s or "for 3" in s or "since 3" in s):
        return {
            "level": "doctor-soon",
            "message": (
                "🤒 <strong>You’ve had fever for 3 days — this needs medical attention.</strong><br>"
                "It could be viral, bacterial, or another cause."
            ),
            "remedies": [
                "Drink plenty of fluids / ORS",
                "Rest and monitor temperature",
                "Paracetamol if needed (follow label dosage)"
            ],
        }

    # Fever + rash or severe body pain (possible dengue warning)
    if "fever" in s and ("rash" in s or "severe body pain" in s):
        return {
            "level": "doctor-soon",
            "message": (
                "⚠️ <strong>Fever with rash or severe body pain can be serious.</strong><br>"
                "Please consult a doctor as soon as possible."
            ),
            "remedies": []
        }

    # Fever + headache together
    if "fever" in s and "headache" in s:
        return {
            "level": "doctor-soon",
            "message": (
                "🤒 <strong>Fever with headache needs monitoring.</strong>"
            ),
            "remedies": [
                "Drink plenty of fluids",
                "Rest in a cool room",
                "Paracetamol if needed"
            ],
        }

    # ---------------- LOOSE MOTION / DIARRHEA ----------------
    if "loose motion" in s or "diarrhea" in s or "loose stools" in s:
        # If dehydration signs present → doctor soon
        if "dizzy" in s or "very weak" in s or "dry mouth" in s:
            return {
                "level": "doctor-soon",
                "message": (
                    "💧 <strong>You may be getting dehydrated.</strong><br>"
                    "Please see a doctor soon."
                ),
                "remedies": [
                    "Take ORS frequently",
                    "Small sips of water",
                    "Light food only"
                ],
            }

        # Mild case → home care
        return {
            "level": "home-care",
            "message": (
                "💧 <strong>Loose motion can often be managed at home.</strong>"
            ),
            "remedies": [
                "Drink ORS in small sips",
                "Eat curd rice, bananas, toast",
                "Avoid spicy/oily food"
            ],
        }

    # ---------------- SORE THROAT ----------------
    if "throat" in s:
        return {
            "level": "home-care",
            "message": (
                "🗣️ <strong>Looks like mild throat irritation.</strong>"
            ),
            "remedies": [
                "Warm salt-water gargle",
                "Honey with warm water",
                "Avoid very cold drinks"
            ]
        }

    # ---------------- COLD / COUGH ----------------
    if "cold" in s or "cough" in s:
        return {
            "level": "home-care",
            "message": (
                "🤧 <strong>Looks like a common cold.</strong>"
            ),
            "remedies": [
                "Steam inhalation",
                "Warm fluids",
                "Rest well"
            ]
        }

    # ---------------- STOMACH PAIN ----------------
    if "stomach" in s or "gas" in s:
        return {
            "level": "home-care",
            "message": (
                "🌿 <strong>Mild stomach discomfort can be managed at home.</strong>"
            ),
            "remedies": [
                "Light meals only",
                "ORS or coconut water",
                "Avoid spicy food"
            ]
        }

    # ---------------- CHILDREN (EXTRA CAUTION) ----------------
    if age and age < 5 and "fever" in s:
        return {
            "level": "doctor-soon",
            "message": (
                "👶 <strong>Your child has fever — please consult a doctor soon.</strong>"
            ),
            "remedies": [
                "Keep the child hydrated",
                "Sponge bath with lukewarm water",
                "Do not self-medicate without a doctor"
            ],
        }

    # ---------------- DEFAULT ----------------
    return {
        "level": "doctor-soon",
        "message": (
            "🩺 <strong>I’m not fully sure about these symptoms.</strong><br>"
            "If they persist or worsen, please see a doctor."
        ),
        "remedies": []
    }
