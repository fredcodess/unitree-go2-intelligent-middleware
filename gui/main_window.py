from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui.chat_page import ChatPage
from gui.worker import AssistantWorker


class MainWindow(QMainWindow):

    ############################################################
    # Signals sent TO worker thread
    ############################################################

    process_request = Signal(str)
    microphone_request = Signal()

    ############################################################

    def __init__(self):
        super().__init__()

        self.setWindowTitle("🤖 GO2 AI Assistant")

        self.resize(1300, 800)

        ########################################################

        central = QWidget()

        self.setCentralWidget(central)

        root = QHBoxLayout(central)

        ########################################################
        # LEFT
        ########################################################

        left = QVBoxLayout()

        title = QLabel("🤖 GO2 AI Assistant")

        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        """)

        left.addWidget(title)

        ########################################################

        self.chat = ChatPage()

        left.addWidget(self.chat)

        ########################################################

        bottom = QHBoxLayout()

        self.message = QLineEdit()

        self.message.setPlaceholderText(
            "Type a message..."
        )

        self.send_button = QPushButton("Send")

        self.mic_button = QPushButton("🎤")

        bottom.addWidget(self.message)

        bottom.addWidget(self.send_button)

        bottom.addWidget(self.mic_button)

        left.addLayout(bottom)

        ########################################################

        self.status = QLabel("● Ready")

        left.addWidget(self.status)

        ########################################################
        # RIGHT PANEL
        ########################################################

        panel = QFrame()

        panel.setFixedWidth(300)

        panel_layout = QVBoxLayout(panel)

        planner = QLabel("Planner")

        planner.setStyleSheet("""
        font-size:20px;
        font-weight:bold;
        """)

        panel_layout.addWidget(planner)

        self.confidence = QLabel(
            "Confidence: --"
        )

        panel_layout.addWidget(self.confidence)

        panel_layout.addSpacing(20)

        actions = QLabel("Actions")

        panel_layout.addWidget(actions)

        self.action_list = QListWidget()

        panel_layout.addWidget(self.action_list)

        panel_layout.addStretch()

        ########################################################

        root.addLayout(left, 4)

        root.addWidget(panel, 1)

        ########################################################
        # Worker Thread
        ########################################################

        self.thread = QThread()

        self.worker = AssistantWorker()

        self.worker.moveToThread(self.thread)

        #
        # GUI -> Worker
        #

        self.process_request.connect(
            self.worker.process
        )

        self.microphone_request.connect(
            self.worker.listen
        )

        #
        # Worker -> GUI
        #

        self.worker.response_ready.connect(
            self.chat.add_robot
        )

        self.worker.user_ready.connect(
            self.chat.add_user
        )

        self.worker.status.connect(
            self.set_status
        )

        self.worker.planner_ready.connect(
            self.on_plan
        )

        self.worker.error.connect(
            self.on_error
        )

        self.thread.start()

        ########################################################
        # Signals
        ########################################################

        self.send_button.clicked.connect(
            self.send_clicked
        )

        self.message.returnPressed.connect(
            self.send_clicked
        )

        self.mic_button.clicked.connect(
            self.mic_clicked
        )

        ########################################################

        self.chat.add_robot(
            "Hello! I'm GO2. How can I help?"
        )

    ############################################################

    def send_clicked(self):

        text = self.message.text().strip()

        if not text:
            return

        self.chat.add_user(text)

        self.message.clear()

        self.process_request.emit(text)

    ############################################################

    def mic_clicked(self):

        self.microphone_request.emit()

    ############################################################

    def set_status(self, text):

        self.status.setText(text)

    ############################################################

    def on_plan(self, confidence, actions):

        self.confidence.setText(
            f"Confidence: {confidence:.2f}"
        )

        self.action_list.clear()

        for action in actions:

            self.action_list.addItem(
                str(action)
            )

    ############################################################

    def on_error(self, message):

        self.chat.add_robot(
            f"⚠ {message}"
        )

    ############################################################

    def closeEvent(self, event):

        self.thread.quit()

        self.thread.wait()

        super().closeEvent(event)