from mouseagent.providers.base import AIProvider
from mouseagent.screen import Screenshot


class MockProvider(AIProvider):
    def ask(self, question: str, screenshot: Screenshot | None = None) -> str:
        if screenshot is None:
            return f"Mock answer: {question}"

        return (
            "I can see your screen context placeholder. Next step: connect a real AI "
            "provider and pass this screenshot with your question."
        )

