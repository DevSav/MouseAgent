from __future__ import annotations

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QColor, QCursor, QPainter
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


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
        self.setFixedSize(320, 112)

        self.message = QLabel("MouseAgent", self)
        self.message.setGeometry(44, 12, 264, 88)
        self.message.setWordWrap(True)
        self.message.setStyleSheet(
            """
            QLabel {
                color: #111827;
                background: rgba(255, 255, 255, 235);
                border: 1px solid rgba(17, 24, 39, 45);
                border-radius: 8px;
                padding: 8px 10px;
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

    @classmethod
    def ask(cls) -> str | None:
        dialog = cls()
        cursor = QCursor.pos()
        dialog.move(cursor + QPoint(24, 24))
        dialog.input.setFocus()

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None

        question = dialog.input.text().strip()
        return question or None
