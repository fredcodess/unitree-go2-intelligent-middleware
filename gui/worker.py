import json
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot

from ai.echo_service import EchoService
from robot.robot_planner import RobotPlanner


class AssistantWorker(QObject):

    ############################################################
    # Signals back to GUI
    ############################################################

    response_ready = Signal(str)

    planner_ready = Signal(float, list)

    user_ready = Signal(str)

    status = Signal(str)

    finished = Signal()

    error = Signal(str)

    ############################################################

    def __init__(self):
        super().__init__()

        self.echo = EchoService()

        self.planner = RobotPlanner()

        project_root = Path(__file__).resolve().parent.parent

        self.action_file = (
            project_root
            / "shared"
            / "action.json"
        )

    ############################################################

    def save_plan(self, actions):

        with open(self.action_file, "w") as f:

            json.dump(
                {
                    "actions": actions
                },
                f,
                indent=4,
            )

    ############################################################
    # TEXT MESSAGE
    ############################################################

    @Slot(str)
    def process(self, text):

        try:

            ####################################################
            # Planner
            ####################################################

            self.status.emit("🧠 Thinking...")

            plan = self.planner.plan(text)

            speech = plan["speech"]

            confidence = plan["confidence"]

            actions = plan["actions"]

            self.planner_ready.emit(
                confidence,
                actions,
            )

            ####################################################
            # Update chat immediately
            ####################################################

            self.response_ready.emit(speech)

            ####################################################
            # Generate speech
            ####################################################

            self.status.emit("🔊 Speaking...")

            sample_rate, audio = self.echo.synthesize(
                speech
            )

            self.echo.save(
                audio,
                sample_rate,
            )

            ####################################################
            # Send actions to robot
            ####################################################

            if confidence >= 0.80 and len(actions) > 0:

                self.save_plan(actions)

            ####################################################
            # Wait until robot has finished
            ####################################################

            self.status.emit("🤖 Executing...")

            self.echo.wait_until_robot_finished()

            ####################################################

            self.status.emit("✅ Ready")

        except Exception as e:

            self.error.emit(str(e))

        finally:

            self.finished.emit()

    ############################################################
    # MICROPHONE
    ############################################################

    @Slot()
    def listen(self):

        try:

            self.status.emit("🎤 Listening...")

            audio = self.echo.record(
                seconds=5
            )

            text = self.echo.transcribe(audio)

            if text is None:

                self.status.emit("✅ Ready")

                return

            text = text.strip()

            if text == "":

                self.status.emit("✅ Ready")

                return

            self.user_ready.emit(text)

            self.process(text)

        except Exception as e:

            self.error.emit(str(e))