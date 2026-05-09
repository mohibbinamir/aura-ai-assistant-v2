# AURA AI Assistant V2

AURA AI Assistant V2 is a local desktop AI assistant built with Python. It combines a modern GUI, smart local actions, and Ollama-powered AI chat to help with everyday desktop tasks.

## Features

- Modern desktop GUI built with CustomTkinter
- Open websites such as GitHub, YouTube, Netflix, Gmail, LinkedIn, and more
- Open applications such as Calculator, Notepad, VS Code, and File Explorer
- Open system folders such as Desktop, Downloads, and Documents
- Search YouTube directly from natural commands
- Search Google directly from natural commands
- Show current time and date
- Save notes and read saved notes
- Take screenshots and save them automatically
- Solve basic math expressions
- Use local AI chat through Ollama

## Example Commands

- Open GitHub
- Open YouTube and search MrBeast
- Open Downloads
- What time is it
- Save note Buy milk
- Read notes
- Take screenshot
- Calculate 3 multiply by 200

## Technologies Used

- Python
- CustomTkinter
- Ollama
- Requests
- PyAutoGUI
- Pillow
- pyttsx3

## How It Works

AURA first checks whether the user request matches a local action such as opening an app, opening a website, searching YouTube, searching Google, saving a note, or taking a screenshot.

If the request is a normal question or conversation, it sends the message to a local Ollama model for AI-generated responses.

## Installation

1. Clone the repository
2. Install Python 3.12
3. Install Ollama
4. Pull a local model:

```bash
ollama pull llama3.2
