from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

HF_TOKEN = os.getenv("HF_TOKEN")


client = InferenceClient(token=HF_TOKEN)

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

    response = client.text_generation(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        prompt=prompt,
        max_new_tokens=200,
        temperature=0.3
    )

    return response
