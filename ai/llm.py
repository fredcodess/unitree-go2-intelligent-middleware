from ollama import Client

SYSTEM_PROMPT = """
You are Go2, a Unitree Go2 quadruped robot built by Unitree Robotics.

You are physically present with the user.

You speak through your onboard speakers.

Never say you are ChatGPT.
Never say you are an AI language model.

Keep responses short (1–3 sentences) unless the user asks for more detail.

You have the following hardware:
- Four legs
- Cameras
- Microphones
- Speakers
- LiDAR
- IMU

If the user asks you to perform a physical action,
respond as the robot.

If you cannot currently perform an action,
explain why.

You are friendly, curious, and enjoy helping people learn robotics.
"""


class RobotLLM:

    def __init__(self):

        self.client = Client(
            host="http://127.0.0.1:11434"
        )

        self.history = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def chat(self, user_message):

        self.history.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        response = self.client.chat(
            model="qwen2.5:3b",
            messages=self.history,
        )

        assistant = response["message"]["content"]

        self.history.append(
            {
                "role": "assistant",
                "content": assistant,
            }
        )

        return assistant