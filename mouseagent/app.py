from __future__ import annotations

import sys

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon

from mouseagent.debug import debug_log
from mouseagent.hotkeys import HotkeyController
from mouseagent.overlay import AnswerWindow, CursorOverlay, QuestionDialog, SettingsDialog
from mouseagent.providers.factory import build_provider
from mouseagent.screen import ScreenCapture
from mouseagent.settings import load_settings, save_settings


class AppEvents(QObject):
    activated = Signal()


class MouseAgentApp:
    def __init__(self) -> None:
        self.qt_app = QApplication(sys.argv)
        self.qt_app.setApplicationName("MouseAgent")
        self.qt_app.setQuitOnLastWindowClosed(False)

        self.events = AppEvents()
        self.events.activated.connect(self.handle_activation)

        self.settings = load_settings()
        debug_log(
            "startup: "
            f"provider={self.settings.provider}, "
            f"gemini_model={self.settings.gemini_model}, "
            f"ollama_model={self.settings.ollama_model}"
        )
        self.overlay = CursorOverlay()
        self.screen_capture = ScreenCapture()
        self.provider = build_provider(self.settings)
        self.hotkeys = HotkeyController(on_activate=self.events.activated.emit)
        self.answer_window = AnswerWindow(
            on_ask=self.events.activated.emit,
            on_settings=self.open_settings,
            on_quit=self.quit,
        )
        self.tray = self._build_tray()

    def start(self) -> int:
        debug_log("app: starting event loop")
        self.overlay.show()
        self.overlay.show_message("Ready")
        self.tray.show()
        self.hotkeys.start()
        return self.qt_app.exec()

    def _build_tray(self) -> QSystemTrayIcon:
        icon = self.qt_app.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        tray = QSystemTrayIcon(icon)
        tray.setToolTip("MouseAgent")

        menu = QMenu()
        ask_action = QAction("Ask now")
        ask_action.triggered.connect(self.events.activated.emit)

        settings_action = QAction("Settings")
        settings_action.triggered.connect(self.open_settings)

        quit_action = QAction("Quit")
        quit_action.triggered.connect(self.quit)

        menu.addAction(ask_action)
        menu.addAction(settings_action)
        menu.addSeparator()
        menu.addAction(quit_action)
        tray.setContextMenu(menu)
        tray.activated.connect(self.handle_tray_activation)
        return tray

    def handle_tray_activation(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        debug_log(f"tray: activated reason={reason}")
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.events.activated.emit()

    def handle_activation(self) -> None:
        debug_log("activation: shortcut/menu triggered")
        # Capture active window before the dialog steals focus
        active_hwnd = self.screen_capture.get_foreground_hwnd()
        window_info = self.screen_capture.get_window_info(active_hwnd)
        debug_log(
            "active-window: "
            f"hwnd={active_hwnd}, "
            f"app={window_info.app_name}, "
            f"title={window_info.window_title!r}"
        )

        question = QuestionDialog.ask()
        if not question:
            debug_log("activation: cancelled or empty question")
            self.overlay.show_message("Ready")
            return
        debug_log(f"question: {question!r}")

        self.overlay.hide()
        self.answer_window.hide()
        self.qt_app.processEvents()
        screenshot = self.screen_capture.capture_window(active_hwnd)
        debug_log(
            "screenshot: "
            f"width={screenshot.width}, height={screenshot.height}, "
            f"target_app={window_info.app_name}"
        )
        self.overlay.show()
        self.overlay.show_message("Thinking")

        debug_log(f"provider: asking {type(self.provider).__name__}")
        response = self.provider.ask(
            question=question,
            screenshot=screenshot,
            window_info=window_info,
        )
        debug_log(f"provider: response_chars={len(response)}")
        self.overlay.show_message("Ready")
        self.answer_window.show_answer(
            question=question,
            text=response,
            app_name=window_info.app_name,
        )

    def open_settings(self) -> None:
        debug_log("settings: opened")
        updated_settings = SettingsDialog.edit(self.settings)
        if updated_settings is None:
            debug_log("settings: cancelled")
            return

        self.settings = updated_settings
        save_settings(self.settings)
        self.provider = build_provider(self.settings)
        debug_log(
            "settings: saved "
            f"provider={self.settings.provider}, "
            f"gemini_model={self.settings.gemini_model}, "
            f"ollama_url={self.settings.ollama_url}, "
            f"ollama_model={self.settings.ollama_model}"
        )
        self.overlay.show_message("Ready")
        self.answer_window.show_answer(
            question="Settings saved",
            text=f"Provider: **{self.settings.provider}**\n\nPress Ctrl+Space to ask again.",
        )

    def quit(self) -> None:
        debug_log("app: quitting")
        self.hotkeys.stop()
        self.tray.hide()
        self.answer_window.hide()
        self.overlay.hide()
        self.qt_app.quit()


def main() -> int:
    app = MouseAgentApp()
    return app.start()
