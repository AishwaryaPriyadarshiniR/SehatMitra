from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

client = Groq(api_key=GROQ_API_KEY)

def make_friendly_response(user_input, triage_result):
    """
    Uses Groq LLM only to polish the response.
    It never changes the safety decision from triage().
    """

    prompt = f"""
    You are SehatMitra, a kind, calm, and trustworthy Indian health assistant.

    User said: "{user_input}"

    Safety decision from rules:
    Level: {triage_result['level']}
    Base message: {triage_result['message']}
    Remedies: {triage_result['remedies']}

    Rewrite this into a concise, well-structured health reply with:
    - Maximum 5 bullet points total
    - Short and direct lines (no long paragraphs)
    - Clear main advice (based only on the base message)
    - Remedies as bullet points (if any)
    - A brief safety note at the end
    - Do not claim memory of previous conversations unless explicitly provided in this prompt
    - Do not add diagnosis certainty or new medical facts not present in base message/remedies
    """

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are SehatMitra, a kind and safe health assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=170,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


def make_conversational_response(user_input, history=None, health_context=None):
    """
    Handles free-form conversation and follow-up questions.
    If health_context is provided, the response stays aligned with prior safety context.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are SehatMitra, a friendly and safe Indian health companion. "
                "You can do normal conversation and health follow-ups. "
                "Do not claim memory unless conversation history is provided. "
                "Do not provide diagnosis certainty; keep advice cautious and practical. "
                "For normal chat (non-medical), keep responses to 3-4 short sentences max."
            ),
        }
    ]

    if history:
        messages.extend(history[-6:])

    if health_context:
        context_text = (
            "Previous health context:\n"
            f"- Level: {health_context.get('level', 'home-care')}\n"
            f"- Message: {health_context.get('message', '')}\n"
            f"- Remedies: {health_context.get('remedies', [])}\n"
            "Answer the user's follow-up consistently with this context. "
            "If emergency signs appear, advise urgent care. "
            "For this health follow-up, respond in 3-5 concise bullet points."
        )
        messages.append({"role": "system", "content": context_text})

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        max_tokens=170,
        temperature=0.5,
    )

    return response.choices[0].message.content.strip()
