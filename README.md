# MouseAgent

MouseAgent is a desktop AI companion that lives beside your cursor and gives live guidance for whatever is on your screen.

The first goal is not to control the mouse. The app should observe context, answer questions, and guide the user with text, voice, and visual highlights while the user stays in control.

## Product Idea

You press a shortcut, ask a question, and MouseAgent captures the current screen context. It sends the screenshot and your question to an AI provider you configure, then shows the answer in a fixed popup while the small companion stays beside your cursor.

Example:

> "How do I make this Excel formula?"

MouseAgent can respond:

> "Click cell D2 and type `=AVERAGE(B2:B12)`, then press Enter."

Later versions can add voice guidance and on-screen arrows or highlights.

## Current Skeleton

This repo starts with a minimal Python desktop MVP:

- cursor-following overlay window
- global shortcut ask flow
- fixed answer popup
- provider abstraction for future OpenAI / Anthropic / other APIs
- screen capture service
- docs for roadmap and architecture

## Tech Stack

Planned MVP stack:

- Python 3.9+
- PySide6 for the desktop overlay
- Pillow / mss for screen capture
- pynput or keyboard for global shortcuts
- OpenAI / Anthropic SDKs through user-provided API keys

## Getting Started

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -e .
```

Or install from the dependency file:

```powershell
pip install -r requirements.txt
```

Run the app:

```powershell
python -m mouseagent
```

Or double-click:

```text
run_mouseagent.cmd
```

Stop the app:

```text
stop_mouseagent.cmd
```

Press `Ctrl+Space` to ask a question. The current MVP captures the screen and returns a mock answer in a fixed popup, which proves the desktop flow before real AI providers are added.

The answer popup includes `Ask again`, `Hide`, and `Quit`. If your system tray is visible, the tray icon also has ask and quit actions.

## Repository Layout

```text
mouseagent/
  app.py                  # Main application bootstrap
  overlay.py              # Cursor companion overlay UI
  hotkeys.py              # Global shortcut handling
  screen.py               # Screenshot capture service
  settings.py             # Local app settings
  providers/
    base.py               # Shared provider interface
    mock.py               # Local mock provider for early UI testing
docs/
  ROADMAP.md              # Build plan and milestones
  ARCHITECTURE.md         # System design notes
  PRODUCT.md              # Product direction and user experience
  REQUIREMENTS.md         # MVP requirements and constraints
  STATUS.md               # Current project state and next steps
scripts/
  run_mouseagent.ps1       # Starts the app from the repo root
  stop_mouseagent.ps1      # Stops MouseAgent Python processes
run_mouseagent.cmd         # Double-click launcher
stop_mouseagent.cmd        # Double-click stopper
```

## Important Principle

MouseAgent should guide, not take over.

No automatic clicking, no hidden control, no surprise actions. The user should always understand what the assistant sees, what it suggests, and what happens next.
