# Copilot Instructions — ifAI Chat

## Running

```bash
python3 chat.py          # normal start (wizard on first run)
python3 chat.py --config # skip wizard, go to menu
python3 chat.py --setup  # re-run setup wizard
```

There is no test suite, linter, or build step.

## Architecture

This is a single-file Python application (`chat.py`, ~1100 lines). All logic lives in one file, organized into clearly marked sections with `# ══` banner comments:

1. **Constants & presets** (top) — `BASE_DIR`, `DEFAULT_CFG`, `PROVIDERS`, `SYSTEM_PRESETS`, `HELP_TOPICS`
2. **Config** — `load_cfg()` / `save_cfg()` read/write `~/chat/config.json`
3. **Database** — SQLite layer (`init_db`, `new_session`, `save_msg`, `load_msgs`, etc.) using `~/chat/chat_history.db` with two tables: `sessions` and `messages`
4. **Curses TUI** — Reusable UI components: `arrow_menu()` for navigation, `text_input()` for prompts, `text_viewer()` for scrollable content, `info_screen()` for simple displays
5. **Setup wizard** — Multi-step curses flow for first-run configuration
6. **Config editor** — In-app settings management
7. **Chat loop** — `chat_loop()` handles the conversation using raw `print()`/`input()` (not curses). Contains nested `stream_req()` and `once_req()` for OpenAI-compatible API calls
8. **Main entry** — `main()` with argparse, runs the curses main menu in a loop, drops into `chat_loop()` when chatting

Key architectural boundary: the TUI (menus, wizard, config) uses **curses**, but the chat loop uses **plain terminal I/O** (`print`/`input`). This is intentional — curses doesn't handle streaming text well.

## Conventions

- **ANSI color globals** — `CY`, `BL`, `GR`, `RD`, `DM`, `BD`, `RS` are defined near the chat loop and used for terminal coloring in non-curses output. Curses sections use `curses.init_pair()` via `setup_colors()`.
- **Section separators** — Major sections use `# ══════` double-line banners with a title comment. Sub-sections use `# ──────` single-line headers.
- **Provider presets** — Each provider in `PROVIDERS` is a dict with `name`, `endpoint`, `needs_key`, `desc`, and `models`. Adding a new provider means appending to this list.
- **All paths are relative to `~/chat/`** — `BASE_DIR = Path.home() / "chat"`. Config and DB files live there, not in the repo directory.
- **No external dependencies beyond `requests`** — `rich` is listed in requirements.txt but is not currently imported or used. The TUI is pure curses + ANSI escapes.
- **`curses.wrapper()` pattern** — All curses UI is invoked via `curses.wrapper(func, ...)` from the main loop, ensuring proper terminal cleanup.
- **Termux compatibility** — The app is designed to run on Android/Termux. Avoid features that require desktop-only terminal capabilities.
