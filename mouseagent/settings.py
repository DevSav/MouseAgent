from dataclasses import dataclass


@dataclass(frozen=True)
class AppSettings:
    provider: str = "mock"
    shortcut: str = "ctrl+space"
    voice_enabled: bool = False

