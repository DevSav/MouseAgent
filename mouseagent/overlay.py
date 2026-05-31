from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QColor, QCursor, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

APP_STYLE = """
QWidget {
    color: #111827;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}
QPushButton {
    background: #111827;
    color: #ffffff;
    border: 0;
    border-radius: 6px;
    padding: 7px 12px;
}
QPushButton:hover {
    background: #1f2937;
}
QPushButton:pressed {
    background: #374151;
}
QPushButton[variant="secondary"] {
    background: #f3f4f6;
    color: #111827;
    border: 1px solid #d1d5db;
}
QPushButton[variant="secondary"]:hover {
    background: #e5e7eb;
}
QPushButton[variant="danger"] {
    background: #991b1b;
}
QPushButton[variant="danger"]:hover {
    background: #7f1d1d;
}
QLineEdit {
    background: #ffffff;
    border: 1px solid #9ca3af;
    border-radius: 7px;
    padding: 10px 11px;
    font-size: 14px;
}
QLineEdit:focus {
    border: 2px solid #2563eb;
    padding: 9px 10px;
}
"""


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
        self.setStyleSheet(APP_STYLE)
        self.setModal(True)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        self.setFixedWidth(520)

        title = QLabel("Ask about this screen")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        subtitle = QLabel("MouseAgent will capture the current screen after you submit.")
        subtitle.setStyleSheet("color: #4b5563;")

        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Example: How do I export this video?")
        self.input.returnPressed.connect(self.accept)

        ask_button = QPushButton("Ask", self)
        ask_button.setDefault(True)
        ask_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.setProperty("variant", "secondary")
        cancel_button.clicked.connect(self.reject)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        buttons.addWidget(cancel_button)
        buttons.addWidget(ask_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(subtitle)
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
        self.setStyleSheet(APP_STYLE)
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setMinimumSize(460, 280)
        self.resize(520, 320)

        header = QHBoxLayout()
        title_block = QVBoxLayout()

        title = QLabel("MouseAgent")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        self.question = QLabel("Ask a question to get guidance.")
        self.question.setWordWrap(True)
        self.question.setStyleSheet("color: #4b5563;")

        title_block.addWidget(title)
        title_block.addWidget(self.question)

        self.badge = QLabel("Guidance")
        self.badge.setStyleSheet(
            """
            QLabel {
                color: #075985;
                background: #e0f2fe;
                border: 1px solid #bae6fd;
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 12px;
            }
            """
        )

        header.addLayout(title_block, 1)
        header.addWidget(self.badge, 0, Qt.AlignmentFlag.AlignTop)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: #e5e7eb;")

        self.answer = QTextEdit()
        self.answer.setReadOnly(True)
        self.answer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.answer.setStyleSheet(
            """
            QTextEdit {
                background: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 12px;
                line-height: 18px;
            }
            """
        )

        ask_button = QPushButton("Ask again")
        ask_button.clicked.connect(on_ask)

        hide_button = QPushButton("Hide")
        hide_button.setProperty("variant", "secondary")
        hide_button.clicked.connect(self.hide)

        quit_button = QPushButton("Quit")
        quit_button.setProperty("variant", "danger")
        quit_button.clicked.connect(on_quit)

        buttons = QHBoxLayout()
        buttons.addWidget(ask_button)
        buttons.addStretch(1)
        buttons.addWidget(hide_button)
        buttons.addWidget(quit_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        layout.addLayout(header)
        layout.addWidget(divider)
        layout.addWidget(self.answer)
        layout.addLayout(buttons)

    def show_answer(self, question: str, text: str) -> None:
        self.question.setText(question)
        self.answer.setPlainText(text)
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
        self.setStyleSheet(APP_STYLE)
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setFixedSize(256, 86)

        self.status = QLabel("Ready")
        self.status.setStyleSheet("font-size: 14px; font-weight: 600;")

        hint = QLabel("Ctrl+Space to ask")
        hint.setStyleSheet("color: #6b7280; font-size: 12px;")

        status_layout = QVBoxLayout()
        status_layout.setSpacing(0)
        status_layout.addWidget(self.status)
        status_layout.addWidget(hint)

        ask_button = QPushButton("Ask")
        ask_button.clicked.connect(on_ask)

        quit_button = QPushButton("Quit")
        quit_button.setProperty("variant", "secondary")
        quit_button.clicked.connect(on_quit)

        buttons = QHBoxLayout()
        buttons.addWidget(ask_button)
        buttons.addWidget(quit_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 9, 10, 10)
        layout.setSpacing(7)
        layout.addLayout(status_layout)
        layout.addLayout(buttons)

    def set_status(self, text: str) -> None:
        self.status.setText(text)

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
