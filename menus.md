# ✦ Interactive Menu System — Philosophy, Patterns & Implementation Guide

> **"The menu IS the manual."**
> Every screen the user sees should teach them what they need to know, right when they need to know it — no external docs required.

This document extracts the interactive menu paradigm used in **ifAI Chat** and provides an exhaustive instruction set for building similar terminal applications. The guiding principle: a person who has **never opened a terminal before** should be able to use the application confidently on their very first try, without reading any documentation outside the app itself.

---

## Table of Contents

1. [Core Philosophy](#1-core-philosophy)
2. [The Five Pillars of Accessible Terminal UI](#2-the-five-pillars-of-accessible-terminal-ui)
3. [Menu Component Catalog](#3-menu-component-catalog)
4. [The Setup Wizard — Guided First Contact](#4-the-setup-wizard--guided-first-contact)
5. [The Main Menu — Persistent Home Base](#5-the-main-menu--persistent-home-base)
6. [The Config Editor — Power Without Peril](#6-the-config-editor--power-without-peril)
7. [The Help System — Docs in Context](#7-the-help-system--docs-in-context)
8. [The Session Picker — Data Navigation](#8-the-session-picker--data-navigation)
9. [The Chat Loop — Minimal-Command Interaction](#9-the-chat-loop--minimal-command-interaction)
10. [Navigation & Input Paradigm](#10-navigation--input-paradigm)
11. [Advanced User Escape Hatches](#11-advanced-user-escape-hatches)
12. [Defaults & Quick-Start Strategy](#12-defaults--quick-start-strategy)
13. [Error Communication](#13-error-communication)
14. [Visual Language & Formatting](#14-visual-language--formatting)
15. [Implementation Patterns & Code Architecture](#15-implementation-patterns--code-architecture)
16. [Building Your Own — Step-by-Step Instruction Set](#16-building-your-own--step-by-step-instruction-set)
17. [Checklist: Does Your Menu Pass the Mom Test?](#17-checklist-does-your-menu-pass-the-mom-test)

---

## 1. Core Philosophy

### The Problem

Terminal applications are intimidating. A blinking cursor on a black screen tells a new user absolutely nothing. Traditional CLI tools assume you already know what to type, what flags exist, and what the program expects. This excludes the vast majority of people.

### The Solution

**Replace "you need to already know" with "we'll show you right now."**

The ifAI Chat menu system is built on a single insight: **the interactive interface itself is the documentation**. Instead of writing a manual and hoping someone reads it, you embed the explanation directly into the moment of decision. When a user is choosing an AI provider, they see what each provider is, what it costs, and why they might choose it — right there on the selection screen, not in a README they'll never find.

### The Golden Rules

1. **Never ask the user to type something they could select instead.**
   If there are known options, present them as a list. Typing is error-prone, scary for beginners, and unnecessary when the set of valid answers is known.

2. **Never present a choice without explaining the consequences.**
   Every menu item has a description. Every option tells the user what will happen if they pick it. No mystery meat navigation.

3. **Never trap the user.**
   Every screen has a way back. `ESC` or `q` always retreats. `Ctrl+C` always works. There is no state from which you cannot gracefully exit.

4. **Never require external knowledge.**
   If the user needs to understand a concept (like "API key" or "endpoint") to make a decision, explain it inline — right there on the screen where they need it.

5. **Never lose user work.**
   Sessions auto-save. Config changes require explicit "Save" vs "Discard." The user never has to wonder if their data survived a crash or a wrong button press.

6. **Always have sensible defaults.**
   If the user isn't sure what to pick, the default should be the right answer for most people. Make "just press Enter" a safe and useful action.

---

## 2. The Five Pillars of Accessible Terminal UI

These five pillars are the non-negotiable principles every menu screen must satisfy:

### Pillar 1: Navigate, Don't Type

```
What the user sees:

  ╭──────────────────────────────────────────────╮
  │   ✦ Choose Your AI Provider  ✦               │
  ╰──────────────────────────────────────────────╯
  Where should the AI come from?

      OpenAI
    ❯ OpenRouter
      Ollama (local)
      LM Studio (local)
      Custom / Other

  ──────────────────────────────────────────────
  Access 100+ AI models from one place — including
  FREE ones! Great for exploring and experimenting.

    Get your key → openrouter.ai/keys

  Great for: trying different models without commitment.

  ↑↓ navigate   Enter select   q back
```

**How it works:**
- Arrow keys (`↑`/`↓`) or vim keys (`k`/`j`) move a highlight cursor (`❯`) between options.
- `Enter` confirms the selection.
- `q` or `ESC` cancels and goes back.
- The user never has to type a word unless absolutely necessary (like entering an API key or custom URL).

**Why this matters:**
A new user looking at a list of options with a highlighted cursor immediately understands what to do — it's the same pattern as every phone app, every TV remote menu, every ATM. They already know `↑↓` and `Enter`. There is zero learning curve.

**Compare to the alternative:**
```
Enter provider (openai/openrouter/ollama/lmstudio/custom): _
```
This requires the user to (a) know the valid options, (b) type one perfectly, (c) know what each one means before choosing. It's hostile to beginners.

### Pillar 2: Explain in Context

Every menu item carries a description that appears **live** as the user highlights it. This is the single most important innovation in the system.

**The anatomy of a menu item:**

```python
# (display_label, return_value, description_text)
("  OpenRouter", provider_dict, 
 "Access 100+ AI models from one place — including\n"
 "FREE ones! Great for exploring and experimenting.\n\n"
 "  Get your key → openrouter.ai/keys\n\n"
 "Great for: trying different models without commitment.")
```

- **Display label**: What the user sees in the list. Short, recognizable.
- **Return value**: What the code receives when this item is selected. The user never sees this.
- **Description**: Appears below the menu when this item is highlighted. This is where you teach.

**What descriptions must contain:**
1. **What it is** — one-sentence plain-English explanation
2. **What it costs** — free? paid? local? cloud?
3. **How to get started** — concrete next step (URL, command, etc.)
4. **Who it's for** — "Great for: ..." gives the user permission to choose confidently

**The description area updates live** as the user moves up and down. This creates a browsing experience — the user can "window shop" through options, reading about each one without committing to anything.

### Pillar 3: Progressive Disclosure

Not everyone needs the same level of detail. The system serves beginners and advanced users simultaneously through layered information:

**Layer 1 — Menu labels** (everyone sees these):
```
  OpenAI
  OpenRouter
  Ollama (local)
```

**Layer 2 — Live descriptions** (visible as you browse):
```
Access 100+ AI models from one place — including
FREE ones! Great for exploring and experimenting.
```

**Layer 3 — Help system** (opt-in deep dives):
```
Help & Docs → Providers & Endpoints → full multi-paragraph explanation
```

**Layer 4 — Config file** (power users skip everything):
```json
// ~/chat/config.json — edit directly, bypass all menus
{"endpoint": "https://openrouter.ai/api/v1", "model": "..."}
```

A beginner naturally reads all four layers. An advanced user skips straight to Layer 4 and never sees a menu. Neither user is punished for their skill level.

### Pillar 4: Safe Exploration

The user must feel safe to explore. This means:

- **Every action is reversible.** Selected the wrong provider? Press `q` to go back. Made a config change you don't like? Choose "Discard" to undo.
- **Nothing destructive is one keypress away.** Deleting data or overwriting config requires explicit confirmation, not a single `Enter` on a default option.
- **Navigation wraps around.** Pressing `↑` at the top of a list wraps to the bottom. Pressing `↓` at the bottom wraps to the top. You can never "fall off the edge."
- **State is always visible.** The main menu shows `Model: gpt-4o   Sessions: 3` so you always know your current configuration at a glance.
- **The back path is always the same.** `q` or `ESC` means "go back" on every screen, every time, no exceptions. Consistency breeds confidence.

### Pillar 5: Text Entry as Last Resort

Text input is reserved for situations where selection is impossible:

| Situation | Input Method | Why |
|-----------|-------------|-----|
| Choose a provider | Arrow-key menu | Known set of options |
| Choose a model | Arrow-key menu | Known set per provider |
| Pick a system prompt | Arrow-key menu | Preset personalities |
| Toggle streaming | Arrow-key menu | Two options (yes/no) |
| Enter API key | Text input | Unique to each user, cannot be pre-filled |
| Enter custom URL | Text input | Infinite possibilities, must be typed |
| Custom model name | Text input | Only when user explicitly chooses "custom" |
| Write own system prompt | Text input | Only when user explicitly chooses "write my own" |

**Even text input screens are guided:**
```
Enter Your API Key

What's an API key?
─────────────────
It's like a password that proves you have an
account with the AI provider.

Where to get yours:
  OpenAI     → platform.openai.com/api-keys
  OpenRouter → openrouter.ai/keys

Your key stays on this device only.
It's saved in ~/chat/config.json

▸ ••••••••••••••

Enter confirm   ESC cancel
```

The hint text explains the concept, tells you where to get the value, reassures you about security, and shows the keyboard controls. The user is never staring at an empty text field with no guidance.

---

## 3. Menu Component Catalog

The system is built from exactly **five reusable UI components**. Every screen in the application is composed from these building blocks:

### 3.1 Arrow Menu (`arrow_menu`)

**Purpose:** Present a list of options with live descriptions. The workhorse of the system.

**Anatomy:**
```
╭──────────────────────────────────────────────╮   ← Title box (draw_box)
│   ✦ Title Text  ✦                            │
╰──────────────────────────────────────────────╯
Subtitle text (current context info)               ← Subtitle line

    Option A                                       ← Unselected item
  ❯ Option B                                       ← Selected item (highlighted)
    Option C
    Option D

──────────────────────────────────────────────     ← Description separator
Description text for the currently                  ← Live description area
highlighted option appears here.                      (updates as cursor moves)
Can be multiple lines (up to 4).

↑↓ navigate   Enter select   q back               ← Footer (always visible)
```

**Behavioral rules:**
- The cursor (`❯`) starts at `idx=0` (first item) unless specified otherwise.
- Pressing `↑` at the top wraps to the bottom of the list.
- Pressing `↓` at the bottom wraps to the top of the list.
- When the list is longer than the visible area, it **scrolls** — items above or below the viewport are hidden but accessible.
- The description area shows up to 4 lines of text for the currently highlighted item.
- Returns the **value** (second element of the tuple) on `Enter`.
- Returns `None` on `q` or `ESC` (this is the "go back" signal).
- Supports both arrow keys and vim-style `j`/`k` navigation for experienced users.

**Item tuple format:**
```python
(display_label: str, return_value: Any, description: str | None)
```

**When to use:** Any time the user must choose from a known set of options.

### 3.2 Text Input (`text_input`)

**Purpose:** Collect a single line of text from the user when selection is impossible.

**Anatomy:**
```
Prompt Text                                        ← Bold prompt

Hint text explaining what to enter                 ← Multi-line hint
and why, with examples and context.                  (can be extensive)
Includes URLs, instructions, reassurance.

▸ user's typed text here█                          ← Input line with cursor

Enter confirm   ESC cancel                         ← Footer
```

**Behavioral rules:**
- The cursor is visible (blinking) during text input.
- Full cursor movement: `←`/`→`, `Home`/`End`, `Backspace`.
- `Enter` confirms and returns the typed string.
- `ESC` cancels and returns `None` (goes back).
- Supports a `default` parameter — pre-fills the input with a value the user can edit or accept.
- Supports a `password` parameter — displays `•` bullets instead of actual characters for sensitive input like API keys.
- The hint text can be multi-line and should explain:
  - What this value is (concept explanation)
  - Where to get it (concrete steps)
  - An example of a valid value
  - Any reassurances (e.g., "stays on your device")

**When to use:** Only when the input is unique to the user and cannot be pre-populated or selected from a list. This should be rare.

### 3.3 Text Viewer (`text_viewer`)

**Purpose:** Display long-form text (help articles, documentation) in a scrollable view.

**Anatomy:**
```
 ✦ Article Title                                   ← Title (bold, colored)
──────────────────────────────────────────────     ← Separator

Long-form content appears here. It can be          ← Scrollable content area
many paragraphs long. The text is word-wrapped       (fills most of the screen)
to fit the terminal width.

This component handles text that's longer than
the screen by providing scrolling.

↑↓ scroll   q back   42%                          ← Footer with scroll position
```

**Behavioral rules:**
- `↑`/`k` scrolls up one line. `↓`/`j`/`Space` scrolls down one line.
- `Page Up`/`Page Down` scroll by a full screen.
- `q`, `ESC`, or `Enter` exits back to the previous screen.
- A percentage indicator shows how far through the document the user has scrolled.
- Text is wrapped at the terminal width so horizontal scrolling is never needed.

**When to use:** For help articles, documentation, or any content that's too long for a single screen. Never for choices — use `arrow_menu` for that.

### 3.4 Info Screen (`info_screen`)

**Purpose:** Show a simple message and wait for acknowledgment. Used for welcome screens, confirmation summaries, and status messages.

**Anatomy:**
```
                                                    ← Blank line for spacing
  ╭──────────────────────────────────────╮          ← Optional decorative box
  │   ✦  Welcome to ifAI Chat  ✦         │
  ╰──────────────────────────────────────╯

  Hi there! 👋                                      ← Content lines
                                                      (each line has its own
  This app lets you chat with AI right                 color and bold setting)
  here in your terminal.

  Don't worry if you're new to this —
  we'll walk you through everything,
  one step at a time.

Press Enter to continue                             ← Footer prompt
```

**Behavioral rules:**
- Displays a list of pre-formatted lines, each with individual color and bold styling.
- Waits for **any key** to proceed (typically `Enter`).
- Cannot be scrolled — content must fit on one screen. Design your messages accordingly.
- The footer text is customizable (e.g., "Press Enter to continue" vs "Press Enter to start →").

**When to use:**
- Welcome/onboarding screens
- Summary/confirmation screens after a multi-step process
- Error or empty-state messages (e.g., "No saved sessions yet!")
- Any "read this, then continue" moment

### 3.5 Draw Box (`draw_box`)

**Purpose:** A visual framing element for titles. Not interactive.

**Anatomy:**
```
╭──────────────────────────────────────────────╮
│   ✦ Box Title  ✦                             │
╰──────────────────────────────────────────────╯
```

**Rules:**
- Uses Unicode box-drawing characters (`╭╮╰╯─│`).
- Width adapts to the terminal (up to 48 characters, with 4-character margin).
- The title is displayed with a `✦` decorative marker.
- Used exclusively inside `arrow_menu` and `info_screen` as a visual anchor — not as a standalone component.

---

## 4. The Setup Wizard — Guided First Contact

The setup wizard is the most critical part of the entire application. It is the user's **first experience** — and it determines whether they continue or give up. Every decision in its design serves one goal: **the user finishes setup successfully on their first try.**

### 4.1 When It Runs

| Scenario | Wizard runs? | How |
|----------|-------------|-----|
| First ever launch | **Yes** | Automatic — `_configured` flag is `False` |
| `python3 chat.py --setup` | **Yes** | Explicit re-run flag |
| `python3 chat.py --config` | **No** | Skip wizard, go to main menu |
| Normal launch after first run | **No** | `_configured` is `True`, goes to main menu |

**The `_configured` flag:**
The config file contains `"_configured": false` by default. The wizard sets it to `true` upon completion. This ensures the wizard runs exactly once automatically, but can always be re-invoked with `--setup`.

### 4.2 Step-by-Step Flow

The wizard is a **linear sequence of screens**, each one building on the previous. The user cannot skip steps (because each step depends on the previous one), but they can cancel at any point with `ESC` to abort the entire wizard.

#### Step 1: Welcome Screen (Info Screen)

```
  ╭──────────────────────────────────────╮
  │   ✦  Welcome to ifAI Chat  ✦         │
  ╰──────────────────────────────────────╯

  Hi there! 👋

  This app lets you chat with AI right
  here in your terminal.

  Don't worry if you're new to this —
  we'll walk you through everything,
  one step at a time.

  Your settings are saved locally and
  you can change them anytime.

Press Enter to continue
```

**Purpose:** Set the tone. Reassure the user. Establish that:
1. This is friendly, not technical.
2. They'll be guided.
3. Nothing is permanent — they can change settings later.
4. Their data is local.

**Design decisions:**
- The emoji (👋) and casual language ("Hi there!") are deliberate — they signal "this is not a scary hacker tool."
- "Don't worry if you're new" explicitly addresses the beginner's anxiety.
- "one step at a time" sets expectations — you'll be walked through it.
- "change them anytime" removes the pressure of making a perfect choice.

#### Step 2: Choose Provider (Arrow Menu)

```
╭──────────────────────────────────────────────╮
│   ✦ Choose Your AI Provider  ✦               │
╰──────────────────────────────────────────────╯
Where should the AI come from?

    OpenAI
    OpenRouter
  ❯ Ollama (local)
    LM Studio (local)
    Custom / Other

──────────────────────────────────────────────
Run AI models entirely on YOUR device. Completely
free, completely private — no internet needed!

  Install → ollama.com
  Then run: ollama pull llama3

Great for: privacy, offline use, and learning.

↑↓ navigate   Enter select   q back
```

**Purpose:** Choose where the AI brain lives. This is the most consequential decision in setup because it determines whether the user needs an API key, what models are available, and whether they need internet access.

**Why each provider description matters:**
- **OpenAI**: Says "paid" upfront so there are no surprises. Gives the exact URL for getting a key.
- **OpenRouter**: Emphasizes "FREE ones!" because cost is the biggest barrier for newcomers. Frames it as "exploring" to make it feel low-commitment.
- **Ollama**: "YOUR device" and "no internet" are the key selling points. Gives the exact install command.
- **LM Studio**: "friendly desktop app" and "visual interface" for people who don't want the command line even for setup.
- **Custom/Other**: Exists so advanced users aren't blocked, but it's listed last so beginners naturally gravitate to the guided options.

**Consequence of selection:**
| Provider | Next step |
|----------|-----------|
| OpenAI | → API key input → Model selection (from preset list) |
| OpenRouter | → API key input → Model selection (from preset list) |
| Ollama | → Model selection (from preset list, no key needed) |
| LM Studio | → Model selection (single option, no key needed) |
| Custom | → Custom endpoint URL input → API key input → Custom model name input |

The wizard **adapts its next steps** based on this choice. A user who picks Ollama will never see the API key screen. A user who picks Custom will get extra text-input screens. This is essential — never show the user steps that don't apply to them.

#### Step 2b: Custom Endpoint (Text Input — Custom only)

```
Enter your endpoint URL

An endpoint is the web address where the AI lives.
Example: https://api.mycompany.com/v1

▸ https://█

Enter confirm   ESC cancel
```

**Only shown when "Custom / Other" is selected.** The hint explains what an endpoint is, provides a concrete example, and pre-fills `https://` as a default to prevent common mistakes (forgetting the protocol).

#### Step 3: API Key (Text Input — Cloud providers only)

```
Enter Your API Key

What's an API key?
─────────────────
It's like a password that proves you have an
account with the AI provider.

Where to get yours:
  OpenAI     → platform.openai.com/api-keys
  OpenRouter → openrouter.ai/keys

Your key stays on this device only.
It's saved in ~/chat/config.json

▸ ••••••••••••••

Enter confirm   ESC cancel
```

**Only shown when the selected provider has `needs_key: True`.** Key design decisions:

- **"It's like a password"** — Uses a familiar concept to explain an unfamiliar one.
- **Exact URLs** — The user doesn't have to google anything. Copy the URL, paste it in a browser, get the key, come back.
- **Security reassurance** — "Your key stays on this device only" addresses the natural fear of entering a secret into an unfamiliar program.
- **Password masking** — The key is displayed as `•` bullets, just like a password field on a website. This is both a security measure and a familiarity signal.

**What happens with local providers:**
For Ollama and LM Studio, the API key is silently set to `"not-needed"` and this screen is never shown. The user is never confused by being asked for a key they don't need.

#### Step 4: Choose Model (Arrow Menu)

```
╭──────────────────────────────────────────────╮
│   ✦ Choose a Model  ✦                        │
╰──────────────────────────────────────────────╯
Which AI model should we use?

  ❯ gpt-4o
    gpt-4o-mini
    gpt-4-turbo
    o3-mini
    Enter custom model name

──────────────────────────────────────────────
Best all-rounder. Smart, fast, great for most tasks.

↑↓ navigate   Enter select   q back
```

**Purpose:** Pick which AI "brain" to use. The model list is pre-filtered to only show models for the selected provider.

**Description strategy for models:**
Each model description focuses on the **practical difference** the user will experience, not technical specs:
- "Best all-rounder" (not "175B parameters, 128K context window")
- "Faster & cheaper" (not "lower latency, reduced token cost")
- "Free!" (the most important word for a new user considering OpenRouter)

**The "Enter custom model name" escape hatch:**
Listed last, this option opens a text input for users who know exactly which model they want. The existence of this option means the preset list doesn't need to be exhaustive — it just needs to cover the common cases.

#### Step 5: Choose Personality (Arrow Menu)

```
╭──────────────────────────────────────────────╮
│   ✦ Choose a Personality  ✦                  │
╰──────────────────────────────────────────────╯
The system prompt shapes how the AI behaves.

  ❯ Helpful Assistant
    Patient Teacher
    Socratic Tutor
    Code Reviewer
    Creative Writer
    Write my own

──────────────────────────────────────────────
A friendly, general-purpose AI that helps with anything.

↑↓ navigate   Enter select   q back
```

**Purpose:** Set the system prompt that shapes AI behavior.

**Why "Personality" instead of "System Prompt":**
A beginner doesn't know what a "system prompt" is. Everyone understands "personality." The subtitle ("The system prompt shapes how the AI behaves") bridges the two concepts — teaching the real term while using the friendly one.

**Preset strategy:**
- **Helpful Assistant** (default, first position) — the safe choice for anyone unsure.
- **Patient Teacher** — explicitly says "explains things simply" to reassure learners.
- **Socratic Tutor** — for the more adventurous, with a clear explanation of what Socratic means in practice.
- **Code Reviewer** — signals that the app isn't just for chat; it's a developer tool too.
- **Creative Writer** — shows the breadth of possibilities.
- **Write my own** (last position) — escape hatch for custom prompts, opens text input.

#### Step 6: Response Style (Arrow Menu)

```
╭──────────────────────────────────────────────╮
│   ✦ Response Style  ✦                        │
╰──────────────────────────────────────────────╯
How should responses appear?

  ❯ Streaming (recommended)
    Wait for full response

──────────────────────────────────────────────
Watch responses appear word by word,
like ChatGPT typing. Most people prefer this.

↑↓ navigate   Enter select   q back
```

**Purpose:** Choose between streaming and non-streaming output.

**Why this exists as a menu:**
This could have been a default that nobody sees. But streaming vs. waiting is a visible behavioral difference that some people have strong opinions about. The "(recommended)" tag guides beginners while still giving choice.

**Description strategy:**
- "like ChatGPT typing" — relates to a known experience.
- "Most people prefer this" — social proof to help the indecisive.

#### Step 7: Summary Screen (Info Screen)

```
  ╭──────────────────────────────────────╮
  │   ✦  You're all set!  ✦              │
  ╰──────────────────────────────────────╯

  Provider:  OpenRouter
  Endpoint:  https://openrouter.ai/api/v1
  API Key:   sk-o····AbCd
  Model:     mistralai/mistral-7b-instruct:free
  Prompt:    You are a helpful assistant.…
  Streaming: Yes

  Your settings are saved. You can change
  them anytime from Configure in the menu.

  Happy chatting! 💡

Press Enter to start →
```

**Purpose:** Confirm what was configured. Give the user one last chance to review before entering the app.

**Design decisions:**
- **API key is masked** — shows first 4 and last 4 characters with `····` in between. Confirms the right key was entered without exposing it.
- **"You can change them anytime"** — reinforces that nothing is permanent.
- **"Happy chatting! 💡"** — ends on a positive, encouraging note.
- **"Press Enter to start →"** — the arrow suggests forward motion into the app.

### 4.3 Wizard Cancellation

If the user presses `ESC` or `q` at **any** step of the wizard:

1. The wizard function returns `None`.
2. The main entry point prints: `"Setup cancelled. Run 'chat --setup' when you're ready!"`
3. The application exits cleanly.

**The message is crucial.** It doesn't say "Error" or "Aborted." It says "when you're ready" — implying the user made a valid choice and can come back anytime. This prevents the anxiety of "did I break something?"

If the user presses `Ctrl+C`:

1. A `KeyboardInterrupt` is caught.
2. The app prints: `"Setup cancelled."`
3. The application exits cleanly.

**No stack trace, no error message, no guilt.**

---

## 5. The Main Menu — Persistent Home Base

The main menu is the **hub** of the application. After setup, every action starts here, and every action returns here.

### 5.1 Layout

```
╭──────────────────────────────────────────────╮
│   ✦ ifAI Chat  ✦                             │
╰──────────────────────────────────────────────╯
Model: gpt-4o   Sessions: 3

  ❯ New Chat
    Resume Session
    Fork Session
    Help & Docs
    Configure
    Exit

──────────────────────────────────────────────
Start a fresh conversation with the AI.

↑↓ navigate   Enter select   q back
```

### 5.2 Menu Items — Detailed Breakdown

Each item, what it does, what happens when selected, and who it's for:

#### New Chat
- **Description shown:** "Start a fresh conversation with the AI."
- **What happens:** Creates a new session in the database with an auto-generated name (e.g., "Chat 2025-01-15 14:30"), initializes history with the system prompt, and drops into the chat loop.
- **Who it's for:** Everyone. This is the primary action.
- **Why it's first:** Most common action should be at the default cursor position (index 0).

#### Resume Session
- **Description shown:** "Continue a previous conversation where you left off."
- **What happens:** Opens the session picker showing all saved sessions. User selects one, and the full message history is loaded. Drops into chat loop with existing context.
- **Who it's for:** Returning users who want to continue a previous conversation.
- **Empty state:** If no sessions exist yet, shows a friendly message: "No saved sessions yet! Start a New Chat from the main menu."

#### Fork Session
- **Description shown:** "Branch off from a past conversation — great for exploring different paths!"
- **What happens:** Opens the session picker. User selects a source session. A new session is created with a copy of all messages from the source. The original session is untouched. Drops into chat loop with the copied context.
- **Who it's for:** Users who want to explore "what if I had asked differently?" scenarios.
- **Why the analogy:** "Branch off" and "exploring different paths" make the concept intuitive even if you don't know what "fork" means in software terms.

#### Help & Docs
- **Description shown:** "Learn how to use this app, understand AI concepts, and more."
- **What happens:** Opens the help menu (a sub-menu of documentation topics). Each topic opens in the text viewer.
- **Who it's for:** Beginners who want to learn, and anyone who needs a refresher.

#### Configure
- **Description shown:** "Change your AI provider, model, API key, and other settings."
- **What happens:** Opens the config editor where each setting can be individually modified.
- **Who it's for:** Anyone who wants to change their setup after the initial wizard.

#### Exit
- **Description shown:** "Close the app. Your chats are always saved automatically."
- **What happens:** Breaks the main loop, prints a friendly goodbye ("Goodbye! Your chats are saved. 👋"), and exits.
- **Who it's for:** Everyone, when they're done.
- **Why the reassurance:** "Your chats are always saved automatically" prevents the "wait, did I save?" anxiety.

### 5.3 The Subtitle Line

```
Model: gpt-4o   Sessions: 3
```

This single line provides **at-a-glance status**:
- **Model** — confirms which AI brain is active, so the user doesn't have to go into Configure to check.
- **Sessions** — shows how many conversations exist, giving a sense of accumulated history.

This is a form of **ambient awareness** — the user always knows the system state without having to ask.

---

## 6. The Config Editor — Power Without Peril

### 6.1 Layout

```
╭──────────────────────────────────────────────╮
│   ✦ Configure  ✦                             │
╰──────────────────────────────────────────────╯
Select a field to edit

  ❯ Endpoint         https://api.openai.com/v1
    API Key          sk-A····xYz9
    Model            gpt-4o
    System Prompt    You are a helpful assistant.
    Streaming        Yes
    Max History      50
    ── Save & Back ──
    ── Discard ──

──────────────────────────────────────────────
The web address of your AI provider's API.

↑↓ navigate   Enter select   q back
```

### 6.2 Design Principles

**Current values are visible inline:**
Each field shows its current value right next to the label. The user can see all their settings at a glance without entering any sub-screen.

**API key is masked:**
Shows `sk-A····xYz9` (first 4, dots, last 4) for security. If the key is `"not-needed"`, that's shown directly.

**Booleans use toggle:**
Selecting "Streaming" simply flips it between `Yes` and `No` — no sub-menu, no text input. One press of `Enter` toggles the value. This is the fastest possible interaction for binary choices.

**Text fields open a text input:**
Selecting "Endpoint," "Model," "System Prompt," or "Max History" opens the text input component with the current value pre-filled as the default. The user can edit the existing value or clear it and start fresh.

**Explicit Save vs. Discard:**
The last two menu items are:
- **Save & Back** — writes changes to `config.json` and returns to the main menu.
- **Discard** — throws away all changes and returns to the main menu.

**Why explicit save matters:**
If changes were saved automatically on every edit, a user who accidentally changed their API key would lose the old one. Explicit save gives a safety net. You can explore, change things experimentally, and then decide whether to keep the changes.

**Pressing `q` or `ESC`:**
Behaves like "Discard" — returns to the main menu without saving. This is consistent with the "q = go back safely" paradigm.

---

## 7. The Help System — Docs in Context

### 7.1 Help Menu Layout

```
╭──────────────────────────────────────────────╮
│   ✦ Help & Docs  ✦                           │
╰──────────────────────────────────────────────╯
Learn about AI and this app

    What is this app?
    Providers & Endpoints
    API Keys Explained
    Understanding Models
  ❯ Chat Tips & Prompting
    Session Management
    Keyboard Shortcuts
    ── Back ──

──────────────────────────────────────────────

↑↓ navigate   Enter select   q back
```

### 7.2 Topic Design

Each help topic is a self-contained mini-article displayed in the `text_viewer` component. The articles follow a consistent format:

```
✦ Topic Title
───────────────

[Opening paragraph: What is this concept in plain English?]

[Details organized with headers, bullet points, and examples]

[Practical tips marked with 💡]

💡 Tip: [Actionable advice the user can try immediately]
```

### 7.3 Help Topics — What Each Covers and Why

| Topic | What It Teaches | Why It Exists |
|-------|----------------|---------------|
| **What is this app?** | High-level overview, what makes it special | Orients brand-new users |
| **Providers & Endpoints** | Cloud vs. local, what an endpoint is | Needed to understand the provider choice |
| **API Keys Explained** | What keys are, where to get them, key safety | The #1 confusion point for beginners |
| **Understanding Models** | What models are, how they differ, context windows | Needed to make an informed model choice |
| **Chat Tips & Prompting** | How to write good prompts, system prompts | Improves the quality of the user's experience |
| **Session Management** | New/resume/fork, in-chat commands | Teaches features the user might not discover |
| **Keyboard Shortcuts** | Complete key reference for all contexts | Quick reference for muscle memory |

### 7.4 Writing Style for Help Content

- **Use analogies:** "An API key is like a password" — relate new concepts to known ones.
- **Use concrete examples:** Don't say "write a specific prompt." Say "instead of 'tell me about Python,' try 'explain Python list comprehensions with 3 examples.'"
- **Use visual formatting:** Bullet points, indented examples, separator lines. The terminal is limited, but you can still create visual hierarchy.
- **End with a 💡 Tip:** Every article ends with a practical, actionable piece of advice. This gives the reader something to try immediately.
- **Keep paragraphs short:** 2-3 sentences max. Long blocks of text are hard to read in a terminal.

---

## 8. The Session Picker — Data Navigation

### 8.1 Layout

```
╭──────────────────────────────────────────────╮
│   ✦ Resume Session  ✦                        │
╰──────────────────────────────────────────────╯

  ❯ #3   Chat 2025-01-15  2025-01-15  Explain how Python decorators...
    #2   My Project        2025-01-14  Can you help me write a REST...
    #1   Chat 2025-01-13  2025-01-13  What is machine learning?
    ── Back ──

──────────────────────────────────────────────

↑↓ navigate   Enter select   q back
```

### 8.2 Session Display Format

Each session line contains four pieces of information:
```
#ID   Session Name          Created Date    First Message Preview
#3    Chat 2025-01-15       2025-01-15      Explain how Python decorators...
```

- **ID** — unique identifier, useful for advanced users or debugging.
- **Session Name** — auto-generated timestamp name, or custom name if the user used `/rename`.
- **Created Date** — when the session started, for chronological context.
- **First Message Preview** — the first 24 characters of the user's first message, truncated with `...`. This is the most useful identifier because users remember *what they talked about*, not when.

### 8.3 Empty State

When there are no sessions to show:
```

  No saved sessions yet!

  Start a New Chat from the main menu
  to create your first conversation.

Press Enter to continue
```

**Why this matters:** An empty list with no explanation would confuse a beginner. The message tells them (a) nothing is wrong, (b) what to do next.

### 8.4 Ordering

Sessions are listed **most recent first** (`ORDER BY id DESC`). The most likely session to resume is the most recent one, so it should be at the top (default cursor position).

---

## 9. The Chat Loop — Minimal-Command Interaction

The chat loop is deliberately **not** a curses screen. It uses plain `print()`/`input()` for a good reason: curses doesn't handle streaming text output well, and the scrolling behavior of a regular terminal is exactly what you want for a conversation.

### 9.1 Chat Loop Header

```
───────────────────────────────────────────────────────
 ✦ Chat 2025-01-15 14:30  gpt-4o
 /back  /clear  /rename <name>  /help  /exit
───────────────────────────────────────────────────────
```

The header shows:
- **Session name** — so you know which conversation you're in.
- **Model name** — so you know which AI brain you're talking to.
- **Available commands** — listed right there, not hidden in a manual.

### 9.2 In-Chat Commands

Commands are prefixed with `/` to distinguish them from messages to the AI:

| Command | What It Does | What the User Sees |
|---------|-------------|-------------------|
| `/back` | Returns to the main menu | Chat loop exits, main menu appears |
| `/clear` | Clears AI context (keeps only system prompt) | "Context cleared — the AI will start fresh but your conversation is still saved in the database." |
| `/rename <name>` | Renames the current session | "Renamed → My Important Chat" |
| `/help` | Shows command list | Formatted list of all commands with descriptions |
| `/exit` | Quits the app entirely | "Goodbye! Your chats are saved. 👋" |

**Why `/` prefix:**
- Clear visual distinction from natural language.
- Familiar pattern from Discord, Slack, IRC, and many other chat applications.
- Only 5 commands to learn, and `/help` is self-documenting.

**Unknown command handling:**
If the user types `/something` that isn't recognized:
```
Unknown command. Type /help for options.
```
No error, no crash, no confusion. Just gentle redirection.

### 9.3 Error Messages in Chat

Every error is **explained in human terms** with a **suggested action**:

| HTTP Status | Message | Guidance |
|-------------|---------|----------|
| 401 | "Hmm, your API key doesn't seem to be working." | "Run 'chat --setup' to update it." |
| 404 | "Model 'xyz' wasn't found at this endpoint." | "Check your model name in Configure." |
| 429 | "You've hit a rate limit — the provider needs a breather." | "Wait a moment and try again." |
| Connection Error | "Can't connect to {endpoint}" | "Check your internet or make sure the local server is running." |
| Other | "Something went wrong: {error}" | (Raw error for debugging) |

**Design principle:** The error message tells the user (a) what happened, (b) why it might have happened, and (c) what to do about it. Never just show a status code or exception.

---

## 10. Navigation & Input Paradigm

### 10.1 Universal Key Bindings

These keys work the **same way** on **every** curses screen in the app:

| Key | Action | Context |
|-----|--------|---------|
| `↑` or `k` | Move up / Scroll up | All menus and viewers |
| `↓` or `j` | Move down / Scroll down | All menus and viewers |
| `Enter` | Confirm / Select | All screens |
| `q` | Go back / Cancel | All curses screens |
| `ESC` | Go back / Cancel | All screens including text input |
| `Ctrl+C` | Emergency exit from chat, interrupt | Chat loop, setup wizard |

**Why vim keys (`j`/`k`):**
Advanced terminal users expect these. They're provided as **aliases**, not replacements — arrow keys always work too. This is progressive enhancement: beginners use arrows, power users use `j`/`k`.

### 10.2 Context-Specific Keys

| Key | Action | Where |
|-----|--------|-------|
| `←` / `→` | Move cursor | Text input only |
| `Home` / `End` | Jump to start/end of input | Text input only |
| `Backspace` | Delete character before cursor | Text input only |
| `Page Up` / `Page Down` | Scroll by full page | Text viewer only |
| `Space` | Scroll down one line | Text viewer only |

### 10.3 The "Two Modes" Model

The application operates in exactly two distinct modes:

**Mode 1: Curses Mode (Menus)**
- Full-screen rendering
- Arrow-key navigation
- No typing (except in text_input screens)
- Managed by `curses.wrapper()`
- Used for: main menu, setup wizard, config editor, help, session picker

**Mode 2: Plain Terminal Mode (Chat)**
- Normal scrolling terminal
- Type messages and press Enter
- Streaming output
- Uses `print()` / `input()`
- Used for: the actual AI conversation

**Why two modes:**
Curses gives a polished menu experience but cannot handle streaming text output or long scrolling conversations well. Plain terminal mode is perfect for chat but terrible for menus. By using each where it's strongest, the app delivers the best experience in both contexts.

**The transition is seamless:**
When the user selects "New Chat" from the curses main menu, `curses.wrapper()` exits (restoring the normal terminal), and `chat_loop()` runs in plain mode. When the user types `/back`, the chat loop ends, and `curses.wrapper()` is called again for the main menu. The user perceives this as a smooth transition, not a mode switch.

---

## 11. Advanced User Escape Hatches

The menu system is designed for beginners, but it must not **frustrate** advanced users. Every layer of hand-holding has a bypass:

### 11.1 Skip the Wizard Entirely

```bash
python3 chat.py --config
```

The `--config` flag skips the wizard and drops the user directly into the main menu, even on first run. The user can then go to Configure and set everything manually, or edit the config file directly.

### 11.2 Edit Config File Directly

All settings live in `~/chat/config.json`:
```json
{
  "endpoint": "https://api.openai.com/v1",
  "api_key": "sk-...",
  "model": "gpt-4o",
  "system_prompt": "You are a helpful assistant.",
  "stream": true,
  "max_history": 50,
  "_configured": true
}
```

An advanced user can:
1. Create this file manually before ever running the app.
2. Set `"_configured": true` to skip the wizard.
3. Never interact with a menu at all.

**The config file is intentionally simple JSON** — no YAML, no TOML, no custom format. Every developer can read and write JSON.

### 11.3 Vim-Style Navigation

`j`/`k` for down/up in all menus. Not documented prominently (it's in the Keyboard Shortcuts help topic) but available for anyone who tries.

### 11.4 Quick Navigation in Menus

Menu items wrap around — pressing `↑` at the top jumps to the bottom. This means a power user who knows "Exit is the last item" can hit `↑` once from the top to reach it, instead of pressing `↓` five times.

### 11.5 Re-Run Wizard as Config Reset

```bash
python3 chat.py --setup
```

Advanced users can use the wizard as a "reset to known-good state" tool. It walks through every setting and overwrites the config file with fresh values. This is faster than manually editing six fields.

---

## 12. Defaults & Quick-Start Strategy

### 12.1 The "Just Press Enter" Principle

At every decision point, the first option (index 0) is the recommended default. A user who just presses `Enter` through every screen of the wizard will end up with:

| Setting | Default Value | Why |
|---------|---------------|-----|
| Provider | OpenAI (first in list) | Most well-known, most documented |
| Model | gpt-4o (first in OpenAI list) | "Best all-rounder" |
| System Prompt | Helpful Assistant (first in list) | Safe, general-purpose |
| Streaming | Streaming (first option, "(recommended)") | Most natural UX |

**Exception:** API key has no default because it's unique to each user. This is the one mandatory text entry in the entire wizard.

### 12.2 Pre-Filled Defaults in Text Input

When text input is shown, it often pre-fills a useful default:
- Custom endpoint pre-fills `https://` to suggest the correct protocol.
- Config editor pre-fills the current value so the user can edit rather than retype.
- Model name inputs show examples in the hint text.

### 12.3 Default Config Values

The `DEFAULT_CFG` dictionary provides sensible defaults for all settings:
```python
DEFAULT_CFG = {
    "endpoint":      "https://api.openai.com/v1",
    "api_key":       "",
    "model":         "gpt-4o",
    "system_prompt": "You are a helpful assistant.",
    "stream":        True,
    "max_history":   50,
    "_configured":   False,
}
```

If a key is missing from the config file (e.g., after a version upgrade adds a new setting), `load_cfg()` fills it in from defaults using `setdefault()`. This means the config file is self-healing — it can never be in a broken state due to missing keys.

---

## 13. Error Communication

### 13.1 The Three-Part Error Pattern

Every error message in the application follows this structure:

1. **What happened** (in plain English)
2. **Why it might have happened** (common causes)
3. **What to do about it** (concrete next step)

**Example:**
```
Hmm, your API key doesn't seem to be working.
Run 'chat --setup' to update it.
```
1. What: key isn't working
2. Why: (implied — the key is wrong or expired)
3. What to do: run setup to enter a new key

**Counter-example (what NOT to do):**
```
Error: HTTP 401 Unauthorized
```
This tells a beginner nothing. They don't know what HTTP 401 means, why it happened, or what to do.

### 13.2 Error Colors

Errors use distinct ANSI colors:
- **Red (`\033[0;91m`)** — the error message itself
- **Dim gray (`\033[0;90m`)** — the guidance/suggestion

This visual distinction makes it immediately clear which text is "the problem" and which is "the solution."

### 13.3 Non-Fatal Errors

All errors in the chat loop are **non-fatal**. An API error doesn't crash the app — it shows the error, removes the failed message from history, and lets the user try again. The conversation continues.

---

## 14. Visual Language & Formatting

### 14.1 Unicode Characters Used

| Character | Usage | Purpose |
|-----------|-------|---------|
| `╭╮╰╯─│` | Box drawing | Title frames |
| `✦` | Decorative marker | Title emphasis |
| `❯` | Selection cursor | Shows current menu position |
| `▸` | Input prompt | Shows text input cursor line |
| `•` | Password masking | Hides API key characters |
| `👋💡` | Emoji | Emotional tone in messages |

### 14.2 Color Palette (Curses Mode)

| Pair | Colors | Usage |
|------|--------|-------|
| 1 | Cyan on default | Titles, boxes, decorative elements |
| 2 | Black on Cyan | Selected/highlighted menu item |
| 3 | White on default | Normal text, unselected items |
| 4 | Yellow on default | Subtitles, descriptions, footers |
| 5 | Green on default | Input prompts, positive messages |
| 6 | Red on default | Error messages |

### 14.3 Color Palette (Chat Mode — ANSI)

| Code | Variable | Usage |
|------|----------|-------|
| `\033[1;36m` | `CY` | Session headers, decorative lines |
| `\033[1;34m` | `BL` | "You:" prompt label |
| `\033[1;32m` | `GR` | "Assistant:" label |
| `\033[0;91m` | `RD` | Error messages |
| `\033[0;90m` | `DM` | Dim/gray hints and guidance |
| `\033[1m` | `BD` | Bold text for emphasis |
| `\033[0m` | `RS` | Reset all formatting |

### 14.4 Layout Constraints

- **Max box width:** 48 characters (or `terminal width - 4`, whichever is smaller).
- **Description area:** Up to 4 lines of text below the menu.
- **Content width:** `terminal width - 6` characters for text viewer content.
- **Menu item scrolling:** When the list exceeds available vertical space, items scroll with the cursor. The visible window is `terminal height - menu_start - 7` items.

**Termux compatibility:**
All widths are calculated dynamically based on `getmaxyx()`. The app works on screens as small as ~40×15 characters (typical phone in portrait mode).

---

## 15. Implementation Patterns & Code Architecture

### 15.1 The Curses Wrapper Pattern

Every curses screen is invoked via `curses.wrapper()`:

```python
# In the main loop:
choice = curses.wrapper(main_menu, conn, cfg)
```

`curses.wrapper()` handles:
1. Initializing the curses screen
2. Calling your function with `stdscr` as the first argument
3. Restoring the terminal to normal on exit (even if an exception occurs)

**Why this matters:** If curses isn't properly cleaned up (e.g., due to an unhandled exception), the terminal becomes unusable — characters echo wrong, line breaks don't work. `curses.wrapper()` guarantees cleanup.

### 15.2 The Safe Addstr Pattern

Never call `stdscr.addstr()` directly. Always use the `safe_addstr()` wrapper:

```python
def safe_addstr(scr, y, x, text, attr=0):
    h, w = scr.getmaxyx()
    if y < 0 or y >= h or x >= w:
        return
    text = str(text)[:w - x - 1]
    try:
        scr.addstr(y, x, text, attr)
    except curses.error:
        pass
```

This prevents:
- Writing outside the screen bounds (crash)
- Writing to the last character of the last line (curses raises an error for this)
- Writing strings wider than the remaining line (garbled output)

### 15.3 The Menu Return Convention

All menu functions follow the same return convention:
- **Return the selected value** on `Enter`
- **Return `None`** on `q`, `ESC`, or cancel

The calling code always checks for `None`:
```python
choice = arrow_menu(stdscr, "Title", items)
if choice is None:
    return  # User cancelled, go back
# ... handle the selection
```

This creates a consistent "go back" mechanism across the entire app.

### 15.4 The Item Tuple Convention

Menu items are always tuples of 2 or 3 elements:
```python
(display_label, return_value)
(display_label, return_value, description)
```

- **display_label**: What the user sees. Padded with leading spaces for visual alignment.
- **return_value**: What the code receives. Can be any type: string, dict, boolean, integer.
- **description**: Optional. Shown in the description area below the menu. `None` or empty string means no description.

### 15.5 The Config Lifecycle

```
First launch:
  DEFAULT_CFG → saved to ~/chat/config.json → wizard modifies → saved again

Subsequent launches:
  ~/chat/config.json → load_cfg() → defaults merged with setdefault() → cfg dict

Config editor:
  cfg dict → copy() → user edits copy → "Save" writes copy → "Discard" drops copy
```

**Key detail:** The config editor works on a **copy** of the config. This means the in-memory config isn't modified until the user explicitly saves. If the app crashes during editing, the saved config file is untouched.

### 15.6 The Database Schema

```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    created_at TEXT,       -- ISO 8601
    forked_from INTEGER    -- NULL or parent session ID
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,    -- FK to sessions
    role TEXT,             -- "user", "assistant", or "system"
    content TEXT,
    created_at TEXT,       -- ISO 8601
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

**forked_from:** Tracks session lineage. When a session is forked, the new session's `forked_from` points to the source session ID. This maintains a history trail.

---

## 16. Building Your Own — Step-by-Step Instruction Set

This section is a concrete guide for implementing the same menu paradigm in your own application.

### Step 1: Define Your UI Components

You need exactly five components (matching Section 3):

1. **Arrow Menu** — For all selection screens.
2. **Text Input** — For the rare cases where typing is needed.
3. **Text Viewer** — For long-form help content.
4. **Info Screen** — For simple messages and confirmations.
5. **Draw Box** — For visual framing (used inside other components).

Implement these as standalone, reusable functions that accept `stdscr` as their first parameter. They should have no side effects except drawing to the screen and reading input.

### Step 2: Choose Your Terminal Library

| Library | Pros | Cons | Best For |
|---------|------|------|----------|
| Python `curses` | Built-in, no dependencies | Limited, no mouse, no color gradients | Simple menu-driven apps |
| `blessed` / `blessings` | Friendlier curses wrapper | Extra dependency | If curses API frustrates you |
| `prompt_toolkit` | Rich input handling, autocompletion | Heavier, different paradigm | Input-heavy applications |
| `textual` | Modern, CSS-like styling, widgets | Heavy, async, different paradigm | Complex TUI dashboards |

For the ifAI Chat paradigm, **raw `curses`** is the right choice. The simplicity of the paradigm (arrow keys + Enter + descriptions) doesn't need a framework. Fewer dependencies = runs everywhere (including Termux on Android).

### Step 3: Establish Your Return Convention

Before writing any menu code, establish these rules:

1. All menu functions return a value or `None`.
2. `None` always means "user cancelled / go back."
3. The calling code always checks for `None` before proceeding.
4. Functions never exit the program — they return, and the caller decides what to do.

### Step 4: Design Your Data Structures

**Provider/option presets:**
```python
PRESETS = [
    {
        "name": "Display Name",
        "value": "internal_value",
        "description": "Multi-line explanation\nfor the description area.",
        # ... any other data needed for this option
    },
]
```

**Menu item tuples:**
```python
items = [(preset["name"], preset, preset["description"]) for preset in PRESETS]
```

**Config with defaults:**
```python
DEFAULT_CFG = {"key": "default_value", ...}

def load_cfg():
    # Load from file, then merge defaults for any missing keys
    for k, v in DEFAULT_CFG.items():
        cfg.setdefault(k, v)
    return cfg
```

### Step 5: Build the Arrow Menu Component

The arrow menu is the heart of the system. Here's what it must do:

1. **Draw the title box** at the top of the screen.
2. **Draw the subtitle** below the box (context line).
3. **Draw the item list** with a highlight cursor on the current selection.
4. **Draw a separator** between the list and the description area.
5. **Draw the description** of the currently highlighted item.
6. **Draw the footer** with key hints.
7. **Handle input:**
   - `↑` / `k` → move cursor up (wrap around at top)
   - `↓` / `j` → move cursor down (wrap around at bottom)
   - `Enter` → return the selected item's value
   - `q` / `ESC` → return `None`
8. **Handle scrolling** when the list is longer than the visible area.

### Step 6: Build the Text Input Component

Text input must:

1. **Show a prompt** explaining what to enter.
2. **Show multi-line hints** with context and examples.
3. **Show the input line** with a visual cursor.
4. **Handle editing:** character insertion, backspace, cursor movement (`←` `→` `Home` `End`).
5. **Support password mode** (show `•` instead of characters).
6. **Support defaults** (pre-fill the input buffer).
7. **Return the string on Enter, `None` on ESC.**

### Step 7: Design Your Wizard Flow

For first-run setup:

1. **Welcome screen** — Set the tone, explain what's about to happen.
2. **Sequential decision screens** — Each choice narrows the next step. Use arrow menus for everything possible.
3. **Conditional screens** — Skip steps that don't apply based on previous choices (e.g., skip API key for local providers).
4. **Summary screen** — Show all chosen values for confirmation.
5. **Save and mark as configured** — Set a flag so the wizard doesn't run again.

**Cancellation at any step** should abort cleanly with a friendly message.

### Step 8: Design Your Main Menu

The main menu is a simple arrow menu that returns an action string:

```python
MENU_ITEMS = [
    ("Action Label", "action_key", "Description of what this does."),
    ...
    ("Exit", "exit", "Close the app. Everything is saved."),
]
```

The main loop:
```python
while True:
    choice = curses.wrapper(main_menu, ...)
    if choice is None or choice == "exit":
        break
    elif choice == "action_key":
        # do the thing
```

### Step 9: Write Your Help Content

For each concept a user might need to understand:

1. **Write a 100-200 word article** in plain English.
2. **Use the pattern:** What is it → Why it matters → How it works → Practical examples → 💡 Tip.
3. **Avoid jargon**, or define it immediately when you must use it.
4. **Use concrete examples**, not abstract descriptions.
5. **Store as string constants** in your code, not external files (so they're always available, even without a filesystem).

### Step 10: Handle Errors Like a Teacher

For every error your application can encounter:

1. **Write a human-readable message** that explains what went wrong.
2. **Add a suggestion** for what the user should do.
3. **Never show raw exceptions** to the user (log them internally if needed).
4. **Make errors non-fatal** whenever possible — recover and let the user try again.

### Step 11: Provide Advanced User Escape Hatches

For every layer of guidance, provide a bypass:

| Guidance Layer | Bypass |
|---------------|--------|
| Setup wizard | `--config` flag to skip |
| Arrow menus | Config file for direct editing |
| Preset lists | "Custom / Other" option with text input |
| Menu navigation | Vim keys for faster movement |
| Full explanations | Descriptions are passive (you don't have to read them) |

### Step 12: Test with a Beginner

The ultimate test is not whether your code works — it's whether a person who has never used the terminal can complete setup and start using your app without help. Watch them try. Note where they hesitate. Fix those spots.

---

## 17. Checklist: Does Your Menu Pass the Mom Test?

Use this checklist for every screen in your application. If any answer is "no," fix it.

### First Impression
- [ ] Can the user figure out what to do within 3 seconds of seeing the screen?
- [ ] Are the available actions visible (not hidden behind keypresses)?
- [ ] Is the key hint footer always visible at the bottom?

### Navigation
- [ ] Do arrow keys work for navigation? (Not everyone knows vim keys)
- [ ] Does `Enter` confirm on every screen?
- [ ] Does `q` or `ESC` go back on every screen?
- [ ] Can the user always get back to where they came from?
- [ ] Does the list wrap around (top ↔ bottom)?

### Information
- [ ] Does every menu item have a description?
- [ ] Does the description explain what happens if you choose this item?
- [ ] If the user needs to understand a concept, is it explained on this screen?
- [ ] Are there concrete examples (URLs, commands, values)?

### Input
- [ ] Is this text input truly necessary, or could it be a selection?
- [ ] Is there a hint explaining what to type?
- [ ] Is there a default value pre-filled?
- [ ] Is sensitive input masked?

### Safety
- [ ] Can the user cancel without losing data?
- [ ] Is destructive action behind a confirmation?
- [ ] Are changes saved explicitly (not automatically)?
- [ ] Does the app recover gracefully from errors?

### Advanced Users
- [ ] Can this screen be bypassed entirely by editing a config file?
- [ ] Are there keyboard shortcuts for experienced users?
- [ ] Is the learning curve flat for someone who already knows what they want?

### Accessibility
- [ ] Does the layout work on a small screen (40×15)?
- [ ] Are colors used for emphasis, not information? (Screen readers and colorblind users)
- [ ] Does the text avoid assumptions about the user's expertise?

---

## Appendix A: Complete Screen Flow Map

```
Launch
  │
  ├─ First run (or --setup) ──────────────────────────────────────────┐
  │                                                                    │
  │   Step 1: Welcome Screen (info_screen)                             │
  │     │                                                              │
  │   Step 2: Choose Provider (arrow_menu)                             │
  │     │                                                              │
  │     ├─ Custom? → Step 2b: Enter Endpoint URL (text_input)          │
  │     │                                                              │
  │   Step 3: Enter API Key (text_input) [cloud providers only]        │
  │     │                                                              │
  │   Step 4: Choose Model (arrow_menu)                                │
  │     │                                                              │
  │     ├─ Custom model? → Enter Model Name (text_input)               │
  │     │                                                              │
  │   Step 5: Choose Personality (arrow_menu)                          │
  │     │                                                              │
  │     ├─ Write own? → Enter System Prompt (text_input)               │
  │     │                                                              │
  │   Step 6: Response Style (arrow_menu)                              │
  │     │                                                              │
  │   Step 7: Summary Screen (info_screen)                             │
  │     │                                                              │
  │     └──────────────────────────────────────────────────────────────┘
  │
  └─ Normal launch (or --config) ─┐
                                   │
  ┌────────────────────────────────┘
  │
  ▼
  MAIN MENU (arrow_menu)
  │
  ├─ New Chat ─────────────── → CHAT LOOP (plain terminal)
  │                              │
  │                              ├─ /back → return to MAIN MENU
  │                              ├─ /clear → reset context, continue chatting
  │                              ├─ /rename <n> → rename session, continue
  │                              ├─ /help → show commands, continue
  │                              ├─ /exit → goodbye, quit app
  │                              └─ Ctrl+C → return to MAIN MENU
  │
  ├─ Resume Session ──────── → SESSION PICKER (arrow_menu)
  │                              │
  │                              ├─ Select session → CHAT LOOP
  │                              └─ q/Back → return to MAIN MENU
  │
  ├─ Fork Session ────────── → SESSION PICKER (arrow_menu)
  │                              │
  │                              ├─ Select session → copy + CHAT LOOP
  │                              └─ q/Back → return to MAIN MENU
  │
  ├─ Help & Docs ─────────── → HELP MENU (arrow_menu)
  │                              │
  │                              ├─ Select topic → TEXT VIEWER
  │                              │                   │
  │                              │                   └─ q → return to HELP MENU
  │                              └─ q/Back → return to MAIN MENU
  │
  ├─ Configure ───────────── → CONFIG EDITOR (arrow_menu loop)
  │                              │
  │                              ├─ Select field → edit value
  │                              │                   │
  │                              │                   ├─ Toggle (stream) → flip, back to list
  │                              │                   └─ Text (others) → TEXT INPUT → back to list
  │                              │
  │                              ├─ Save & Back → save config, return to MAIN MENU
  │                              ├─ Discard → return to MAIN MENU
  │                              └─ q → return to MAIN MENU (discards)
  │
  └─ Exit / q ────────────── → "Goodbye! Your chats are saved. 👋" → quit
```

---

## Appendix B: Terminology Quick Reference

| Term Used in App | Technical Term | Plain English |
|-----------------|---------------|---------------|
| Provider | API service / backend | The company or software that runs the AI |
| Endpoint | API base URL | The web address where the AI lives |
| API Key | Authentication token | A password that proves you have an account |
| Model | LLM / language model | The AI "brain" that generates responses |
| System Prompt | System message | Instructions that shape the AI's personality |
| Streaming | Server-sent events | Watching responses appear word by word |
| Session | Conversation thread | A saved conversation you can come back to |
| Fork | Branch / copy | Create a copy of a conversation to explore differently |
| Context | Conversation history | What the AI "remembers" from earlier messages |
| Max History | Context window limit | How many messages the AI can see at once |

---

## Appendix C: Why Not a Web UI?

The terminal menu paradigm was chosen over a web interface for specific reasons:

1. **Runs anywhere.** A terminal exists on every computer, phone (Termux), server, and embedded device. A web UI needs a browser, a port, and often a framework.
2. **Zero dependencies.** The entire UI runs on Python's built-in `curses` library. No npm, no React, no CSS frameworks.
3. **Instant startup.** The app starts in milliseconds. No webpack build, no server boot, no page load.
4. **SSH-friendly.** The app works over SSH connections — you can use it on a remote server.
5. **Low bandwidth.** The entire app is one Python file. It can be copied over a slow connection.
6. **Privacy.** Everything runs locally. No browser fingerprinting, no cookies, no tracking.
7. **Educational.** Terminal skills transfer to every computing platform. Teaching people to use the terminal, through a friendly interface, is itself a valuable outcome.

---

<p align="center"><em>Built with the belief that powerful tools can also be friendly ones.</em></p>
