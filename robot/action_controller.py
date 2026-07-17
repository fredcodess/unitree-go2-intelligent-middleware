import asyncio
import json

from unitree_webrtc_connect.constants import (
    RTC_TOPIC,
    SPORT_CMD,
)


class ActionController:

    def __init__(self, conn):

        self.conn = conn
        self.initialized = False

        #
        # Approximate robot speeds
        #
        self.linear_speed = 0.4      # m/s
        self.angular_speed = 45.0    # deg/s

    ############################################################

    async def initialize(self):

        if self.initialized:
            return

        print("Checking motion mode...")

        response = await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["MOTION_SWITCHER"],
            {"api_id": 1001},
        )

        data = json.loads(response["data"]["data"])

        mode = data["name"]

        print(f"Motion mode: {mode}")

        if mode != "normal":

            print("Switching to NORMAL mode...")

            await self.conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["MOTION_SWITCHER"],
                {
                    "api_id": 1002,
                    "parameter": {
                        "name": "normal"
                    },
                },
            )

            print("Waiting for robot...")

            await asyncio.sleep(5)

        self.initialized = True

        print("Robot ready.")

    ############################################################

    async def _move(self, x=0.0, y=0.0, z=0.0, duration=2.0):

        end = asyncio.get_running_loop().time() + duration

        while asyncio.get_running_loop().time() < end:

            await self.conn.datachannel.pub_sub.publish_request_new(
                RTC_TOPIC["SPORT_MOD"],
                {
                    "api_id": SPORT_CMD["Move"],
                    "parameter": {
                        "x": x,
                        "y": y,
                        "z": z,
                    },
                },
            )

            await asyncio.sleep(0.05)

        await self.stop()

    ############################################################

    async def hello(self):

        print("Hello")

        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {
                "api_id": SPORT_CMD["Hello"]
            },
        )

    ############################################################

    async def sit(self):

        print("Sit")

        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {
                "api_id": SPORT_CMD["StandDown"]
            },
        )

    ############################################################

    async def stand(self):

        print("Stand")

        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {
                "api_id": SPORT_CMD["StandUp"]
            },
        )

    ############################################################
    # Linear Motion
    ############################################################

    async def forward(
        self,
        speed=0.4,
        duration=2,
        distance=None,
    ):

        print("Forward")

        if distance is not None:

            duration = distance / max(speed, 0.01)

        await self._move(
            x=speed,
            duration=duration,
        )

    ############################################################

    async def backward(
        self,
        speed=0.4,
        duration=2,
        distance=None,
    ):

        print("Backward")

        if distance is not None:

            duration = distance / max(speed, 0.01)

        await self._move(
            x=-speed,
            duration=duration,
        )

    ############################################################

    async def left(
        self,
        speed=0.35,
        duration=2,
    ):

        print("Left")

        await self._move(
            y=speed,
            duration=duration,
        )

    ############################################################

    async def right(
        self,
        speed=0.35,
        duration=2,
    ):

        print("Right")

        await self._move(
            y=-speed,
            duration=duration,
        )

    ############################################################
    # Rotation
    ############################################################

    async def rotate_left(
        self,
        angle=90,
        speed=0.6,
    ):

        print(f"Rotate Left ({angle}°)")

        duration = angle / self.angular_speed

        await self._move(
            z=speed,
            duration=duration,
        )

    ############################################################

    async def rotate_right(
        self,
        angle=90,
        speed=0.6,
    ):

        print(f"Rotate Right ({angle}°)")

        duration = angle / self.angular_speed

        await self._move(
            z=-speed,
            duration=duration,
        )

    ############################################################

    async def stop(self):

        print("Stop")

        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {
                "api_id": SPORT_CMD["StopMove"]
            },
        )

    ############################################################
    # Tricks
    ############################################################

    async def jump(self):

        print("Front Jump")

        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {
                "api_id": SPORT_CMD["FrontJump"]
            },
        )

    ############################################################

    async def jump_forward(self):

        print("Front Pounce")

        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {
                "api_id": SPORT_CMD["FrontPounce"]
            },
        )

    ############################################################

    async def dance(self):

        print("Dance")

        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {
                "api_id": SPORT_CMD["Dance1"]
            },
        )

    ############################################################

    async def stretch(self):

        print("Stretch")

        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {
                "api_id": SPORT_CMD["Stretch"]
            },
        )

    ############################################################

    async def heart(self):

        print("Finger Heart")

        await self.conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["SPORT_MOD"],
            {
                "api_id": SPORT_CMD["FingerHeart"]
            },
        )