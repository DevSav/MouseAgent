from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppSettings:
    provider: str = "mock"
    shortcut: str = "ctrl+space"
    voice_enabled: bool = False
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2-vision"


SETTINGS_PATH = Path("settings.local.json")


def load_settings() -> AppSettings:
    if not SETTINGS_PATH.exists():
        return AppSettings()

    try:
        raw = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return AppSettings()

    valid_fields = AppSettings.__dataclass_fields__.keys()
    values = {key: value for key, value in raw.items() if key in valid_fields}
    return AppSettings(**values)


def save_settings(settings: AppSettings) -> None:
    SETTINGS_PATH.write_text(
        json.dumps(asdict(settings), indent=2),
        encoding="utf-8",
    )
