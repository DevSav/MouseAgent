from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QColor, QCursor, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from mouseagent.settings import AppSettings


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
QComboBox {
    background: rgba(4, 12, 24, 220);
    color: #f8fbff;
    border: 1px solid rgba(48, 230, 255, 96);
    border-radius: 10px;
    padding: 8px 10px;
}
QComboBox QAbstractItemView {
    background: #061426;
    color: #f8fbff;
    border: 1px solid rgba(48, 230, 255, 120);
    selection-background-color: rgba(48, 230, 255, 70);
    selection-color: #ffffff;
}
QComboBox::drop-down {
    border: 0;
    width: 24px;
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


def move_inside_screen(widget: QWidget, preferred: QPoint, margin: int = 16) -> None:
    screen = QApplication.screenAt(preferred) or QApplication.primaryScreen()
    if screen is None:
        widget.move(preferred)
        return

    area = screen.availableGeometry()
    size = widget.sizeHint()
    if not size.isValid() or size.width() <= 0 or size.height() <= 0:
        size = widget.size()

    width = max(size.width(), widget.width())
    height = max(size.height(), widget.height())

    min_x = area.left() + margin
    min_y = area.top() + margin
    max_x = area.right() - width - margin + 1
    max_y = area.bottom() - height - margin + 1

    x = max(min_x, min(preferred.x(), max_x))
    y = max(min_y, min(preferred.y(), max_y))
    widget.move(x, y)


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
        self.setFixedSize(34, 34)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.follow_cursor)
        self.timer.start(16)

    def follow_cursor(self) -> None:
        self.move(QCursor.pos() + QPoint(16, 16))

    def show_message(self, text: str) -> None:
        self.show()

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.setBrush(QColor(48, 230, 255, 42))
        painter.drawEllipse(1, 1, 32, 32)
        painter.setBrush(QColor(48, 230, 255))
        painter.drawEllipse(8, 8, 18, 18)
        painter.setBrush(QColor(120, 255, 214))
        painter.drawEllipse(14, 14, 6, 6)


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
        move_inside_screen(dialog, QCursor.pos() + QPoint(24, 24))

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None

        question = dialog.input.text().strip()
        return question or None


class SettingsDialog(QDialog):
    def __init__(self, settings: AppSettings) -> None:
        super().__init__()
        self.setWindowTitle("MouseAgent Settings")
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
                background: rgba(3, 10, 22, 238);
                border: 1px solid rgba(48, 230, 255, 82);
                border-radius: 18px;
            }
            """
        )

        title = QLabel("Settings")
        title.setStyleSheet("font-size: 18px; font-weight: 600; color: #f8fbff;")

        subtitle = QLabel("Choose how MouseAgent answers screen questions.")
        subtitle.setStyleSheet("color: #8aa4c5;")

        self.provider = QComboBox()
        self.provider.addItem("Mock", "mock")
        self.provider.addItem("Gemini", "gemini")
        self.provider.addItem("Ollama", "ollama")
        provider_index = self.provider.findData(settings.provider)
        self.provider.setCurrentIndex(max(provider_index, 0))

        self.gemini_api_key = QLineEdit(settings.gemini_api_key)
        self.gemini_api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.gemini_api_key.setPlaceholderText("Gemini API key")

        self.gemini_model = QLineEdit(settings.gemini_model)
        self.gemini_model.setPlaceholderText("gemini-2.5-flash")
        self.ollama_url = QLineEdit(settings.ollama_url)
        self.ollama_url.setPlaceholderText("http://localhost:11434")
        self.ollama_model = QLineEdit(settings.ollama_model)
        self.ollama_model.setPlaceholderText("llama3.2-vision")

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setFormAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(10)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form.addRow("Provider", self.provider)
        form.addRow("Gemini key", self.gemini_api_key)
        form.addRow("Gemini model", self.gemini_model)
        form.addRow("Ollama URL", self.ollama_url)
        form.addRow("Ollama model", self.ollama_model)

        save_button = QPushButton("Save")
        save_button.setDefault(True)
        save_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Cancel")
        cancel_button.setProperty("variant", "ghost")
        cancel_button.clicked.connect(self.reject)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        buttons.addWidget(cancel_button)
        buttons.addWidget(save_button)

        layout = QVBoxLayout(surface)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(form)
        layout.addLayout(buttons)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(surface)

    def to_settings(self, previous: AppSettings) -> AppSettings:
        return AppSettings(
            provider=self.provider.currentData(),
            shortcut=previous.shortcut,
            voice_enabled=previous.voice_enabled,
            gemini_api_key=self.gemini_api_key.text().strip(),
            gemini_model=self.gemini_model.text().strip() or "gemini-2.5-flash",
            ollama_url=self.ollama_url.text().strip() or "http://localhost:11434",
            ollama_model=self.ollama_model.text().strip() or "llama3.2-vision",
        )

    @classmethod
    def edit(cls, settings: AppSettings) -> AppSettings | None:
        dialog = cls(settings)
        screen = QApplication.primaryScreen()
        if screen is not None:
            area = screen.availableGeometry()
            move_inside_screen(dialog, area.center() - QPoint(dialog.width() // 2, 180))

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None

        return dialog.to_settings(settings)


class AnswerWindow(QWidget):
    def __init__(
        self,
        on_ask: Callable[[], None],
        on_settings: Callable[[], None],
        on_quit: Callable[[], None],
    ) -> None:
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

        settings_button = QPushButton("Settings")
        settings_button.setProperty("variant", "ghost")
        settings_button.clicked.connect(on_settings)

        hide_button = QPushButton("Hide")
        hide_button.setProperty("variant", "ghost")
        hide_button.clicked.connect(self.hide)

        quit_button = QPushButton("Quit")
        quit_button.setProperty("variant", "danger")
        quit_button.clicked.connect(on_quit)

        footer = QHBoxLayout()
        footer.addWidget(ask_button)
        footer.addWidget(settings_button)
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

    def show_answer(self, question: str, text: str, app_name: str = "") -> None:
        label = f"[{app_name}]  {question}" if app_name and app_name != "unknown" else question
        self.question.setText(label)
        self.answer.setMarkdown(text)
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
        move_inside_screen(self, QPoint(x, y), margin=margin)
