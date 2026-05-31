from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QColor, QCursor, QPainter
from PySide6.QtWidgets import QLabel, QWidget


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
        self.setFixedSize(260, 92)

        self.message = QLabel("MouseAgent", self)
        self.message.setGeometry(44, 12, 204, 68)
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

