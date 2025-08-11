# Local‑LLM Chatbot Project

A beginner‑friendly Python project that shows two ways to run a *local*, privacy‑preserving chatbot with [Ollama](https://ollama.ai):

1. **Text‑only CLI**

   * Files: `chat.py`, `bot.py`
   * Uses any small local language model pulled with `ollama pull`.
2. **Vision‑enabled CLI**

   * Files: `vision_chat.py`, `vision_bot.py`
   * Lets you upload an image, ask a question, and get a multimodal answer.

Both variants persist chat history in `history.json`, so you can pick up the conversation where you left off.

---

## 1. Prerequisites

| Tool / Library   | Purpose                        | Install                                                              |
| ---------------- | ------------------------------ | -------------------------------------------------------------------- |
| **Python ≥ 3.9** | Run the scripts                | [https://python.org/downloads](https://python.org/downloads)         |
| **Ollama**       | Local LLM runtime              | `curl -fsSL https://ollama.ai/install.sh \| sh` or Windows installer |
| **requests**     | HTTP calls to Ollama           | `pip install requests`                                               |
| **Pillow**       | Image encoding for vision chat | `pip install pillow`                                                 |

*(All Python packages are installed inside a virtual environment; see below.)*

---

## 2. Setup (one‑time)

```powershell
# clone / open this repo
cd Local-LLM

# create & activate venv (Windows PowerShell)
py -m venv .venv
.\.venv\Scripts\Activate

# install required libraries
pip install requests pillow

# pull at least one model
ollama pull llama2:7b          # text‑only example
ollama pull llava:13b          # vision example
```

> **Tip:** `ollama serve` is usually autostarted on Windows; on macOS/Linux run it manually in another terminal.

---

## 3. Running the **text‑only** chatbot

```powershell
python chat.py
```

| Action         | Example               |
| -------------- | --------------------- |
| Ask a question | `Hello, who are you?` |
| Quit           | `exit` or `Ctrl+C`    |

### Changing the model (text chat)

Open **`bot.py`** and edit the `MODEL` constant, e.g.

```python
MODEL = "mistral:7b-instruct"
```

Save the file and rerun `chat.py`.

---

## 4. Running the **vision** chatbot

```powershell
python vision_chat.py                # uses default model from vision_bot.py
python vision_chat.py -m qwen-vl     # pick a model at launch
```

When the program starts it prints the exact model name it will use.

### Image turn syntax

```
img <path-to-image>  [optional question]
```

Examples:

* `img cat.jpg What breed is this?`
* `img screenshot.png` (no question → the bot will describe the image)

### Changing the default model (vision chat)

*One‑off*: pass the `-m / --model` flag as shown above.

*Permanent*: edit **`DEFAULT_MODEL`** in `vision_bot.py` or set an env‑var before running:

```powershell
set OLLAMA_MODEL=llava:34b
python vision_chat.py
```

---

## 5. Project structure

```
Local-LLM/
├─ bot.py            # helper functions for text chat
├─ chat.py           # CLI wrapper for text chat
├─ vision_bot.py     # helper functions for vision chat
├─ vision_chat.py    # CLI wrapper for vision chat
├─ history.json      # created automatically, stores conversation
└─ README.md         # this file
```

*(`.venv/`, `__pycache__/`, `.vs/`, etc. are ignored via `.gitignore`)*

---

## 6. Cleaning or resetting history

Delete `history.json` or type `reset` while running `chat.py` / `vision_chat.py` if you added that command.

---

## 7. Next steps / ideas

* **Streaming tokens** – turn on `stream=True` in the payload for real‑time responses.
* **GUI** – wrap `vision_bot` in a web app (FastAPI + HTMX) or a desktop UI (`textual`, `tkinter`).
* **Prune old turns** – keep the system prompt + last *N* messages to save memory.

Enjoy hacking on local LLMs! Pull requests & issues welcome 🤖🖼️
