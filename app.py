from assistant_core import AuraCore
from gui import AuraGUI
from speech import SpeechManager

core = AuraCore()
speech = SpeechManager()


def send_message(user_text: str) -> str:
    try:
        reply = core.get_response(user_text)
    except Exception as e:
        reply = f"Error while processing request: {e}"

    try:
        speech.speak(reply)
    except Exception:
        pass

    return reply


if __name__ == "__main__":
    app = AuraGUI(send_message)
    app.mainloop()