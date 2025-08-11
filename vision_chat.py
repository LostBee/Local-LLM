"""
chat.py  –  CLI that supports normal text turns *and*    image turns.
Usage:
  text question  → type as usual
  img <path> ?Q  → ask about an image, optional question after the path
"""

from pathlib import Path
from bot import (
    load_history, save_history, ensure_system,
    add_user, add_assistant, query_ollama, image_to_base64
)

def main() -> None:
    history = ensure_system(load_history())

    print("Vision Chat – type 'exit' to quit.")
    print("For image questions:  img <path-to-image>  [optional question]\n")

    while True:
        try:
            raw = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if raw.lower() in {"exit", "quit"}:
            break

        # ─── branch: image or text ───────────────────────────────
        if raw.lower().startswith("img "):
            parts = raw.split(maxsplit=2)            # img path [question...]
            if len(parts) < 2:
                print("⚠️  Usage: img <path> [question]")
                continue

            path = Path(parts[1]).expanduser()
            if not path.exists():
                print("⚠️  File not found.")
                continue

            question = parts[2] if len(parts) == 3 else "Describe this image."
            history = add_user(question, history)
            img_b64 = image_to_base64(path)

            reply = query_ollama(history, img_b64=img_b64)
        else:
            # plain text turn
            history = add_user(raw, history)
            reply = query_ollama(history)

        print(f"Bot: {reply}\n")
        history = add_assistant(reply, history)
        save_history(history)

    print("Goodbye!")

if __name__ == "__main__":
    main()

