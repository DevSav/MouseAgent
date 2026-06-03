from __future__ import annotations

from datetime import datetime
from pathlib import Path


DEBUG_LOG_PATH = Path("mouseagent_debug.log")


def debug_log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line, flush=True)

    try:
        with DEBUG_LOG_PATH.open("a", encoding="utf-8") as log_file:
            log_file.write(line + "\n")
    except OSError:
        pass
