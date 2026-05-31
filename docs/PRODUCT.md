# Product Notes

## One-Sentence Pitch

MouseAgent is an AI guide that sits beside your cursor, sees your screen when you ask, and tells you what to do next without taking control.

## Target Users

- students learning software
- creators working in Adobe tools
- office workers using Excel, Word, and PowerPoint
- developers who want quick guidance inside IDEs
- anyone who currently screenshots their screen and uploads it to an AI chat

## Product Principles

- The user stays in control.
- The assistant should feel present but not annoying.
- Guidance should be short, specific, and actionable.
- The app should ask for screen context only when needed.
- Privacy should be obvious, not hidden in settings.

## MVP User Story

As a user, I want to press a shortcut and ask what to do on my current screen, so I can get immediate guidance without taking a screenshot manually.

## What Makes It Different

Most AI assistants live in a separate chat window. MouseAgent lives in the working context: next to the cursor, on top of the current app, and focused on the next action.

## Early Design Decisions

- Use an icon beside the cursor, not a full chat sidebar.
- Show short guidance first, with an option to expand.
- Avoid automatic clicking in the MVP.
- Let users bring their own API key.
- Start Windows-first.

## Risks

- AI may misunderstand the screen.
- Global hotkeys and overlays can be OS-specific.
- Consumer AI subscriptions may not work as direct integrations.
- Screen capture creates privacy concerns.
- Latency must be low enough to feel useful.

## Good First Demo

Open Excel, press the shortcut, ask:

> "How do I average these numbers?"

MouseAgent captures the screen and replies near the cursor:

> "Click the result cell, type `=AVERAGE(B2:B12)`, then press Enter."

