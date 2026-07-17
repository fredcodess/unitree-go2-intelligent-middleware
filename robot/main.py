import asyncio
import json
from pathlib import Path

from robot_connection import RobotConnection
from speaker import RobotSpeaker
from microphone import RobotMicrophone
from action_controller import ActionController


PROJECT_ROOT = Path(__file__).resolve().parent.parent

AUDIO_FILE = (
    PROJECT_ROOT
    / "shared"
    / "audio"
    / "echo.wav"
)

ACTION_FILE = (
    PROJECT_ROOT
    / "shared"
    / "action.json"
)


############################################################
# Execute one action dictionary
############################################################

async def execute_action(controller, action):

    name = action["action"]

    repeat = action.get("repeat", 1)

    speed = action.get("speed", 0.4)

    duration = action.get("duration", 2)

    angle = action.get("angle", 90)

    distance = action.get("distance", None)

    for i in range(repeat):

        print(f"\nAction {i+1}/{repeat}: {name}")

        ####################################################

        if name == "forward":

            await controller.forward(
                speed=speed,
                duration=duration,
                distance=distance,
            )

        elif name == "backward":

            await controller.backward(
                speed=speed,
                duration=duration,
                distance=distance,
            )

        elif name == "left":

            await controller.left(
                speed=speed,
                duration=duration,
            )

        elif name == "right":

            await controller.right(
                speed=speed,
                duration=duration,
            )

        elif name == "rotate_left":

            await controller.rotate_left(
                angle=angle,
            )

        elif name == "rotate_right":

            await controller.rotate_right(
                angle=angle,
            )

        ####################################################

        elif name == "stand":

            await controller.stand()

        elif name == "sit":

            await controller.sit()

        elif name == "jump":

            await controller.jump()

        elif name == "jump_forward":

            await controller.jump_forward()

        elif name == "dance":

            await controller.dance()

        elif name == "stretch":

            await controller.stretch()

        elif name == "heart":

            await controller.heart()

        elif name == "hello":

            await controller.hello()

        elif name == "stop":

            await controller.stop()

        else:

            print(f"Unknown action: {name}")

        await asyncio.sleep(0.5)


############################################################

async def main():

    ########################################################
    # Connect Robot
    ########################################################

    robot = RobotConnection()

    await robot.connect()

    ########################################################
    # Motion
    ########################################################

    controller = ActionController(robot.conn)

    await controller.initialize()

    ########################################################
    # Audio
    ########################################################

    mic = RobotMicrophone()

    robot.conn.audio.switchAudioChannel(True)

    robot.conn.audio.add_track_callback(
        mic.callback
    )

    speaker = RobotSpeaker(robot.conn)

    ########################################################

    print("\nRobot service started.")

    print(f"Watching audio : {AUDIO_FILE}")

    print(f"Watching action: {ACTION_FILE}")

    ########################################################

    while True:

        ####################################################
        # SPEECH
        ####################################################

        if AUDIO_FILE.exists():

            print("\nDetected echo.wav")

            try:

                await speaker.play(str(AUDIO_FILE))

                AUDIO_FILE.unlink()

                print("Speech finished.")

            except Exception as e:

                print(e)

        ####################################################
        # ACTION PLAN
        ####################################################

        if ACTION_FILE.exists():

            try:

                with open(ACTION_FILE, "r") as f:

                    plan = json.load(f)

                actions = plan.get("actions", [])

                if actions:

                    print("\n========== EXECUTING PLAN ==========\n")

                for action in actions:

                    print(action)

                    await execute_action(
                        controller,
                        action,
                    )

                if actions:

                    print("\n========== PLAN COMPLETE ==========\n")

            except Exception as e:

                print(e)

            finally:

                ACTION_FILE.unlink(
                    missing_ok=True
                )

        ####################################################

        await asyncio.sleep(0.1)


############################################################

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print("\nRobot service stopped.")