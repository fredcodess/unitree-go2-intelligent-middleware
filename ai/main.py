import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(PROJECT_ROOT / "robot"))

from echo_service import EchoService
from robot_planner import RobotPlanner


ACTION_FILE = (
    PROJECT_ROOT
    / "shared"
    / "action.json"
)

WAKE_WORDS = [
    "go2",
    "go to",
    "go too",
    "robot",
]


############################################################


def save_plan(actions):

    with open(ACTION_FILE, "w") as f:

        json.dump(
            {
                "actions": actions
            },
            f,
            indent=4,
        )


############################################################


def main():

    echo = EchoService()

    planner = RobotPlanner()

    print("=" * 50)
    print(" AI Voice Assistant Started ")
    print("=" * 50)

    printed = False

    while True:

        ####################################################
        # Listen for wake word
        ####################################################

        if not printed:

            print("\nListening for wake word...")

            printed = True

        wake = echo.listen(seconds=2)

        if wake is None:

            continue

        print(f"Heard: {wake}")

        wake = wake.lower()

        if not any(word in wake for word in WAKE_WORDS):

            continue

        printed = False

        print("\nWake word detected!")

        ####################################################
        # Record command
        ####################################################

        audio = echo.record(seconds=5)

        user_text = echo.transcribe(audio)

        if user_text is None:

            continue

        print(f"\nYou:\n{user_text}")

        ####################################################
        # Ask planner
        ####################################################

        plan = planner.plan(user_text)

        speech = plan["speech"]

        confidence = plan["confidence"]

        actions = plan["actions"]

        print("\n==============================")

        print(f"Confidence : {confidence:.2f}")

        print("\nSpeech:")

        print(speech)

        print("\nActions:")

        print(actions)

        print("==============================")

        ####################################################
        # Generate speech
        ####################################################

        sample_rate, speech_audio = echo.synthesize(
            speech
        )

        echo.save(
            speech_audio,
            sample_rate,
        )

        ####################################################
        # Safety
        ####################################################

        if confidence >= 0.80 and len(actions) > 0:

            print("\nPlanner accepted.")

            save_plan(actions)

        else:

            print("\nPlanner rejected.")

            print("Robot will speak only.")

        ####################################################
        # Wait until robot has finished
        ####################################################

        echo.wait_until_robot_finished()


############################################################


if __name__ == "__main__":

    main()