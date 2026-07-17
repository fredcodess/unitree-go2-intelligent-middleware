from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from chat_bubble import ChatBubble


class ChatPage(QScrollArea):

    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.NoFrame)

        self.container = QWidget()

        self.setWidget(self.container)

        self.layout = QVBoxLayout(self.container)

        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignTop)

        self.layout.addStretch()

    ############################################################

    def _add(self, text, user):

        bubble = ChatBubble(text, user)

        self.layout.insertWidget(
            self.layout.count() - 1,
            bubble,
        )

        self.scroll_to_bottom()

        return bubble

    ############################################################

    def add_user(self, text):

        return self._add(text, True)

    ############################################################

    def add_robot(self, text):

        return self._add(text, False)

    ############################################################

    def scroll_to_bottom(self):

        bar = self.verticalScrollBar()

        bar.setValue(bar.maximum())