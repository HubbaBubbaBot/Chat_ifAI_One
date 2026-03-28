# ✦ ifAI Chat

**A friendly terminal AI chat client for everyone.**

Built by [ifAI.One](https://github.com/ifAI-One) — Educational AI tools for everyone.

---

## What is this?

ifAI Chat is a terminal-based AI chat application that lets you have conversations with AI assistants right from your command line. It works with any OpenAI-compatible API endpoint — including OpenAI, OpenRouter, Ollama, LM Studio, and more.

**No AI expertise needed.** The app includes a guided setup wizard and built-in documentation that explains everything from "what is an API key?" to "how do I write a good prompt."

### Features

- 🧭 **Interactive arrow-key menus** — no commands to memorize
- 🧙 **First-run setup wizard** — walks you through everything step by step
- 💬 **Multi-turn conversations** — the AI remembers your chat history
- 💾 **SQLite session storage** — conversations saved locally, always
- 🔀 **Fork sessions** — branch a conversation to explore different paths
- 📚 **Built-in Help & Docs** — learn about AI, prompts, and more right inside the app
- 🔌 **Any OpenAI-compatible endpoint** — OpenAI, OpenRouter, Ollama, LM Studio, custom
- 📱 **Runs on Termux** — yes, even on your phone
- ⚡ **Streaming responses** — watch the AI type in real time

---

## Install

### Termux (Android)

```bash
pkg install python
pip install requests rich
```

### Linux / macOS

```bash
pip3 install requests rich
```

### Clone and run

```bash
git clone https://github.com/ifAI-One/ifai-chat.git
cd ifai-chat
pip install -r requirements.txt
python3 chat.py
```

### Optional: Create a `chat` command

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
alias chat="python3 /path/to/chat.py"
```

On Termux, you can also create a launcher script:
```bash
echo '#!/bin/bash
python3 "$HOME/chat/chat.py" "$@"' > $PREFIX/bin/chat
chmod +x $PREFIX/bin/chat
```

---

## Quick Start

1. Run `chat` (or `python3 chat.py`)
2. The setup wizard will guide you through choosing a provider and entering your API key
3. Start chatting!

**Already know what you're doing?** Use `chat --config` to skip the wizard.

---

## Provider Setup

### OpenAI
1. Create an account at [platform.openai.com](https://platform.openai.com)
2. Go to [API Keys](https://platform.openai.com/api-keys) and create a new key
3. Add billing info (API usage is pay-per-use)
4. In the setup wizard, choose **OpenAI** and paste your key

### OpenRouter
1. Create an account at [openrouter.ai](https://openrouter.ai)
2. Go to [Keys](https://openrouter.ai/keys) and create a new key
3. Many models are **free** — great for getting started!
4. In the setup wizard, choose **OpenRouter** and paste your key

### Ollama (Local, Free)
1. Install from [ollama.com](https://ollama.com)
2. Pull a model: `ollama pull llama3`
3. Ollama runs automatically in the background
4. In the setup wizard, choose **Ollama** — no API key needed!

### LM Studio (Local, Free)
1. Download from [lmstudio.ai](https://lmstudio.ai)
2. Download a model inside the app
3. Start the local server in LM Studio
4. In the setup wizard, choose **LM Studio** — no API key needed!

---

## Usage

### CLI Flags

| Flag | Description |
|------|-------------|
| `chat` | Normal start (wizard on first run) |
| `chat --config` | Skip wizard, go straight to menu |
| `chat --setup` | Re-run the setup wizard |
| `chat --version` | Show version |

### Main Menu

Navigate with **arrow keys**, select with **Enter**:

- **New Chat** — Start a fresh conversation
- **Resume Session** — Continue a previous chat
- **Fork Session** — Branch off from a past conversation
- **Help & Docs** — Built-in guides and explanations
- **Configure** — Change provider, model, API key, etc.

### In-Chat Commands

| Command | Description |
|---------|-------------|
| `/back` | Return to main menu |
| `/clear` | Clear AI context (chat stays saved) |
| `/rename <name>` | Rename the current session |
| `/help` | Show available commands |
| `/exit` | Quit the app |

### Keyboard Shortcuts

| Key | In Menus | In Chat |
|-----|----------|---------|
| `↑↓` or `jk` | Navigate | — |
| `Enter` | Select | Send message |
| `q` / `ESC` | Go back | — |
| `Ctrl+C` | — | Return to menu |

---

## Configuration

Settings are stored in `~/chat/config.json`:

```json
{
  "endpoint": "https://api.openai.com/v1",
  "api_key": "sk-...",
  "model": "gpt-4o",
  "system_prompt": "You are a helpful assistant.",
  "stream": true,
  "max_history": 50
}
```

You can edit this file directly or use **Configure** in the app menu.

---

## Data Storage

All conversations are stored locally in `~/chat/chat_history.db` (SQLite). Nothing is sent anywhere except to your configured AI provider.

---

## Contributing

We welcome contributions! This project is part of ifAI.One's educational mission.

- 🐛 Found a bug? [Open an issue](https://github.com/ifAI-One/ifai-chat/issues)
- 💡 Have an idea? We'd love to hear it
- 🔧 Want to contribute code? Fork and submit a PR

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with ♥ by <a href="https://github.com/ifAI-One">ifAI.One</a><br>
  <em>Educational AI tools for everyone.</em>
</p>
