from __future__ import annotations

import sys

from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon

from mouseagent.hotkeys import HotkeyController
from mouseagent.overlay import AnswerWindow, ControlPanel, CursorOverlay, QuestionDialog
from mouseagent.providers.mock import MockProvider
from mouseagent.screen import ScreenCapture


class AppEvents(QObject):
    activated = Signal()


class MouseAgentApp:
    def __init__(self) -> None:
        self.qt_app = QApplication(sys.argv)
        self.qt_app.setApplicationName("MouseAgent")
        self.qt_app.setQuitOnLastWindowClosed(False)

        self.events = AppEvents()
        self.events.activated.connect(self.handle_activation)

        self.overlay = CursorOverlay()
        self.screen_capture = ScreenCapture()
        self.provider = MockProvider()
        self.hotkeys = HotkeyController(on_activate=self.events.activated.emit)
        self.answer_window = AnswerWindow(on_ask=self.events.activated.emit, on_quit=self.quit)
        self.control_panel = ControlPanel(on_ask=self.events.activated.emit, on_quit=self.quit)
        self.tray = self._build_tray()

    def start(self) -> int:
        self.overlay.show()
        self.overlay.show_message("Ready")
        self.control_panel.set_status("Ready")
        self.tray.show()
        self.hotkeys.start()
        QTimer.singleShot(0, self.control_panel.show)
        return self.qt_app.exec()

    def _build_tray(self) -> QSystemTrayIcon:
        icon = self.qt_app.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        tray = QSystemTrayIcon(icon)
        tray.setToolTip("MouseAgent")

        menu = QMenu()
        ask_action = QAction("Ask now")
        ask_action.triggered.connect(self.events.activated.emit)

        quit_action = QAction("Quit")
        quit_action.triggered.connect(self.quit)

        menu.addAction(ask_action)
        menu.addSeparator()
        menu.addAction(quit_action)
        tray.setContextMenu(menu)
        tray.activated.connect(self.handle_tray_activation)
        return tray

    def handle_tray_activation(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.events.activated.emit()

    def handle_activation(self) -> None:
        question = QuestionDialog.ask()
        if not question:
            self.overlay.show_message("Ready")
            self.control_panel.set_status("Ready")
            return

        self.overlay.hide()
        self.answer_window.hide()
        self.control_panel.hide()
        self.qt_app.processEvents()
        screenshot = self.screen_capture.capture_primary_screen()
        self.overlay.show()
        self.overlay.show_message("Thinking")
        self.control_panel.show()
        self.control_panel.set_status("Thinking")

        response = self.provider.ask(
            question=question,
            screenshot=screenshot,
        )
        self.overlay.show_message("Ready")
        self.control_panel.set_status("Ready")
        self.answer_window.show_answer(question=question, text=response)

    def quit(self) -> None:
        self.hotkeys.stop()
        self.tray.hide()
        self.answer_window.hide()
        self.control_panel.hide()
        self.overlay.hide()
        self.qt_app.quit()


def main() -> int:
    app = MouseAgentApp()
    return app.start()
