from __future__ import annotations

from abc import ABC, abstractmethod

from mouseagent.screen import Screenshot


class AIProvider(ABC):
    @abstractmethod
    def ask(self, question: str, screenshot: Screenshot | None = None) -> str:
        raise NotImplementedError
