import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("INCEPTION_API_KEY")

API_URL = "https://api.inceptionlabs.ai/v1/chat/completions"


def ask_ai(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mercury-2.5",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=data
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]