import re


class ActionParser:

    def __init__(self):

        self.commands = {

            # ----------------------------------------------------
            # Stand
            # ----------------------------------------------------

            "stand": (
                [
                    "stand",
                    "stand up",
                    "get up",
                    "rise",
                    "stand straight",
                ],
                "Okay, standing up.",
            ),

            # ----------------------------------------------------

            "sit": (
                [
                    "sit",
                    "sit down",
                    "take a seat",
                ],
                "Okay, sitting down.",
            ),

            # ----------------------------------------------------

            "forward": (
                [
                    "forward",
                    "go forward",
                    "move forward",
                    "walk forward",
                    "come forward",
                    "advance",
                ],
                "Okay, moving forward.",
            ),

            # ----------------------------------------------------

            "backward": (
                [
                    "backward",
                    "go backward",
                    "move backward",
                    "back up",
                    "reverse",
                    "back",
                ],
                "Okay, moving backward.",
            ),

            # ----------------------------------------------------

            "left": (
                [
                    "step left",
                    "move left",
                    "strafe left",
                ],
                "Moving left.",
            ),

            # ----------------------------------------------------

            "right": (
                [
                    "step right",
                    "move right",
                    "strafe right",
                ],
                "Moving right.",
            ),

            # ----------------------------------------------------

            "rotate_left": (
                [
                    "turn left",
                    "rotate left",
                    "face left",
                    "spin left",
                ],
                "Turning left.",
            ),

            # ----------------------------------------------------

            "rotate_right": (
                [
                    "turn right",
                    "rotate right",
                    "face right",
                    "spin right",
                ],
                "Turning right.",
            ),

            # ----------------------------------------------------

            "stop": (
                [
                    "stop",
                    "halt",
                    "freeze",
                    "don't move",
                    "stay",
                ],
                "Stopping.",
            ),

            # ----------------------------------------------------

            "hello": (
                [
                    "hello",
                    "wave",
                    "say hello",
                    "greet",
                ],
                "Hello!",
            ),

            # ----------------------------------------------------

            "jump": (
                [
                    "jump",
                ],
                "Jumping.",
            ),

            # ----------------------------------------------------

            "jump_forward": (
                [
                    "jump forward",
                    "leap forward",
                    "pounce",
                ],
                "Jumping forward.",
            ),

            # ----------------------------------------------------

            "dance": (
                [
                    "dance",
                ],
                "Let's dance!",
            ),

            # ----------------------------------------------------

            "stretch": (
                [
                    "stretch",
                ],
                "Stretching.",
            ),

            # ----------------------------------------------------

            "heart": (
                [
                    "heart",
                    "finger heart",
                    "love",
                ],
                "Making a heart for you.",
            ),

            # ----------------------------------------------------

            "wiggle": (
                [
                    "wiggle",
                    "shake",
                    "shake your hips",
                ],
                "Wiggling.",
            ),

        }

    #################################################################

    def clean(self, text):

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9 ]",
            "",
            text,
        )

        return text

    #################################################################

    def parse(self, text):

        if text is None:

            return None

        text = self.clean(text)

        for action, (phrases, reply) in self.commands.items():

            for phrase in phrases:

                if phrase in text:

                    return {

                        "action": action,

                        "reply": reply,

                        "text": text,

                    }

        return None