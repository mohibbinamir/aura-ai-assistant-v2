import pyttsx3


class SpeechManager:
    def __init__(self) -> None:
        self.engine = None
        self._init_engine()

    def _init_engine(self) -> None:
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 180)
        except Exception:
            self.engine = None

    def speak(self, text: str) -> None:
        if not text or text.startswith("__ASK_"):
            return
        if text.startswith("__SPEAK__:"):
            text = text.replace("__SPEAK__:", "", 1)

        if not self.engine:
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            pass