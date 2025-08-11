"""
bot.py  –  vision-enabled utilities for Ollama chat
"""

from __future__ import annotations
import base64, json
from pathlib import Path
from typing import List, Dict, Optional
import requests
from PIL import Image

# ───────── configuration ─────────
MODEL = "llava:13b"                     # ← change to any multimodal model you pulled
BASE_URL = "http://localhost:11434/api/chat"
SYSTEM_PROMPT = (
    "You are Vision-Buddy, a concise and friendly assistant. "
    "When an image is provided, describe it and answer the user’s question."
)
HISTORY_FILE = Path("history.json")
History = List[Dict[str, str]]          # (images are injected only for the API call)

# ───────── persistence ────────────
def load_history() -> History:
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    return []

def save_history(history: History) -> None:
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")

# ───────── helper: encode image ────
def image_to_base64(path: Path) -> str:
    """Load an image file and return base-64 string suitable for Ollama."""
    with Image.open(path) as img:
        img = img.convert("RGB")        # ensure consistent encoding
        buf = Path(path).read_bytes()
    return base64.b64encode(buf).decode("utf-8")

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
    Send history (+ optional base64 image) to Ollama and return the assistant reply.
    """
    # If it's an image turn, tack the image list onto the *last* user message
    if img_b64:
        history[-1]["images"] = [img_b64]

    payload = {
        "model": MODEL,
        "messages": history,
        "stream": False
    }

    resp = requests.post(BASE_URL, json=payload, timeout=300)
    resp.raise_for_status()
    return resp.json()["message"]["content"]
