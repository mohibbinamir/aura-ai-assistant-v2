import requests
from intent_router import detect_intent
from commands import perform_action

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"

SYSTEM_PROMPT = """
You are AURA, a helpful desktop AI assistant.
Rules:
1. Local actions are handled before AI chat.
2. If the request is normal conversation, answer naturally.
3. Keep responses concise unless more detail is requested.
"""


class AuraCore:
    def __init__(self) -> None:
        pass

    def get_response(self, user_text: str) -> str:
        intent_data = detect_intent(user_text)

        if intent_data["intent"] != "general_chat":
            result = perform_action(intent_data)
            if result:
                return result

        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            "stream": False,
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"].strip()
        except requests.exceptions.ConnectionError:
            return "Ollama is not running. Please start Ollama first."
        except Exception as e:
            return f"Local AI Error: {e}"