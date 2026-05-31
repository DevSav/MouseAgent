from PySide6.QtWidgets import QApplication

from mouseagent.hotkeys import HotkeyController
from mouseagent.overlay import CursorOverlay
from mouseagent.providers.mock import MockProvider
from mouseagent.screen import ScreenCapture


class MouseAgentApp:
    def __init__(self) -> None:
        self.qt_app = QApplication([])
        self.overlay = CursorOverlay()
        self.screen_capture = ScreenCapture()
        self.provider = MockProvider()
        self.hotkeys = HotkeyController(on_activate=self.handle_activation)

    def start(self) -> int:
        self.overlay.show()
        self.hotkeys.start()
        return self.qt_app.exec()

    def handle_activation(self) -> None:
        screenshot = self.screen_capture.capture_primary_screen()
        response = self.provider.ask(
            question="What should I do next?",
            screenshot=screenshot,
        )
        self.overlay.show_message(response)


def main() -> int:
    app = MouseAgentApp()
    return app.start()

