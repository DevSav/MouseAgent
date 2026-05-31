from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QColor, QCursor, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CursorOverlay(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setFixedSize(156, 54)

        self.message = QLabel("MouseAgent", self)
        self.message.setGeometry(44, 8, 104, 38)
        self.message.setWordWrap(True)
        self.message.setStyleSheet(
            """
            QLabel {
                color: #111827;
                background: rgba(255, 255, 255, 235);
                border: 1px solid rgba(17, 24, 39, 45);
                border-radius: 8px;
                padding: 5px 7px;
                font-size: 12px;
                line-height: 16px;
            }
            """
        )

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.follow_cursor)
        self.timer.start(16)

    def follow_cursor(self) -> None:
        cursor = QCursor.pos()
        self.move(cursor + QPoint(18, 18))

    def show_message(self, text: str) -> None:
        self.message.setText(text)
        self.show()

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(35, 131, 226))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(8, 24, 24, 24)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(15, 31, 10, 10)


class QuestionDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Ask MouseAgent")
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        self.setFixedWidth(460)

        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Ask about what is on your screen...")
        self.input.returnPressed.connect(self.accept)

        ask_button = QPushButton("Ask", self)
        ask_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.reject)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        buttons.addWidget(cancel_button)
        buttons.addWidget(ask_button)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("What do you need help with?"))
        layout.addWidget(self.input)
        layout.addLayout(buttons)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self.raise_()
        self.activateWindow()
        QTimer.singleShot(0, self.input.setFocus)
        QTimer.singleShot(50, self.input.setFocus)

    @classmethod
    def ask(cls) -> str | None:
        dialog = cls()
        cursor = QCursor.pos()
        dialog.move(cursor + QPoint(24, 24))

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None

        question = dialog.input.text().strip()
        return question or None


class AnswerWindow(QWidget):
    def __init__(self, on_ask: Callable[[], None], on_quit: Callable[[], None]) -> None:
        super().__init__()
        self.setWindowTitle("MouseAgent")
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setMinimumSize(440, 220)

        self.answer = QLabel("Ask MouseAgent to get guidance.")
        self.answer.setWordWrap(True)
        self.answer.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.answer.setStyleSheet(
            """
            QLabel {
                color: #111827;
                background: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 14px;
                font-size: 13px;
            }
            """
        )

        ask_button = QPushButton("Ask again")
        ask_button.clicked.connect(on_ask)

        hide_button = QPushButton("Hide")
        hide_button.clicked.connect(self.hide)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(on_quit)

        buttons = QHBoxLayout()
        buttons.addWidget(ask_button)
        buttons.addStretch(1)
        buttons.addWidget(hide_button)
        buttons.addWidget(quit_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.answer)
        layout.addLayout(buttons)

    def show_answer(self, text: str) -> None:
        self.answer.setText(text)
        self._move_to_default_position()
        self.show()
        self.raise_()
        self.activateWindow()

    def _move_to_default_position(self) -> None:
        screen = QApplication.primaryScreen()
        if screen is None:
            return

        area = screen.availableGeometry()
        margin = 28
        x = area.right() - self.width() - margin
        y = area.top() + margin
        self.move(x, y)


class ControlPanel(QWidget):
    def __init__(self, on_ask: Callable[[], None], on_quit: Callable[[], None]) -> None:
        super().__init__()
        self.setWindowTitle("MouseAgent Controls")
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setFixedSize(178, 42)

        ask_button = QPushButton("Ask")
        ask_button.clicked.connect(on_ask)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(on_quit)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.addWidget(ask_button)
        layout.addWidget(quit_button)

    def show(self) -> None:
        self._move_to_default_position()
        super().show()

    def _move_to_default_position(self) -> None:
        screen = QApplication.primaryScreen()
        if screen is None:
            return

        area = screen.availableGeometry()
        margin = 18
        x = area.right() - self.width() - margin
        y = area.bottom() - self.height() - margin
        self.move(x, y)
