from __future__ import annotations

from mouseagent.providers.base import AIProvider
from mouseagent.providers.gemini import GeminiProvider
from mouseagent.providers.mock import MockProvider
from mouseagent.providers.ollama import OllamaProvider
from mouseagent.settings import AppSettings


def build_provider(settings: AppSettings) -> AIProvider:
    if settings.provider == "gemini":
        return GeminiProvider(
            api_key=settings.gemini_api_key,
            model=settings.gemini_model,
        )

    if settings.provider == "ollama":
        return OllamaProvider(
            base_url=settings.ollama_url,
            model=settings.ollama_model,
        )

    return MockProvider()
