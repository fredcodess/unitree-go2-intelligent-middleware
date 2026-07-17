import json

from ai.llm import RobotLLM


VALID_ACTIONS = {
    "stand",
    "sit",
    "forward",
    "backward",
    "left",
    "right",
    "rotate_left",
    "rotate_right",
    "jump",
    "jump_forward",
    "dance",
    "stretch",
    "heart",
    "hello",
    "stop",
}


SYSTEM_PROMPT = """
You are the task planner for a Unitree Go2 robot.

Your job is to convert a user's request into a robot execution plan.

The robot ONLY supports these actions:

stand
sit
forward
backward
left
right
rotate_left
rotate_right
jump
jump_forward
dance
stretch
heart
hello
stop

Return ONLY valid JSON.

The JSON MUST have exactly these fields:

{
    "speech": "...",
    "confidence": 0.0,
    "actions": []
}

Rules:

1. Never return markdown.
2. Never explain your reasoning.
3. Never invent robot actions.
4. Never guess the user's intent.
5. Never replace an unsupported action with another action.
6. If you are not highly confident, return:
   - confidence below 0.8
   - actions = []
7. If the request is conversational, answer normally with actions=[].
8. Only use supported actions.
9. Preserve the order requested by the user.
10. Multiple actions are allowed.

Examples

User:
Move backwards then jump.

Output:

{
    "speech":"Sure! I'll move backwards and then jump.",
    "confidence":0.99,
    "actions":[
        {"action":"backward"},
        {"action":"jump"}
    ]
}

User:
Move forward one meter.

Output:

{
    "speech":"Sure! I'll move forward one meter.",
    "confidence":0.98,
    "actions":[
        {
            "action":"forward",
            "distance":1.0,
            "speed":0.3
        }
    ]
}

User:
Turn left 45 degrees then wave.

Output:

{
    "speech":"Sure! I'll turn left 45 degrees and then wave hello.",
    "confidence":0.98,
    "actions":[
        {
            "action":"rotate_left",
            "angle":45
        },
        {
            "action":"hello"
        }
    ]
}

User:
Walk like a crab.

Output:

{
    "speech":"Sorry, I don't know how to do that.",
    "confidence":0.10,
    "actions":[]
}

User:
Do something cool.

Output:

{
    "speech":"Could you be more specific about what you'd like me to do?",
    "confidence":0.20,
    "actions":[]
}

User:
I don't know.

Output:

{
    "speech":"I'm not sure what you'd like me to do.",
    "confidence":0.05,
    "actions":[]
}
"""


class RobotPlanner:

    def __init__(self):

        self.llm = RobotLLM()

    ############################################################

    def _extract_json(self, text):

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError("Planner returned no JSON.")

        return text[start:end + 1]

    ############################################################

    def plan(self, user_text):

        prompt = f"""
{SYSTEM_PROMPT}

User:
{user_text}
"""

        response = self.llm.chat(prompt)

        print("\nPlanner Output:\n")
        print(response)

        try:

            plan = json.loads(
                self._extract_json(response)
            )

        except Exception:

            return {
                "speech": "Sorry, I couldn't understand that.",
                "confidence": 0.0,
                "actions": [],
            }

        ####################################################
        # Defaults
        ####################################################

        speech = plan.get(
            "speech",
            "Sorry, I couldn't understand that."
        )

        confidence = float(
            plan.get("confidence", 0.0)
        )

        actions = plan.get("actions", [])

        ####################################################
        # Validate actions
        ####################################################

        filtered = []

        if isinstance(actions, list):

            for action in actions:

                if not isinstance(action, dict):
                    continue

                name = action.get("action")

                if name not in VALID_ACTIONS:
                    continue

                filtered.append(action)

        ####################################################
        # Safety
        ####################################################

        if confidence < 0.80:

            return {
                "speech": speech,
                "confidence": confidence,
                "actions": [],
            }

        return {
            "speech": speech,
            "confidence": confidence,
            "actions": filtered,
        }