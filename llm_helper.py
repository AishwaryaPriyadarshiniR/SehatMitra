from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

client = Groq(api_key=GROQ_API_KEY)

def make_friendly_response(user_input, triage_result):
    """
    Uses Hugging Face LLM only to polish the response.
    It never changes the safety decision from triage().
    """

    prompt = f"""
    You are SehatMitra, a kind, calm, and trustworthy Indian health assistant.

    User said: "{user_input}"

    Safety decision from rules:
    Level: {triage_result['level']}
    Base message: {triage_result['message']}
    Remedies: {triage_result['remedies']}

    Rewrite this into a friendly, well-structured reply with:
    - One empathetic opening line
    - Clear main advice (based only on the base message)
    - A short list of remedies (if any)
    - A gentle safety note at the end
    - Keep it simple and readable
    """

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are SehatMitra, a kind and safe health assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
