from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class ChatBubble(QWidget):

    MAX_WIDTH = 550

    def __init__(self, text: str, user: bool):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)

        self.label = QLabel(text)

        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        self.label.setMaximumWidth(self.MAX_WIDTH)

        self.label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred,
        )

        if user:

            self.label.setStyleSheet("""
            QLabel{
                background:#2563eb;
                color:white;
                border-radius:14px;
                padding:12px;
            }
            """)

            layout.setAlignment(Qt.AlignRight)

        else:

            self.label.setStyleSheet("""
            QLabel{
                background:#2f3136;
                color:white;
                border-radius:14px;
                padding:12px;
            }
            """)

            layout.setAlignment(Qt.AlignLeft)

        layout.addWidget(self.label)

    ####################################################

    def set_text(self, text):

        self.label.setText(text)

    ####################################################

    def append_text(self, text):

        self.label.setText(
            self.label.text() + text
        )