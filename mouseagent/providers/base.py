from __future__ import annotations

from abc import ABC, abstractmethod

from mouseagent.screen import Screenshot, WindowInfo


class AIProvider(ABC):
    @abstractmethod
    def ask(
        self,
        question: str,
        screenshot: Screenshot | None = None,
        window_info: WindowInfo | None = None,
    ) -> str:
        raise NotImplementedError
