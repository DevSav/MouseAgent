from __future__ import annotations

from mouseagent.providers.base import AIProvider
from mouseagent.screen import Screenshot, WindowInfo


class MockProvider(AIProvider):
    def ask(
        self,
        question: str,
        screenshot: Screenshot | None = None,
        window_info: WindowInfo | None = None,
    ) -> str:
        app_line = f"Detected app: **{window_info.app_name}**\n\n" if window_info else ""

        if screenshot is None:
            return f"{app_line}Mock answer: {question}"

        return (
            f"{app_line}"
            "I captured your screen and received your question.\n\n"
            "Suggested next steps:\n\n"
            "1. Confirm the visible app and task are correct.\n"
            "2. Connect Gemini or Ollama so MouseAgent can analyze the screenshot.\n"
            "3. Replace this mock response with model-generated guidance.\n\n"
            f"Screenshot size: {screenshot.width} x {screenshot.height}\n"
            f"Question: {question}"
        )
