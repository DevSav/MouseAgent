from __future__ import annotations

from collections.abc import Callable
from threading import Thread

from pynput import keyboard


class HotkeyController:
    def __init__(self, on_activate: Callable[[], None]) -> None:
        self.on_activate = on_activate
        self.listener: keyboard.GlobalHotKeys | None = None

    def start(self) -> None:
        self.listener = keyboard.GlobalHotKeys(
            {
                "<ctrl>+<space>": self.on_activate,
            }
        )
        Thread(target=self.listener.run, daemon=True).start()

    def stop(self) -> None:
        if self.listener is not None:
            self.listener.stop()
