import webbrowser
import subprocess
import sys
import os
import re
from datetime import datetime
from urllib.parse import quote_plus


def open_url(url: str, label: str) -> str:
    webbrowser.open(url)
    return f"Opening {label}."


def open_youtube_search(topic: str) -> str:
    url = f"https://www.youtube.com/results?search_query={quote_plus(topic)}"
    webbrowser.open(url)
    return f"Opening YouTube and searching for {topic}."


def open_google_search(topic: str) -> str:
    url = f"https://www.google.com/search?q={quote_plus(topic)}"
    webbrowser.open(url)
    return f"Opening Google and searching for {topic}."


def open_app_windows(command: str, label: str) -> str:
    subprocess.Popen(command)
    return f"Opening {label}."


def get_special_folder(folder_name: str) -> str | None:
    home = os.path.expanduser("~")
    onedrive = os.path.join(home, "OneDrive")
    candidates = [
        os.path.join(home, folder_name),
        os.path.join(onedrive, folder_name),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def open_folder(path: str, label: str) -> str:
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
        return f"Opening {label}."
    raise RuntimeError("Folder opening is only configured for Windows.")


def extract_topic_from_text(user_text: str, keywords: list[str]) -> str | None:
    lowered = user_text.lower()
    for keyword in keywords:
        if keyword in lowered:
            start = lowered.find(keyword) + len(keyword)
            topic = user_text[start:].strip(" :,-")
            if topic:
                return topic
    return None


def normalize_math_expression(text: str) -> str:
    expr = text.lower()
    expr = expr.replace("calculate", "")
    expr = expr.replace("what is", "")
    expr = expr.replace("solve", "")
    expr = expr.replace("multiplied by", "*")
    expr = expr.replace("multiply by", "*")
    expr = expr.replace("times", "*")
    expr = expr.replace("x", "*")
    expr = expr.replace("divided by", "/")
    expr = expr.replace("divide by", "/")
    expr = expr.replace("plus", "+")
    expr = expr.replace("minus", "-")
    return expr.strip()


def safe_calculate(expression: str) -> str:
    cleaned = normalize_math_expression(expression)
    if not re.fullmatch(r"[0-9\.\+\-\*\/\(\) ]+", cleaned):
        return "I could not understand that math expression."
    try:
        result = eval(cleaned, {"__builtins__": {}}, {})
        return f"The result is {result}."
    except Exception:
        return "I could not calculate that expression."


def perform_action(intent_data: dict) -> str:
    intent = intent_data.get("intent", "")

    websites = {
        "github": "https://github.com",
        "linkedin": "https://linkedin.com",
        "gmail": "https://mail.google.com",
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "chatgpt": "https://chatgpt.com",
        "whatsapp": "https://web.whatsapp.com",
        "spotify": "https://open.spotify.com",
        "netflix": "https://netflix.com",
        "jobstreet": "https://www.jobstreet.com.my",
    }

    if intent == "open_website":
        target = intent_data.get("target", "").lower()
        if target in websites:
            return open_url(websites[target], target.title())

    if intent == "open_app":
        target = intent_data.get("target", "").lower()

        if target == "calculator":
            return open_app_windows("calc.exe", "Calculator")

        if target == "notepad":
            return open_app_windows("notepad.exe", "Notepad")

        if target in {"file explorer", "explorer"}:
            return open_app_windows("explorer.exe", "File Explorer")

        if target in {"command prompt", "cmd"}:
            return open_app_windows("cmd.exe", "Command Prompt")

        if target in {"vs code", "vscode"}:
            code_path = os.path.expandvars(
                r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            )
            try:
                subprocess.Popen(code_path)
                return "Opening VS Code."
            except Exception:
                return "I could not find VS Code on your system."

    if intent == "open_folder":
        target = intent_data.get("target", "").capitalize()
        path = get_special_folder(target)
        if path:
            return open_folder(path, target)
        return f"I could not find your {target} folder."

    if intent == "youtube_search":
        topic = extract_topic_from_text(
            intent_data.get("text", ""),
            [
                "search youtube for",
                "search on youtube for",
                "open youtube and search for",
                "open youtube and search",
                "youtube search for",
                "youtube search",
                "find on youtube",
                "look up on youtube",
                "play on youtube",
                "type",
                "search",
                "find",
                "play",
            ],
        )
        if topic:
            return open_youtube_search(topic)
        return "Tell me what you want to search on YouTube."

    if intent == "google_search":
        topic = extract_topic_from_text(
            intent_data.get("text", ""),
            [
                "search google for",
                "search on google for",
                "open google and search for",
                "open google and search",
                "google search for",
                "google search",
                "find on google",
                "look up on google",
                "search",
                "find",
                "look up",
            ],
        )
        if topic:
            return open_google_search(topic)
        return "Tell me what you want to search on Google."

    if intent == "math":
        return safe_calculate(intent_data.get("text", ""))

    if intent == "time":
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."

    if intent == "date":
        return f"Today is {datetime.now().strftime('%A, %d %B %Y')}."

    if intent == "save_note":
        text = intent_data.get("text", "")
        lowered = text.lower()
        note = text[lowered.find("save note") + len("save note"):].strip(" :,-") if "save note" in lowered else ""
        if not note:
            return "__ASK_SAVE_NOTE__"
        with open("notes.txt", "a", encoding="utf-8") as file:
            file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {note}\n")
        return "Your note has been saved."

    if intent == "read_notes":
        if not os.path.exists("notes.txt"):
            return "You do not have any saved notes yet."
        try:
            with open("notes.txt", "r", encoding="utf-8") as file:
                content = file.read().strip()
            return content if content else "Your notes file is empty."
        except Exception:
            return "I could not read your notes."

    if intent == "screenshot":
        try:
            import pyautogui
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desktop_path = get_special_folder("Desktop")
            if desktop_path:
                filename = os.path.join(desktop_path, f"screenshot_{timestamp}.png")
            else:
                filename = f"screenshot_{timestamp}.png"

            image = pyautogui.screenshot()
            image.save(filename)
            return f"Screenshot saved as {filename}."
        except ImportError:
            return "Screenshot support is not installed. Please install pyautogui and pillow."
        except Exception as e:
            return f"Screenshot error: {e}"

    if intent == "speak_text":
        text = intent_data.get("text", "")
        spoken = text.split(" ", 1)[1].strip() if " " in text else ""
        return f"__SPEAK__:{spoken}" if spoken else "Tell me what you want me to say."

    return ""