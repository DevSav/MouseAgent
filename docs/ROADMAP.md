# Roadmap

This roadmap is written for two people building the project together. The goal is to reach a real, testable MVP quickly before adding ambitious features.

## Phase 0: Repo Setup

- Create GitHub repo.
- Agree on name, license, and README.
- Decide the first target OS. Recommended: Windows first.
- Add project board with columns: Backlog, Ready, In Progress, Review, Done.

## Phase 1: Local Desktop Prototype

Goal: prove that the app can feel like it lives next to the mouse.

- Build a small always-on-top cursor overlay.
- Make the overlay follow the mouse smoothly.
- Add a basic answer bubble.
- Add a global shortcut that opens a prompt.
- Add local settings for shortcut and provider choice.

Definition of done:

- Running the app shows a small icon near the cursor.
- Pressing the shortcut opens a prompt or triggers a mock answer.
- The app can be closed cleanly from the tray or terminal.

Current MVP status:

- Cursor-following overlay exists.
- `Ctrl+Space` opens an ask dialog.
- Primary screen capture runs after a question is submitted.
- Mock provider returns guidance near the cursor.
- Tray menu supports "Ask now" and "Quit".

## Phase 2: Screen Context

Goal: let the assistant see what the user sees.

- Capture the primary screen.
- Capture the active window if possible.
- Add screenshot preview/debug mode.
- Add privacy controls so users know what is being sent.

Definition of done:

- The app captures a screenshot when activated.
- The screenshot can be sent to a provider module.
- The user can disable screen capture.

## Phase 3: Bring Your Own AI

Goal: support user-provided AI access without owning their subscription.

- Add provider interface.
- Add OpenAI provider using API key.
- Add Anthropic provider using API key.
- Store API keys securely using the OS credential store.
- Add a provider test button.

Important note:

ChatGPT Plus and Claude Pro are consumer subscriptions. They usually do not give third-party apps direct programmatic access. The MVP should use API keys first.

Definition of done:

- User can enter an API key.
- User can choose a provider.
- User can ask a question about the screen and receive an answer.

## Phase 4: Guidance UI

Goal: move beyond chat into live guidance.

- Show short text guidance near cursor.
- Add step-by-step mode.
- Add screen highlights and arrows.
- Add "next step" and "done" controls.
- Keep all interaction user-driven.

Definition of done:

- The assistant can show a 3-5 step guide.
- The user can advance steps manually.
- The app can highlight a general screen region.

## Phase 5: Voice

Goal: make the assistant useful when the user's hands are busy.

- Add push-to-talk.
- Add speech-to-text.
- Add text-to-speech.
- Add mute and voice speed settings.

Definition of done:

- User can ask a question by voice.
- Assistant can read guidance aloud.

## Phase 6: App-Specific Quality

Goal: become genuinely helpful inside common tools.

Start with:

- Excel
- Adobe Premiere Pro
- Photoshop
- Browser
- VS Code

For each app:

- Collect common tasks.
- Test prompts with real screenshots.
- Improve guidance formats.
- Add known UI vocabulary and workflows.

## Phase 7: Packaging and Sharing

Goal: make it easy for other people to try.

- Package for Windows.
- Add installer.
- Add auto-update plan.
- Add privacy policy.
- Add crash/error logging with consent.

## Suggested Split Between Two People

Person A:

- Desktop shell
- Overlay UI
- Hotkeys
- Packaging

Person B:

- AI provider integration
- Screenshot processing
- Prompt design
- App-specific task testing

Both:

- Product testing
- Privacy decisions
- UX decisions
