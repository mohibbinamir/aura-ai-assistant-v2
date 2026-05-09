from typing import Dict


def detect_intent(user_text: str) -> Dict[str, str]:
    text = user_text.lower().strip()

    # Calculator / math
    if any(word in text for word in ["calculate", "what is", "solve"]) and any(
        sym in text for sym in ["+", "-", "*", "/", "multiply", "divided", "times", "minus", "plus"]
    ):
        return {"intent": "math", "text": user_text}

    # YouTube search
    if "youtube" in text and any(word in text for word in ["search", "find", "look up", "play", "type"]):
        return {"intent": "youtube_search", "text": user_text}

    # Google search
    if "google" in text and any(word in text for word in ["search", "find", "look up"]):
        return {"intent": "google_search", "text": user_text}

    # Open website
    for site in [
        "github", "linkedin", "gmail", "chatgpt", "whatsapp",
        "spotify", "netflix", "youtube", "google", "jobstreet"
    ]:
        if site in text and any(word in text for word in ["open", "launch", "start", "visit", "go to"]):
            return {"intent": "open_website", "target": site}

    # Open app
    for app in ["calculator", "notepad", "vs code", "vscode", "file explorer", "explorer", "command prompt", "cmd"]:
        if app in text and any(word in text for word in ["open", "launch", "start"]):
            return {"intent": "open_app", "target": app}

    # Open folder
    for folder in ["desktop", "downloads", "documents"]:
        if folder in text and any(word in text for word in ["open", "show"]):
            return {"intent": "open_folder", "target": folder}

    # Time
    if any(phrase in text for phrase in ["what time", "time is it", "current time"]):
        return {"intent": "time"}

    # Date
    if any(phrase in text for phrase in ["today's date", "what is the date", "current date", "show date"]):
        return {"intent": "date"}

    # Save note
    if text.startswith("save note") or ("save" in text and "note" in text):
        return {"intent": "save_note", "text": user_text}

    # Read notes
    if any(phrase in text for phrase in ["read notes", "show notes", "open notes"]):
        return {"intent": "read_notes"}

    # Screenshot
    if any(phrase in text for phrase in ["take screenshot", "screenshot"]):
        return {"intent": "screenshot"}

    # Speak text
    if text.startswith("say ") or text.startswith("speak "):
        return {"intent": "speak_text", "text": user_text}

    return {"intent": "general_chat", "text": user_text}