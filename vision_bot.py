"""
vision_bot.py
Pure utilities and configuration for a multimodal (vision+text) Ollama chatbot.
"""

from __future__ import annotations
import base64, json
from pathlib import Path
from typing import List, Dict, Optional
import requests
from PIL import Image

# ───────── configuration ─────────
MODEL = "gemma3:4b"                      # change to any multimodal model you pulled
BASE_URL = "http://localhost:11434/api/chat"

SYSTEM_PROMPT = (
    "You are Vision-Buddy, a concise and friendly assistant. "
    "When an image is provided, describe it and answer the user’s question."
)

HISTORY_FILE = Path("history.json")
History = List[Dict[str, str]]           # type alias

# ───────── persistence ────────────
def load_history() -> History:
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    return []

def save_history(history: History) -> None:
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")

# ───────── helper: encode image ────
def image_to_base64(path: Path) -> str:
    """Return base-64 string of the image, suitable for Ollama."""
    data = path.read_bytes()             # Pillow not strictly needed, but keeps option to preprocess
    return base64.b64encode(data).decode("utf-8")

# ───────── conversation helpers ───
def ensure_system(history: History) -> History:
    if not history or history[0]["role"] != "system":
        history = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    return history

def add_user(text: str, history: History) -> History:
    history.append({"role": "user", "content": text})
    return history

def add_assistant(reply: str, history: History) -> History:
    history.append({"role": "assistant", "content": reply})
    return history

# ───────── model call ──────────────
def query_ollama(history: History, img_b64: Optional[str] = None) -> str:
    """
    Send history (+ optional image) to Ollama and return assistant reply.
    """
    if img_b64:
        history[-1]["images"] = [img_b64]   # attach image to the most-recent user turn

    payload = {
        "model": MODEL,
        "messages": history,
        "stream": False
    }

    resp = requests.post(BASE_URL, json=payload, timeout=300)
    resp.raise_for_status()
    return resp.json()["message"]["content"]
