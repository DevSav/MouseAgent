from __future__ import annotations

from mouseagent.providers.base import AIProvider
from mouseagent.screen import Screenshot


class MockProvider(AIProvider):
    def ask(self, question: str, screenshot: Screenshot | None = None) -> str:
        if screenshot is None:
            return f"Mock answer: {question}"

        return (
            f"You asked: {question}\n\n"
            "MVP mock guidance: I captured your screen. Next we will connect a real AI "
            "provider so this answer can use the screenshot."
        )
