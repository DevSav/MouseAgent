# MouseAgent Status

Last updated: 2026-05-31

## What We Have Now

MouseAgent is currently a Windows-first Python desktop MVP.

The app can:

- start from `python -m mouseagent`
- show a small logo-only companion beside the cursor
- listen for the global shortcut `Ctrl+Space`
- open a minimal ask dialog
- focus the question input automatically
- capture the primary screen after the user submits a question
- hide its own UI during screenshot capture
- show the response in a fixed floating answer popup
- ask again from the popup
- hide the popup
- quit from the popup or system tray
- save local settings to `settings.local.json`
- switch between provider options in Settings

## Current UI Direction

The current design direction is:

- minimal
- dark glass surface
- smooth rounded edges
- cyan/teal futuristic accent colors
- no permanent bottom-right control panel
- no text next to the cursor
- cursor companion is just a small agent logo/orb

## Current Providers

### Mock

The default provider. It does not call a real AI model. It proves that the desktop flow works end to end.

### Gemini

Provider scaffold exists.

It supports:

- API key setting
- model setting
- screenshot plus question payload

It still needs live testing with a real Gemini API key.

### Ollama

Provider scaffold exists.

It supports:

- local Ollama URL
- model setting
- screenshot plus question payload

It still needs live testing with a local vision model, for example:

```powershell
ollama pull llama3.2-vision
```

## Important Files

- `requirements.txt` - dependency file for collaborators
- `README.md` - setup and project overview
- `docs/PRODUCT.md` - product direction
- `docs/REQUIREMENTS.md` - MVP requirements and constraints
- `docs/ROADMAP.md` - phased build plan
- `docs/ARCHITECTURE.md` - system design notes
- `mouseagent/app.py` - application bootstrap and main flow
- `mouseagent/overlay.py` - desktop UI windows
- `mouseagent/screen.py` - screen capture
- `mouseagent/settings.py` - local settings storage
- `mouseagent/providers/` - AI provider implementations

## How To Run

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the app:

```powershell
python -m mouseagent
```

Use the app:

```text
Ctrl+Space -> type question -> Enter
```

## Known Limitations

- Real AI provider calls have not been fully tested yet.
- The app captures only the primary screen.
- Settings are stored in plain local JSON for now.
- API keys are not yet stored in the OS credential store.
- No screenshot preview/privacy confirmation yet.
- No installer or packaged `.exe` yet.
- No voice input/output yet.
- No step-by-step structured guidance yet.
- No app-specific intelligence for Excel, Adobe, browser, etc.

## Next Steps

### 1. Test Settings UI

Verify that:

- Settings opens from the answer popup.
- Settings opens from the tray menu.
- Provider dropdown is visible.
- Gemini and Ollama model fields are visible.
- Saving settings updates `settings.local.json`.
- App continues using the selected provider.

### 2. Test Gemini Provider

Use a Gemini API key and verify:

- text-only question works
- screenshot question works
- errors are readable
- model name is correct
- latency is acceptable

### 3. Test Ollama Provider

Install Ollama and a vision model, then verify:

- app reaches `http://localhost:11434`
- selected model responds
- screenshot input works
- local latency is acceptable

### 4. Add Screenshot Privacy Preview

Before sending to a provider, show:

- small screenshot preview
- provider name
- Continue / Cancel

This is important before real cloud providers are used heavily.

### 5. Improve Guidance Format

Move from plain text responses to structured guidance:

- summary
- numbered steps
- optional warning
- optional follow-up question

### 6. Package For Friends

Create a Windows executable so collaborators can test without Python setup.

Likely path:

- PyInstaller
- simple build script
- release zip

## Suggested Work Split

Person A:

- UI polish
- settings flow
- packaging
- screenshot preview

Person B:

- Gemini testing
- Ollama testing
- provider error handling
- prompt design

Both:

- test on real apps like Excel, Premiere, browser, and VS Code
- collect bad answers
- improve prompts and UX

