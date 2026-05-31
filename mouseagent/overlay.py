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
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


APP_STYLE = """
QWidget {
    color: #e5eefb;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}
QPushButton {
    background: rgba(48, 230, 255, 34);
    color: #dffbff;
    border: 1px solid rgba(48, 230, 255, 110);
    border-radius: 10px;
    padding: 7px 12px;
}
QPushButton:hover {
    background: rgba(48, 230, 255, 56);
}
QPushButton:pressed {
    background: rgba(48, 230, 255, 82);
}
QPushButton[variant="ghost"] {
    background: transparent;
    color: #9fb4cf;
    border: 1px solid rgba(159, 180, 207, 65);
}
QPushButton[variant="danger"] {
    background: rgba(255, 79, 117, 30);
    color: #ffd8e2;
    border: 1px solid rgba(255, 79, 117, 100);
}
QLineEdit {
    background: rgba(4, 12, 24, 220);
    color: #f8fbff;
    border: 1px solid rgba(48, 230, 255, 96);
    border-radius: 14px;
    padding: 12px 14px;
    selection-background-color: #30e6ff;
    selection-color: #03111f;
}
QLineEdit:focus {
    border: 1px solid rgba(120, 255, 214, 190);
}
QTextEdit {
    background: rgba(2, 8, 18, 196);
    color: #dbeafe;
    border: 1px solid rgba(48, 230, 255, 55);
    border-radius: 14px;
    padding: 12px;
    selection-background-color: #30e6ff;
    selection-color: #03111f;
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
        self.setFixedSize(88, 32)

        self.message = QLabel("Ready", self)
        self.message.setGeometry(31, 5, 52, 22)
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message.setStyleSheet(
            """
            QLabel {
                color: #dffbff;
                background: rgba(4, 12, 24, 176);
                border: 1px solid rgba(48, 230, 255, 82);
                border-radius: 11px;
                font-size: 10px;
            }
            """
        )

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.follow_cursor)
        self.timer.start(16)

    def follow_cursor(self) -> None:
        self.move(QCursor.pos() + QPoint(16, 16))

    def show_message(self, text: str) -> None:
        self.message.setText(text)
        self.show()

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.setBrush(QColor(48, 230, 255, 56))
        painter.drawEllipse(2, 2, 28, 28)
        painter.setBrush(QColor(48, 230, 255))
        painter.drawEllipse(8, 8, 16, 16)
        painter.setBrush(QColor(120, 255, 214))
        painter.drawEllipse(13, 13, 6, 6)


class QuestionDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MouseAgent")
        self.setStyleSheet(APP_STYLE)
        self.setModal(True)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Dialog
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedWidth(560)

        surface = QWidget()
        surface.setObjectName("surface")
        surface.setStyleSheet(
            """
            QWidget#surface {
                background: rgba(3, 10, 22, 235);
                border: 1px solid rgba(48, 230, 255, 82);
                border-radius: 18px;
            }
            """
        )

        title = QLabel("Ask MouseAgent")
        title.setStyleSheet("font-size: 18px; font-weight: 600; color: #f8fbff;")

        close_button = QPushButton("x")
        close_button.setFixedSize(30, 28)
        close_button.setProperty("variant", "ghost")
        close_button.clicked.connect(self.reject)

        header = QHBoxLayout()
        header.addWidget(title)
        header.addStretch(1)
        header.addWidget(close_button)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask about the screen...")
        self.input.returnPressed.connect(self.accept)

        hint = QLabel("Press Enter to send. Esc cancels.")
        hint.setStyleSheet("color: #8aa4c5; font-size: 12px;")

        ask_button = QPushButton("Ask")
        ask_button.setDefault(True)
        ask_button.clicked.connect(self.accept)

        footer = QHBoxLayout()
        footer.addWidget(hint)
        footer.addStretch(1)
        footer.addWidget(ask_button)

        surface_layout = QVBoxLayout(surface)
        surface_layout.setContentsMargins(18, 16, 18, 16)
        surface_layout.setSpacing(12)
        surface_layout.addLayout(header)
        surface_layout.addWidget(self.input)
        surface_layout.addLayout(footer)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(surface)

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self.raise_()
        self.activateWindow()
        QTimer.singleShot(0, self.input.setFocus)
        QTimer.singleShot(50, self.input.setFocus)

    @classmethod
    def ask(cls) -> str | None:
        dialog = cls()
        dialog.move(QCursor.pos() + QPoint(24, 24))

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None

        question = dialog.input.text().strip()
        return question or None


class AnswerWindow(QWidget):
    def __init__(self, on_ask: Callable[[], None], on_quit: Callable[[], None]) -> None:
        super().__init__()
        self.setWindowTitle("MouseAgent")
        self.setStyleSheet(APP_STYLE)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(520, 330)

        surface = QWidget()
        surface.setObjectName("surface")
        surface.setStyleSheet(
            """
            QWidget#surface {
                background: rgba(3, 10, 22, 238);
                border: 1px solid rgba(48, 230, 255, 82);
                border-radius: 20px;
            }
            """
        )

        title = QLabel("MouseAgent")
        title.setStyleSheet("font-size: 18px; font-weight: 600; color: #f8fbff;")

        self.question = QLabel("Guidance")
        self.question.setWordWrap(True)
        self.question.setStyleSheet("color: #8aa4c5;")

        close_button = QPushButton("x")
        close_button.setFixedSize(30, 28)
        close_button.setProperty("variant", "ghost")
        close_button.clicked.connect(self.hide)

        header_text = QVBoxLayout()
        header_text.setSpacing(2)
        header_text.addWidget(title)
        header_text.addWidget(self.question)

        header = QHBoxLayout()
        header.addLayout(header_text, 1)
        header.addWidget(close_button, 0, Qt.AlignmentFlag.AlignTop)

        self.answer = QTextEdit()
        self.answer.setReadOnly(True)

        ask_button = QPushButton("Ask again")
        ask_button.clicked.connect(on_ask)

        hide_button = QPushButton("Hide")
        hide_button.setProperty("variant", "ghost")
        hide_button.clicked.connect(self.hide)

        quit_button = QPushButton("Quit")
        quit_button.setProperty("variant", "danger")
        quit_button.clicked.connect(on_quit)

        footer = QHBoxLayout()
        footer.addWidget(ask_button)
        footer.addStretch(1)
        footer.addWidget(hide_button)
        footer.addWidget(quit_button)

        surface_layout = QVBoxLayout(surface)
        surface_layout.setContentsMargins(18, 16, 18, 16)
        surface_layout.setSpacing(12)
        surface_layout.addLayout(header)
        surface_layout.addWidget(self.answer, 1)
        surface_layout.addLayout(footer)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(surface)

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
