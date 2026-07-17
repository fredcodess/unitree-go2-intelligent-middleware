import json
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent

SHARED = ROOT / "shared"

AUDIO_DIR = SHARED / "audio"

ACTION_FILE = SHARED / "action.json"


###############################################################


def prepare_shared_files():

    SHARED.mkdir(exist_ok=True)

    AUDIO_DIR.mkdir(exist_ok=True)

    if not ACTION_FILE.exists():

        with open(ACTION_FILE, "w") as f:

            json.dump({}, f, indent=4)


###############################################################


def banner():

    print("=" * 60)
    print("Starting Go2 Voice Assistant")
    print("=" * 60)


###############################################################


def main():

    banner()

    prepare_shared_files()

    robot_script = ROOT / "robot" / "main.py"

    gui_script = ROOT / "gui" / "app.py"

    ###########################################################

    print("\nStarting Robot Service...\n")

    robot = subprocess.Popen(
        [sys.executable, str(robot_script)]
    )

    #
    # Give robot enough time to establish
    # the single WebRTC connection.
    #

    time.sleep(5)

    ###########################################################

    print("\nStarting GUI...\n")

    gui = subprocess.Popen(
        [sys.executable, str(gui_script)]
    )

    ###########################################################

    try:

        robot.wait()

        gui.wait()

    except KeyboardInterrupt:

        print("\nStopping services...")

        gui.terminate()

        robot.terminate()

        gui.wait()

        robot.wait()

        print("Done.")


###############################################################


if __name__ == "__main__":

    main()