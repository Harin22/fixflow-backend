import json

from app.services.ai_service import ask_ai


def analyze_code(code, error):

    prompt = f"""
You are FixFlow, an AI code debugging assistant.

Analyze the following code and error.

CODE:
{code}

ERROR:
{error}

Return ONLY valid JSON in exactly this format:

{{
    "why_it_happened": "Explain the root cause.",
    "how_to_fix_it": "Explain how to fix the problem.",
    "what_you_can_learn": "Explain the programming concept.",
    "fixed_code": "Provide the complete corrected code."
}}
"""

    result = ask_ai(prompt)

    return json.loads(result)