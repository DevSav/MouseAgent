# MouseAgent Requirements

## Purpose

MouseAgent is a desktop AI companion that stays beside the user's cursor and gives live guidance about what is currently on screen.

The app should reduce the friction of taking screenshots, uploading them to an AI chat, and manually explaining context.

## MVP Goal

Build a Windows-first desktop prototype where the user can:

- launch MouseAgent
- see a small companion near the cursor
- press a global shortcut
- ask a question
- allow the app to capture the current screen
- receive guidance in a lightweight popup
- quit the app cleanly

## Core User Flow

1. User starts MouseAgent.
2. A small companion appears near the cursor.
3. User presses `Ctrl+Space`.
4. A minimal ask dialog opens and focuses the input automatically.
5. User types a question and presses Enter.
6. MouseAgent hides its own UI, captures the screen, and restores the companion.
7. MouseAgent sends the question and screenshot to the selected provider.
8. MouseAgent shows the response in a fixed answer popup.
9. User can ask again, hide the popup, or quit.

## Functional Requirements

### Cursor Companion

- Must follow near the cursor without blocking clicks.
- Must be visually small and minimal.
- Must show simple status states: ready, thinking.
- Must not expand into the full answer surface.

### Shortcut

- Must support a global ask shortcut.
- Default shortcut: `Ctrl+Space`.
- Shortcut should work while another app is focused.
- Future versions should allow shortcut customization.

### Ask Dialog

- Must open quickly after the shortcut.
- Must focus the text input automatically.
- Must submit with Enter.
- Must allow cancel/close without capturing the screen.
- Must stay visually minimal.

### Screen Capture

- Must capture the primary screen for MVP.
- Must hide MouseAgent UI during capture.
- Must not capture continuously in the background.
- Future versions should support active-window capture.

### Answer Popup

- Must appear in a stable screen position.
- Must not follow the cursor.
- Must show the user's question and the assistant guidance.
- Must include a way to ask again.
- Must include a way to hide the popup.
- Must include a way to quit the app.

### Quit Behavior

- App must be quit-able from the answer popup.
- App must be quit-able from the system tray when available.
- Quitting must stop the hotkey listener.

## Provider Requirements

### MVP

- Must include a mock provider for UI testing.
- Provider interface must allow screenshot plus text question.

### Near-Term Providers

- Gemini API for a low-cost/free-tier cloud vision option.
- Ollama for local/no-credit mode.

### Later Providers

- OpenAI API through user-provided API key.
- Anthropic API through user-provided API key.
- Optional OpenRouter integration.

## Subscription and Billing Constraints

- MouseAgent should not assume ChatGPT Plus or Claude Pro can be used as API access.
- Consumer subscriptions generally do not expose third-party app usage credits.
- The app may support:
  - user-provided API keys
  - local models
  - free-tier providers
  - manual export/copy workflows

## Privacy Requirements

- Screen capture must happen only after explicit user action.
- The app must avoid background screenshot sending.
- The app should clearly indicate when a screenshot is being used.
- Future provider settings must explain where screenshots are sent.
- Screenshots should not be saved by default.
- API keys must not be committed to the repo.

## UX Requirements

- The UI should feel minimal, fast, and non-invasive.
- The companion should feel present without becoming distracting.
- The app should use smooth rounded surfaces and futuristic accent colors.
- Controls should not sit permanently in a bulky corner panel.
- Answers should be concise and action-oriented.
- User remains in control at all times.

## Non-Goals for MVP

- No automatic mouse movement.
- No automatic clicking.
- No background screen monitoring.
- No installer.
- No voice mode.
- No app-specific automation.
- No perfect UI element detection.

## Technical Requirements

- Python 3.9+.
- PySide6 desktop UI.
- `mss` for screenshot capture.
- `pynput` for global shortcut handling.
- Provider modules should stay isolated from UI code.
- Generated files, caches, virtual environments, and secrets must be ignored.

## Acceptance Criteria

The MVP is acceptable when:

- `python -m mouseagent` starts the app.
- Cursor companion appears near the mouse.
- `Ctrl+Space` opens the ask dialog.
- The ask input can be typed into immediately.
- Submitting a question captures the screen.
- A mock answer appears in the answer popup.
- `Ask again` works.
- `Hide` works.
- `Quit` fully exits the app.

