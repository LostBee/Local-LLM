# chat.py - Minimal terminal chatbot for local Ollama model
# Author: https://github.com/LostBee

import requests
import sys

MODEL     = "qwen3:4b"
BASE_URL  = "http://localhost:11434/api/chat"

history: list[dict[str, str]] = [] # Keeping conversations

print("Type 'exit' to quit.\n")

while True:
    try:
        user_text = input("You: ").strip()
    except (EOFError, KeyboardInterrupt): #To handle Ctrl+C if needeed to terminate script
        print("\nBye!")
        sys.exit(0)

    if user_text.lower() in {"exit", "quit"}:
        break

    history.append({"role": "user", "content": user_text})

    payload = {
        "model": MODEL,
        "messages": history,
        "stream": False        
    }

    resp = requests.post(BASE_URL, json=payload, timeout=600)
    resp.raise_for_status()

    data = resp.json()          # one complete JSON object
    assistant_reply = data["message"]["content"]

    print(f"Bot: {assistant_reply}\n")

    history.append({"role": "assistant", "content": assistant_reply})
    


