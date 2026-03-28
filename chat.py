#!/usr/bin/env python3
"""
ifAI Chat — A friendly terminal AI chat client.
Built by ifAI.One · Educational AI tools for everyone.
"""

__version__ = "1.0.0"

import argparse
import curses
import json
import sqlite3
import sys
import os
import textwrap
import requests
from datetime import datetime
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path.home() / "chat"
CFG_FILE = BASE_DIR / "config.json"
DB_FILE  = BASE_DIR / "chat_history.db"

DEFAULT_CFG = {
    "endpoint":      "https://api.openai.com/v1",
    "api_key":       "",
    "model":         "gpt-4o",
    "system_prompt": "You are a helpful assistant.",
    "stream":        True,
    "max_history":   50,
    "_configured":   False,
}

# ── Provider presets ──────────────────────────────────────────────────────────

PROVIDERS = [
    {
        "name": "OpenAI",
        "endpoint": "https://api.openai.com/v1",
        "needs_key": True,
        "desc": (
            "The company behind ChatGPT — the most popular AI\n"
            "assistant in the world. Requires a paid API key.\n\n"
            "  Get your key → platform.openai.com/api-keys\n\n"
            "Great for: reliable, high-quality conversations."
        ),
        "models": [
            ("gpt-4o",       "Best all-rounder. Smart, fast, great for most tasks."),
            ("gpt-4o-mini",  "Faster & cheaper. Great for quick questions."),
            ("gpt-4-turbo",  "Powerful. Handles very long conversations."),
            ("o3-mini",      "Reasoning model. Good for math and logic."),
        ],
    },
    {
        "name": "OpenRouter",
        "endpoint": "https://openrouter.ai/api/v1",
        "needs_key": True,
        "desc": (
            "Access 100+ AI models from one place — including\n"
            "FREE ones! Great for exploring and experimenting.\n\n"
            "  Get your key → openrouter.ai/keys\n\n"
            "Great for: trying different models without commitment."
        ),
        "models": [
            ("openai/gpt-4o-mini",                  "OpenAI's fast model via OpenRouter."),
            ("mistralai/mistral-7b-instruct:free",   "Free! Fast, capable open-source model."),
            ("google/gemma-2-9b-it:free",            "Free! Google's efficient open model."),
            ("meta-llama/llama-3-8b-instruct:free",  "Free! Meta's popular open model."),
        ],
    },
    {
        "name": "Ollama (local)",
        "endpoint": "http://localhost:11434/v1",
        "needs_key": False,
        "desc": (
            "Run AI models entirely on YOUR device. Completely\n"
            "free, completely private — no internet needed!\n\n"
            "  Install → ollama.com\n"
            "  Then run: ollama pull llama3\n\n"
            "Great for: privacy, offline use, and learning."
        ),
        "models": [
            ("llama3",   "Meta's Llama 3. Excellent open-source model."),
            ("mistral",  "Fast and capable. Great for most tasks."),
            ("phi3",     "Small but mighty. Works on low-resource devices."),
            ("gemma2",   "Google's efficient open model."),
        ],
    },
    {
        "name": "LM Studio (local)",
        "endpoint": "http://localhost:1234/v1",
        "needs_key": False,
        "desc": (
            "A friendly desktop app for running AI locally.\n"
            "Download models with a visual interface.\n\n"
            "  Download → lmstudio.ai\n\n"
            "Great for: beginners who want local AI with a GUI."
        ),
        "models": [
            ("(use LM Studio's loaded model)", "LM Studio serves whatever model you load in the app."),
        ],
    },
    {
        "name": "Custom / Other",
        "endpoint": "",
        "needs_key": True,
        "desc": (
            "Enter your own OpenAI-compatible endpoint.\n"
            "This works with any server that speaks the\n"
            "OpenAI Chat Completions API format.\n\n"
            "Great for: self-hosted models, company endpoints."
        ),
        "models": [],
    },
]

SYSTEM_PRESETS = [
    ("Helpful Assistant",
     "You are a helpful assistant.",
     "A friendly, general-purpose AI that helps with anything."),
    ("Patient Teacher",
     "You are a patient, encouraging teacher. Explain things simply, use analogies, and always check for understanding.",
     "Perfect for learning — explains things step by step."),
    ("Socratic Tutor",
     "You are a Socratic tutor. Guide the user to answers through thoughtful questions rather than giving direct answers.",
     "Helps you think through problems on your own."),
    ("Code Reviewer",
     "You are an expert code reviewer. Be thorough, explain your reasoning, and suggest improvements with examples.",
     "Detailed code feedback with explanations."),
    ("Creative Writer",
     "You are a creative writing assistant. Help with stories, poetry, dialogue, and worldbuilding. Be imaginative and supportive.",
     "For fiction, poetry, and creative projects."),
    ("Write my own", "", "Enter your own custom instructions for the AI."),
]

# ── Help docs ─────────────────────────────────────────────────────────────────

HELP_TOPICS = [
    ("What is this app?", textwrap.dedent("""\
        ✦ What is ifAI Chat?
        ─────────────────────

        ifAI Chat is a terminal-based chat application that lets you
        have conversations with AI assistants — right from your
        command line!

        Think of it like ChatGPT, but running in your terminal.
        You type messages, and an AI responds.

        What makes it special:
        • Works with many AI providers (OpenAI, Ollama, etc.)
        • Your conversations are saved locally in a database
        • You can resume, fork, and manage chat sessions
        • It runs anywhere — even on a phone with Termux!

        This app was built by ifAI.One as part of our mission to
        make AI tools accessible and educational for everyone.

        No AI expertise needed — just curiosity! 💡
    """)),

    ("Providers & Endpoints", textwrap.dedent("""\
        ✦ AI Providers & Endpoints
        ──────────────────────────

        An "AI provider" is a service that runs AI models for you.
        Some run in the cloud (you need internet), and some run
        right on your own device (completely offline).

        Cloud providers:
        • OpenAI    — makers of ChatGPT (paid, very capable)
        • OpenRouter — one account, 100+ models (some free!)

        Local providers (free, private, no internet):
        • Ollama    — simple CLI tool for local AI
        • LM Studio — desktop app with a visual interface

        An "endpoint" is just a web address where the AI lives.
        For example: https://api.openai.com/v1

        All providers in this app use the same "language" to
        communicate (the OpenAI API format), so you can switch
        between providers easily.

        💡 Tip: Start with OpenRouter if you want to explore —
        they have free models you can try immediately!
    """)),

    ("API Keys Explained", textwrap.dedent("""\
        ✦ What are API Keys?
        ────────────────────

        An API key is like a password that proves you have an
        account with an AI provider. When you send a message,
        the key tells the provider "this person is allowed to
        use my AI."

        Where to get your key:
        • OpenAI     → platform.openai.com/api-keys
        • OpenRouter → openrouter.ai/keys

        When you create a key, COPY IT RIGHT AWAY — most
        providers only show it once!

        Keeping your key safe:
        • Never share it publicly (don't post it online)
        • It's stored locally in ~/chat/config.json
        • It never leaves your device (except to the provider)

        Local providers (Ollama, LM Studio) don't need keys
        because the AI runs on your own device.

        💡 Tip: If your key stops working, check your provider's
        dashboard — you may need to add billing or generate
        a new key.
    """)),

    ("Understanding Models", textwrap.dedent("""\
        ✦ Understanding AI Models
        ─────────────────────────

        An AI "model" is the brain behind the conversation.
        Different models have different strengths:

        Capability: How smart and nuanced the responses are.
        Speed: How fast it generates responses.
        Cost: How much each message costs (cloud only).
        Context: How much conversation it can "remember."

        General guidelines:
        • Bigger models → smarter but slower and pricier
        • Smaller models → faster, cheaper, good for simple tasks
        • "Free" models → great for learning and experimenting

        Popular models:
        • GPT-4o      — OpenAI's best all-rounder
        • GPT-4o-mini — fast & cheap, good for quick chats
        • Llama 3     — excellent free/open-source model
        • Mistral     — fast, open-source, runs locally

        Context window = how many words the AI can "see" at once.
        Bigger context = remembers more of your conversation.

        💡 Tip: Start with a smaller model to learn the ropes,
        then try larger ones when you need more power.
    """)),

    ("Chat Tips & Prompting", textwrap.dedent("""\
        ✦ Chat Tips & Writing Good Prompts
        ───────────────────────────────────

        A "prompt" is just what you type to the AI. Better
        prompts get better responses. Here are some tips:

        Be specific:
          ✗ "Tell me about Python"
          ✓ "Explain Python list comprehensions with 3 examples"

        Give context:
          ✗ "Fix this code"
          ✓ "This Python function should return even numbers
             but returns all numbers. Fix it: [paste code]"

        Ask for a format:
          ✓ "Explain in bullet points"
          ✓ "Give me a step-by-step guide"
          ✓ "Explain like I'm 10 years old"

        System prompts shape the AI's personality. You can
        set one in Configure → System Prompt. For example:
          "You are a patient teacher who uses analogies"

        💡 Tip: If the response isn't what you wanted, try
        rephrasing or adding "Let me clarify what I mean..."
    """)),

    ("Session Management", textwrap.dedent("""\
        ✦ Managing Your Chat Sessions
        ──────────────────────────────

        Every conversation is automatically saved to a local
        database on your device.

        New Chat:
          Starts a fresh conversation. Your previous chats
          are saved and can be resumed anytime.

        Resume:
          Pick a previous conversation and continue where
          you left off. The AI remembers the full history.

        Fork:
          Create a copy of a past conversation and take it
          in a different direction. The original is untouched.
          Think of it like "branching" in a choose-your-own-
          adventure story!

        In-chat commands:
          /back          Return to the main menu
          /clear         Forget context (session stays saved)
          /rename <name> Give your session a custom name
          /help          Show available commands
          /exit          Close the app

        All data is stored in: ~/chat/chat_history.db

        💡 Tip: Use /rename to label important conversations
        so you can find them easily later!
    """)),

    ("Keyboard Shortcuts", textwrap.dedent("""\
        ✦ Keyboard Shortcuts
        ────────────────────

        In menus:
          ↑ / k       Move up
          ↓ / j       Move down
          Enter       Select
          q / ESC     Go back

        In text input fields:
          ← →         Move cursor
          Backspace   Delete character
          Enter       Confirm
          ESC         Cancel

        In chat:
          Type normally and press Enter to send.
          Use / commands (see Session Management).
          Ctrl+C      Return to menu
    """)),
]


# ══════════════════════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════════════════════

def load_cfg():
    if not CFG_FILE.exists():
        save_cfg(DEFAULT_CFG.copy())
    with open(CFG_FILE) as f:
        cfg = json.load(f)
    for k, v in DEFAULT_CFG.items():
        cfg.setdefault(k, v)
    return cfg

def save_cfg(cfg):
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    with open(CFG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


# ══════════════════════════════════════════════════════════════════════════════
#  DATABASE
# ══════════════════════════════════════════════════════════════════════════════

def init_db():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, created_at TEXT, forked_from INTEGER)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER, role TEXT, content TEXT, created_at TEXT,
        FOREIGN KEY (session_id) REFERENCES sessions(id))""")
    conn.commit()
    return conn

def new_session(conn, name=None, forked_from=None):
    name = name or datetime.now().strftime("Chat %Y-%m-%d %H:%M")
    cur = conn.execute(
        "INSERT INTO sessions (name, created_at, forked_from) VALUES (?,?,?)",
        (name, datetime.now().isoformat(), forked_from))
    conn.commit()
    return cur.lastrowid

def save_msg(conn, sid, role, content):
    conn.execute(
        "INSERT INTO messages (session_id,role,content,created_at) VALUES (?,?,?,?)",
        (sid, role, content, datetime.now().isoformat()))
    conn.commit()

def load_msgs(conn, sid):
    rows = conn.execute(
        "SELECT role,content FROM messages WHERE session_id=? ORDER BY id", (sid,)
    ).fetchall()
    return [{"role": r, "content": c} for r, c in rows]

def list_sessions(conn, limit=30):
    return conn.execute(
        "SELECT id,name,created_at FROM sessions ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()

def session_preview(conn, sid):
    row = conn.execute(
        "SELECT content FROM messages WHERE session_id=? AND role='user' ORDER BY id LIMIT 1",
        (sid,)).fetchone()
    return row[0][:50] if row else "(empty)"

def rename_session(conn, sid, name):
    conn.execute("UPDATE sessions SET name=? WHERE id=?", (name, sid))
    conn.commit()

def count_sessions(conn):
    return conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]


# ══════════════════════════════════════════════════════════════════════════════
#  CURSES HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def setup_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN,   -1)
    curses.init_pair(2, curses.COLOR_BLACK,  curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_WHITE,  -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)
    curses.init_pair(5, curses.COLOR_GREEN,  -1)
    curses.init_pair(6, curses.COLOR_RED,    -1)

def C(n, bold=False):
    attr = curses.color_pair(n)
    if bold:
        attr |= curses.A_BOLD
    return attr

def safe_addstr(scr, y, x, text, attr=0):
    h, w = scr.getmaxyx()
    if y < 0 or y >= h or x >= w:
        return
    text = str(text)[:w - x - 1]
    try:
        scr.addstr(y, x, text, attr)
    except curses.error:
        pass

def draw_box(scr, y, x, width, title=""):
    safe_addstr(scr, y,     x, "╭" + "─" * (width - 2) + "╮", C(1))
    safe_addstr(scr, y + 1, x, "│" + " " * (width - 2) + "│", C(1))
    safe_addstr(scr, y + 2, x, "╰" + "─" * (width - 2) + "╯", C(1))
    if title:
        safe_addstr(scr, y + 1, x + 2, f" ✦ {title} ", C(1, True))


# ══════════════════════════════════════════════════════════════════════════════
#  ARROW-KEY MENU (with live description)
# ══════════════════════════════════════════════════════════════════════════════

def arrow_menu(stdscr, title, items, subtitle="", idx=0):
    """
    items: [(label, value, description_or_None), ...]
    Returns selected value, or None on ESC/q.
    """
    curses.curs_set(0)
    setup_colors()

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        bw = min(w - 4, 48)

        draw_box(stdscr, 0, 1, bw, title)
        if subtitle:
            safe_addstr(stdscr, 3, 3, subtitle[:w - 5], C(4))

        menu_start = 5
        visible = max(1, h - menu_start - 7)
        scroll = max(0, idx - visible + 1)

        for i, item in enumerate(items):
            label = item[0]
            pos = i - scroll
            if pos < 0 or pos >= visible:
                continue
            row = menu_start + pos
            if i == idx:
                safe_addstr(stdscr, row, 3, f"  ❯ {label}", C(2, True))
            else:
                safe_addstr(stdscr, row, 3, f"    {label}", C(3))

        # Description area
        desc_row = menu_start + visible + 1
        safe_addstr(stdscr, desc_row, 3, "─" * min(w - 6, 44), C(4))

        desc = items[idx][2] if len(items[idx]) > 2 and items[idx][2] else ""
        if desc:
            for j, line in enumerate(desc.split("\n")[:4]):
                safe_addstr(stdscr, desc_row + 1 + j, 3, line[:w - 5], C(4))

        foot = "↑↓ navigate   Enter select   q back"
        safe_addstr(stdscr, h - 1, 2, foot, C(4))
        stdscr.refresh()

        key = stdscr.getch()
        if key in (curses.KEY_UP, ord('k')):
            idx = (idx - 1) % len(items)
        elif key in (curses.KEY_DOWN, ord('j')):
            idx = (idx + 1) % len(items)
        elif key in (curses.KEY_ENTER, 10, 13):
            return items[idx][1]
        elif key in (ord('q'), 27):
            return None


# ══════════════════════════════════════════════════════════════════════════════
#  TEXT INPUT (curses)
# ══════════════════════════════════════════════════════════════════════════════

def text_input(stdscr, prompt, hint="", default="", password=False):
    curses.curs_set(1)
    setup_colors()
    buf = list(default)
    cursor = len(buf)

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        safe_addstr(stdscr, 1, 2, prompt, C(1, True))
        if hint:
            for i, line in enumerate(hint.split("\n")):
                safe_addstr(stdscr, 3 + i, 2, line[:w - 4], C(4))

        input_row = 3 + (len(hint.split("\n")) if hint else 0) + 1
        safe_addstr(stdscr, input_row, 2, "▸ ", C(5))

        disp = "•" * len(buf) if password else "".join(buf)
        safe_addstr(stdscr, input_row, 4, disp[:w - 6], C(5, True))

        cx = 4 + min(cursor, w - 7)
        if password:
            cx = 4 + min(len(buf), w - 7)
        try:
            stdscr.move(input_row, cx)
        except curses.error:
            pass

        safe_addstr(stdscr, h - 1, 2, "Enter confirm   ESC cancel", C(4))
        stdscr.refresh()

        key = stdscr.getch()
        if key in (curses.KEY_ENTER, 10, 13):
            curses.curs_set(0)
            return "".join(buf)
        elif key == 27:
            curses.curs_set(0)
            return None
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if cursor > 0:
                buf.pop(cursor - 1)
                cursor -= 1
        elif key == curses.KEY_LEFT:
            cursor = max(0, cursor - 1)
        elif key == curses.KEY_RIGHT:
            cursor = min(len(buf), cursor + 1)
        elif key == curses.KEY_HOME:
            cursor = 0
        elif key == curses.KEY_END:
            cursor = len(buf)
        elif 32 <= key <= 126:
            buf.insert(cursor, chr(key))
            cursor += 1


# ══════════════════════════════════════════════════════════════════════════════
#  SCROLLABLE TEXT VIEWER (curses)
# ══════════════════════════════════════════════════════════════════════════════

def text_viewer(stdscr, title, text):
    curses.curs_set(0)
    setup_colors()

    lines = []
    h, w = stdscr.getmaxyx()
    content_w = max(20, w - 6)
    for raw_line in text.split("\n"):
        if len(raw_line) <= content_w:
            lines.append(raw_line)
        else:
            while raw_line:
                lines.append(raw_line[:content_w])
                raw_line = raw_line[content_w:]
    scroll = 0

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        safe_addstr(stdscr, 0, 2, f" ✦ {title} ", C(1, True))
        safe_addstr(stdscr, 1, 2, "─" * min(w - 4, 44), C(4))

        visible = h - 4
        for i in range(visible):
            li = scroll + i
            if li >= len(lines):
                break
            safe_addstr(stdscr, 2 + i, 2, lines[li][:w - 4], C(3))

        pct = int((scroll / max(len(lines) - visible, 1)) * 100) if len(lines) > visible else 100
        safe_addstr(stdscr, h - 1, 2, f"↑↓ scroll   q back   {pct}%", C(4))
        stdscr.refresh()

        key = stdscr.getch()
        if key in (curses.KEY_UP, ord('k')):
            scroll = max(0, scroll - 1)
        elif key in (curses.KEY_DOWN, ord('j'), ord(' ')):
            scroll = min(max(0, len(lines) - visible), scroll + 1)
        elif key == curses.KEY_PPAGE:
            scroll = max(0, scroll - visible)
        elif key == curses.KEY_NPAGE:
            scroll = min(max(0, len(lines) - visible), scroll + visible)
        elif key in (ord('q'), 27, curses.KEY_ENTER, 10, 13):
            return


# ══════════════════════════════════════════════════════════════════════════════
#  INFO SCREEN (press any key to continue)
# ══════════════════════════════════════════════════════════════════════════════

def info_screen(stdscr, lines_list, footer="Press Enter to continue"):
    """Show a simple screen of text lines, wait for a key."""
    curses.curs_set(0)
    setup_colors()
    stdscr.erase()
    h, w = stdscr.getmaxyx()
    for i, (text, color_idx, bold) in enumerate(lines_list):
        if i >= h - 2:
            break
        safe_addstr(stdscr, i + 1, 2, text[:w - 4], C(color_idx, bold))
    safe_addstr(stdscr, h - 1, 2, footer, C(4))
    stdscr.refresh()
    stdscr.getch()


# ══════════════════════════════════════════════════════════════════════════════
#  FIRST-RUN SETUP WIZARD
# ══════════════════════════════════════════════════════════════════════════════

def setup_wizard(stdscr):
    setup_colors()
    cfg = DEFAULT_CFG.copy()

    # ── Step 1: Welcome ──
    info_screen(stdscr, [
        ("",             3, False),
        ("  ╭──────────────────────────────────────╮", 1, False),
        ("  │   ✦  Welcome to ifAI Chat  ✦         │", 1, True),
        ("  ╰──────────────────────────────────────╯", 1, False),
        ("",             3, False),
        ("  Hi there! 👋",                            5, True),
        ("",             3, False),
        ("  This app lets you chat with AI right",    3, False),
        ("  here in your terminal.",                  3, False),
        ("",             3, False),
        ("  Don't worry if you're new to this —",     3, False),
        ("  we'll walk you through everything,",      3, False),
        ("  one step at a time.",                     3, False),
        ("",             3, False),
        ("  Your settings are saved locally and",     4, False),
        ("  you can change them anytime.",             4, False),
    ])

    # ── Step 2: Provider ──
    items = []
    for p in PROVIDERS:
        items.append((f"  {p['name']}", p, p["desc"]))

    provider = arrow_menu(stdscr, "Choose Your AI Provider", items,
                          "Where should the AI come from?")
    if provider is None:
        return None

    cfg["endpoint"] = provider["endpoint"]

    # ── Step 2b: Custom endpoint ──
    if not provider["endpoint"]:
        ep = text_input(stdscr, "Enter your endpoint URL",
                        "An endpoint is the web address where the AI lives.\n"
                        "Example: https://api.mycompany.com/v1",
                        default="https://")
        if ep is None:
            return None
        cfg["endpoint"] = ep

    # ── Step 3: API key ──
    if provider["needs_key"]:
        key_hint = (
            "What's an API key?\n"
            "─────────────────\n"
            "It's like a password that proves you have an\n"
            "account with the AI provider.\n"
            "\n"
            "Where to get yours:\n"
            "  OpenAI     → platform.openai.com/api-keys\n"
            "  OpenRouter → openrouter.ai/keys\n"
            "\n"
            "Your key stays on this device only.\n"
            "It's saved in ~/chat/config.json"
        )
        key = text_input(stdscr, "Enter Your API Key", key_hint, password=True)
        if key is None:
            return None
        cfg["api_key"] = key
    else:
        cfg["api_key"] = "not-needed"

    # ── Step 4: Model ──
    if provider.get("models"):
        model_items = []
        for mname, mdesc in provider["models"]:
            model_items.append((f"  {mname}", mname, mdesc))
        model_items.append(("  Enter custom model name", "__custom__",
                            "Type in any model name you know."))

        model = arrow_menu(stdscr, "Choose a Model", model_items,
                           "Which AI model should we use?")
        if model is None:
            return None
        if model == "__custom__":
            model = text_input(stdscr, "Enter model name",
                               "Type the exact model name your provider supports.\n"
                               "Example: gpt-4o, llama3, mistral")
            if model is None:
                return None
        cfg["model"] = model
    else:
        model = text_input(stdscr, "Enter model name",
                           "Type the model name your endpoint serves.\n"
                           "If unsure, check your provider's documentation.")
        if model is None:
            return None
        cfg["model"] = model

    # ── Step 5: System prompt ──
    sp_items = []
    for sp_name, sp_val, sp_desc in SYSTEM_PRESETS:
        sp_items.append((f"  {sp_name}", sp_val, sp_desc))

    sysprompt = arrow_menu(stdscr, "Choose a Personality", sp_items,
                           "The system prompt shapes how the AI behaves.")
    if sysprompt is None:
        return None
    if sysprompt == "":  # "Write my own"
        sysprompt = text_input(stdscr, "Write your system prompt",
                               "This is the AI's 'job description'.\n"
                               "Example: You are a friendly cooking expert\n"
                               "who suggests recipes based on ingredients.")
        if sysprompt is None:
            return None
    cfg["system_prompt"] = sysprompt

    # ── Step 6: Streaming ──
    stream_choice = arrow_menu(stdscr, "Response Style", [
        ("  Streaming (recommended)",
         True,
         "Watch responses appear word by word,\nlike ChatGPT typing. Most people prefer this."),
        ("  Wait for full response",
         False,
         "Wait until the AI finishes thinking,\nthen show the complete response at once."),
    ], "How should responses appear?")
    if stream_choice is None:
        return None
    cfg["stream"] = stream_choice

    # ── Step 7: Summary ──
    masked_key = ""
    if cfg["api_key"] and cfg["api_key"] != "not-needed":
        k = cfg["api_key"]
        masked_key = k[:4] + "····" + k[-4:] if len(k) > 8 else "····"
    else:
        masked_key = "(not needed)"

    info_screen(stdscr, [
        ("",             3, False),
        ("  ╭──────────────────────────────────────╮", 5, False),
        ("  │   ✦  You're all set!  ✦              │", 5, True),
        ("  ╰──────────────────────────────────────╯", 5, False),
        ("",             3, False),
        (f"  Provider:  {provider['name']}",          3, False),
        (f"  Endpoint:  {cfg['endpoint'][:38]}",      3, False),
        (f"  API Key:   {masked_key}",                3, False),
        (f"  Model:     {cfg['model']}",              3, False),
        (f"  Prompt:    {cfg['system_prompt'][:35]}…", 3, False),
        (f"  Streaming: {'Yes' if cfg['stream'] else 'No'}", 3, False),
        ("",             3, False),
        ("  Your settings are saved. You can change", 4, False),
        ("  them anytime from Configure in the menu.", 4, False),
        ("",             3, False),
        ("  Happy chatting! 💡",                      5, True),
    ], "Press Enter to start →")

    cfg["_configured"] = True
    save_cfg(cfg)
    return cfg


# ══════════════════════════════════════════════════════════════════════════════
#  CONFIG EDITOR SCREEN
# ══════════════════════════════════════════════════════════════════════════════

CFG_FIELDS = [
    ("endpoint",      "Endpoint",     "The web address of your AI provider's API."),
    ("api_key",       "API Key",      "Your authentication key for the provider."),
    ("model",         "Model",        "Which AI model to use for conversations."),
    ("system_prompt", "System Prompt","Instructions that shape how the AI behaves."),
    ("stream",        "Streaming",    "Show responses word-by-word as they arrive."),
    ("max_history",   "Max History",  "How many messages to keep in context."),
]

def config_editor(stdscr, cfg):
    cfg = cfg.copy()
    while True:
        items = []
        for key, label, desc in CFG_FIELDS:
            val = cfg.get(key, "")
            if key == "api_key" and val and val != "not-needed":
                disp = val[:4] + "····" + val[-4:] if len(val) > 8 else "····"
            elif key == "stream":
                disp = "Yes" if val else "No"
            else:
                disp = str(val)[:30]
            items.append((f"  {label:<16} {disp}", key, desc))
        items.append(("  ── Save & Back ──", "__save__", "Save changes and return to menu."))
        items.append(("  ── Discard ──",     "__discard__", "Discard changes and return."))

        choice = arrow_menu(stdscr, "Configure", items, "Select a field to edit")

        if choice is None or choice == "__discard__":
            return None
        if choice == "__save__":
            save_cfg(cfg)
            return cfg

        if choice == "stream":
            cfg["stream"] = not cfg.get("stream", True)
        elif choice == "api_key":
            val = text_input(stdscr, "Edit: API Key",
                             "Your provider authentication key.\n"
                             "Leave empty if using a local provider.",
                             password=True)
            if val is not None:
                cfg[choice] = val
        else:
            label = dict((k, l) for k, l, _ in CFG_FIELDS).get(choice, choice)
            val = text_input(stdscr, f"Edit: {label}", "", str(cfg.get(choice, "")))
            if val is not None:
                if choice == "max_history" and val.isdigit():
                    cfg[choice] = int(val)
                else:
                    cfg[choice] = val


# ══════════════════════════════════════════════════════════════════════════════
#  HELP & DOCS MENU
# ══════════════════════════════════════════════════════════════════════════════

def help_menu(stdscr):
    while True:
        items = []
        for title, _ in HELP_TOPICS:
            items.append((f"  {title}", title, ""))
        items.append(("  ── Back ──", None, "Return to main menu."))

        choice = arrow_menu(stdscr, "Help & Docs", items, "Learn about AI and this app")
        if choice is None:
            return

        for title, body in HELP_TOPICS:
            if title == choice:
                text_viewer(stdscr, title, body)
                break


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION PICKER
# ══════════════════════════════════════════════════════════════════════════════

def pick_session(stdscr, conn, title="Select Session"):
    sessions = list_sessions(conn)
    if not sessions:
        info_screen(stdscr, [
            ("", 3, False),
            ("  No saved sessions yet!", 1, True),
            ("", 3, False),
            ("  Start a New Chat from the main menu", 3, False),
            ("  to create your first conversation.", 3, False),
        ])
        return None

    items = []
    for sid, name, created in sessions:
        preview = session_preview(conn, sid)
        lbl = f"  #{sid:<3} {(name or '')[:16]:<16} {created[:10]}  {preview[:24]}"
        items.append((lbl, sid, ""))
    items.append(("  ── Back ──", None, "Return to menu."))

    return arrow_menu(stdscr, title, items)


# ══════════════════════════════════════════════════════════════════════════════
#  CHAT LOOP (normal terminal — curses suspended)
# ══════════════════════════════════════════════════════════════════════════════

CY = "\033[1;36m"; BL = "\033[1;34m"; GR = "\033[1;32m"
RD = "\033[0;91m"; DM = "\033[0;90m"; BD = "\033[1m"; RS = "\033[0m"

def chat_loop(conn, cfg, sid, history):
    max_h = cfg.get("max_history", 50)
    use_s = cfg.get("stream", True)

    # Get session name
    row = conn.execute("SELECT name FROM sessions WHERE id=?", (sid,)).fetchone()
    sname = row[0] if row else f"Session #{sid}"

    print(f"\n{CY}{'─' * 55}{RS}")
    print(f"{CY} ✦ {sname}{RS}  {DM}{cfg['model']}{RS}")
    print(f"{DM} /back  /clear  /rename <name>  /help  /exit{RS}")
    print(f"{CY}{'─' * 55}{RS}\n")

    def stream_req(messages):
        url = cfg["endpoint"].rstrip("/") + "/chat/completions"
        hdrs = {"Authorization": f"Bearer {cfg['api_key']}",
                "Content-Type": "application/json"}
        resp = requests.post(url, headers=hdrs, timeout=120,
                             json={"model": cfg["model"], "messages": messages, "stream": True},
                             stream=True)
        resp.raise_for_status()
        full = ""
        for line in resp.iter_lines():
            if not line:
                continue
            raw = line.decode()
            if raw.startswith("data: "):
                data = raw[6:]
                if data.strip() == "[DONE]":
                    break
                try:
                    delta = json.loads(data)["choices"][0]["delta"].get("content", "")
                    if delta:
                        full += delta
                        print(delta, end="", flush=True)
                except Exception:
                    pass
        print()
        return full

    def once_req(messages):
        url = cfg["endpoint"].rstrip("/") + "/chat/completions"
        hdrs = {"Authorization": f"Bearer {cfg['api_key']}",
                "Content-Type": "application/json"}
        resp = requests.post(url, headers=hdrs, timeout=120,
                             json={"model": cfg["model"], "messages": messages, "stream": False})
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    while True:
        try:
            user_input = input(f"{BL}You:{RS} ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not user_input:
            continue

        cmd = user_input.lower().strip()

        if cmd == "/back":
            break
        elif cmd == "/exit":
            print(f"\n{DM}Goodbye! Your chats are saved. 👋{RS}")
            sys.exit(0)
        elif cmd == "/clear":
            history = history[:1]
            print(f"{DM}Context cleared — the AI will start fresh but your{RS}")
            print(f"{DM}conversation is still saved in the database.{RS}")
            continue
        elif cmd == "/help":
            print(f"\n{CY}Available commands:{RS}")
            print(f"  {BD}/back{RS}          {DM}Return to main menu{RS}")
            print(f"  {BD}/clear{RS}         {DM}Clear context (chat stays saved){RS}")
            print(f"  {BD}/rename <name>{RS} {DM}Rename this session{RS}")
            print(f"  {BD}/help{RS}          {DM}Show this help{RS}")
            print(f"  {BD}/exit{RS}          {DM}Quit the app{RS}\n")
            continue
        elif user_input.startswith("/rename "):
            name = user_input[8:].strip()
            if name:
                rename_session(conn, sid, name)
                sname = name
                print(f"{DM}Renamed → {name}{RS}")
            continue
        elif user_input.startswith("/"):
            print(f"{DM}Unknown command. Type /help for options.{RS}")
            continue

        history.append({"role": "user", "content": user_input})
        save_msg(conn, sid, "user", user_input)

        if len(history) > max_h + 1:
            history = history[:1] + history[-max_h:]

        print(f"\n{GR}Assistant:{RS} ", end="", flush=True)
        try:
            if use_s:
                reply = stream_req(history)
            else:
                reply = once_req(history)
                print(reply)
        except requests.HTTPError as e:
            code = e.response.status_code
            history.pop()
            if code == 401:
                print(f"\n{RD}Hmm, your API key doesn't seem to be working.{RS}")
                print(f"{DM}Run 'chat --setup' to update it.{RS}")
            elif code == 404:
                print(f"\n{RD}Model '{cfg['model']}' wasn't found at this endpoint.{RS}")
                print(f"{DM}Check your model name in Configure.{RS}")
            elif code == 429:
                print(f"\n{RD}You've hit a rate limit — the provider needs a breather.{RS}")
                print(f"{DM}Wait a moment and try again.{RS}")
            else:
                print(f"\n{RD}API error ({code}): {e.response.text[:200]}{RS}")
            continue
        except requests.ConnectionError:
            history.pop()
            print(f"\n{RD}Can't connect to {cfg['endpoint']}{RS}")
            print(f"{DM}Check your internet or make sure the local server is running.{RS}")
            continue
        except Exception as e:
            history.pop()
            print(f"\n{RD}Something went wrong: {e}{RS}")
            continue

        print()
        history.append({"role": "assistant", "content": reply})
        save_msg(conn, sid, "assistant", reply)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN TUI MENU
# ══════════════════════════════════════════════════════════════════════════════

MENU_ITEMS = [
    ("  New Chat",        "new",      "Start a fresh conversation with the AI."),
    ("  Resume Session",  "resume",   "Continue a previous conversation where you left off."),
    ("  Fork Session",    "fork",     "Branch off from a past conversation — great for exploring different paths!"),
    ("  Help & Docs",     "help",     "Learn how to use this app, understand AI concepts, and more."),
    ("  Configure",       "config",   "Change your AI provider, model, API key, and other settings."),
    ("  Exit",            "exit",     "Close the app. Your chats are always saved automatically."),
]

def main_menu(stdscr, conn, cfg):
    setup_colors()
    n = count_sessions(conn)
    subtitle = f"Model: {cfg['model']}   Sessions: {n}"
    return arrow_menu(stdscr, "ifAI Chat", MENU_ITEMS, subtitle)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        prog="chat",
        description="ifAI Chat — A friendly terminal AI chat client.",
        epilog="Built with ♥ by ifAI.One · Educational AI tools for everyone."
    )
    parser.add_argument("--config", action="store_true",
                        help="Skip setup wizard, go straight to the menu")
    parser.add_argument("--setup", action="store_true",
                        help="Re-run the first-time setup wizard")
    parser.add_argument("--version", action="version",
                        version=f"ifAI Chat v{__version__}")
    args = parser.parse_args()

    conn = init_db()
    cfg  = load_cfg()

    # First-run wizard (or forced with --setup)
    if args.setup or (not args.config and not cfg.get("_configured", False)):
        try:
            result = curses.wrapper(setup_wizard)
            if result:
                cfg = result
            else:
                print("Setup cancelled. Run 'chat --setup' when you're ready!")
                sys.exit(0)
        except KeyboardInterrupt:
            print("\nSetup cancelled.")
            sys.exit(0)

    # Main loop
    while True:
        try:
            choice = curses.wrapper(main_menu, conn, cfg)
        except KeyboardInterrupt:
            break

        if choice is None or choice == "exit":
            break

        elif choice == "new":
            sid = new_session(conn)
            history = [{"role": "system", "content": cfg.get("system_prompt", "")}]
            chat_loop(conn, cfg, sid, history)

        elif choice == "resume":
            sid = curses.wrapper(pick_session, conn, "Resume Session")
            if sid is not None:
                msgs = load_msgs(conn, sid)
                history = [{"role": "system", "content": cfg.get("system_prompt", "")}] + msgs
                chat_loop(conn, cfg, sid, history)

        elif choice == "fork":
            src = curses.wrapper(pick_session, conn, "Fork — pick source session")
            if src is not None:
                msgs = load_msgs(conn, src)
                new_sid = new_session(conn, forked_from=src)
                for m in msgs:
                    save_msg(conn, new_sid, m["role"], m["content"])
                history = [{"role": "system", "content": cfg.get("system_prompt", "")}] + msgs
                print(f"\n{DM}Forked session #{src} → new session #{new_sid}{RS}")
                chat_loop(conn, cfg, new_sid, history)

        elif choice == "help":
            curses.wrapper(help_menu)

        elif choice == "config":
            result = curses.wrapper(config_editor, cfg)
            if result:
                cfg = result

    print(f"\nGoodbye! Your chats are saved. 👋")


if __name__ == "__main__":
    main()
