# bot.py
# Lightweight way to dump history to JSON i.e. same structure Ollama already expects
# Keeps network calls, history loading/saving, and prompt handling separate from any user-interface code so we can unit-test easily.


from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict
import requests


# Configuration
MODEL = "qwen3:4b"                       
BASE_URL = "http://localhost:11434/api/chat"

SYSTEM_PROMPT = (
    "You are a an online AI Companion named Lily"
    "Chat with the user about whatever they desire"
)

HISTORY_FILE = Path("history.json")       # saved in the project root
History = List[Dict[str, str]]           



# Persistence helpers
def load_history() -> History:
    """
    Return the saved chat history if the file exists, otherwise an empty list.
    """
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    return []


def save_history(history: History) -> None:
    """
    Overwrite history.json with the current conversation.
    """
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")



# Conversation Helpers
def ensure_system_prompt(history: History) -> History:
    """
    Make sure the first entry in history is always the system prompt.
    """
    if not history or history[0]["role"] != "system":
        history = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    return history


def append_user_message(user_text: str, history: History) -> History:
    history.append({"role": "user", "content": user_text})
    return history


def append_assistant_message(reply: str, history: History) -> History:
    history.append({"role": "assistant", "content": reply})
    return history



# Model Call
def query_ollama(history: History) -> str:
    """
    Send the given history to Ollama and return the assistant's reply text.
    Non-streaming call for simplicity.
    """
    payload = {
        "model": MODEL,
        "messages": history,
        "stream": False
    }

    resp = requests.post(BASE_URL, json=payload, timeout=300)
    resp.raise_for_status()                                  # raise on HTTP errors
    data = resp.json()
    return data["message"]["content"]
