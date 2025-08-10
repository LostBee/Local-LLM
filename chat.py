"""
chat.py
Command-line interface that wires user I/O to the functions in bot.py.
"""

from bot import (
    load_history,
    save_history,
    ensure_system_prompt,
    append_user_message,
    append_assistant_message,
    query_ollama,
)


def main() -> None:
    history = load_history()
    history = ensure_system_prompt(history)

    print("Local-LLM Chat – type 'exit' or press Ctrl+C to quit.\n")

    try:
        while True:
            user_text = input("You: ").strip()
            if user_text.lower() in {"exit", "quit"}:
                break

            history = append_user_message(user_text, history)
            assistant_reply = query_ollama(history)
            print(f"Bot: {assistant_reply}\n")

            history = append_assistant_message(assistant_reply, history)
            save_history(history)
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")


if __name__ == "__main__":
    main()

