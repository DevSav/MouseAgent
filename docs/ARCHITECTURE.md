# Architecture

MouseAgent should be built as small modules that can be tested independently.

## Core Modules

### Overlay

Responsible for:

- cursor-side icon
- text bubble
- step controls
- visual highlights

The overlay should never perform user actions. It only displays guidance.

### Hotkeys

Responsible for:

- global shortcut registration
- activation events
- push-to-talk events later

### Screen Capture

Responsible for:

- primary screen capture
- active window capture later
- screenshot resizing/compression
- privacy/debug previews

### AI Providers

Responsible for:

- converting app requests into provider calls
- supporting OpenAI, Anthropic, and other providers
- keeping provider-specific code out of the UI

### Guidance Engine

Responsible for:

- turning AI responses into UI steps
- deciding what is text, voice, or highlight
- validating that response shape is usable

This can start as plain text and later become structured JSON.

## First MVP Flow

1. User presses shortcut.
2. App captures screen.
3. App asks user for a question.
4. Provider receives screenshot plus question.
5. Provider returns short guidance.
6. Overlay displays guidance near cursor.

## Privacy Model

MouseAgent should be explicit about screen capture.

Recommended rules:

- capture only when shortcut is pressed
- show when capture is happening
- never send screenshots in the background
- let users choose active-window capture when possible
- store API keys securely
- avoid keeping screenshot history by default

## Future Structured Guidance Shape

```json
{
  "summary": "Create an average formula.",
  "steps": [
    {
      "text": "Click the empty cell where you want the result.",
      "voice": "Click the empty cell where you want the result.",
      "highlight": null
    },
    {
      "text": "Type =AVERAGE(B2:B12), then press Enter.",
      "voice": "Type equals average B two through B twelve, then press enter.",
      "highlight": {
        "type": "region",
        "x": 420,
        "y": 180,
        "width": 300,
        "height": 40
      }
    }
  ]
}
```

