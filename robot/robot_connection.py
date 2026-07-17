import os

from unitree_webrtc_connect.webrtc_driver import (
    UnitreeWebRTCConnection,
    WebRTCConnectionMethod,
)


class RobotConnection:
    """
    Handles the WebRTC connection to the Unitree Go2.

    Responsibilities:
    - Connect
    - Disconnect
    - Expose the underlying WebRTC connection

    Nothing else.
    """

    def __init__(self):

        self.conn = None

        self.aes_key = os.environ.get(
            "UNITREE_AES_KEY",
            "...",
        )


    async def connect(self):

        if self.conn is not None:
            return

        self.conn = UnitreeWebRTCConnection(
            WebRTCConnectionMethod.LocalAP,
            aes_128_key=self.aes_key,
        )

        print("Connecting to robot...")

        await self.conn.connect()

        print("Robot Connected")


    async def disconnect(self):

        if self.conn is None:
            return

        print("Disconnecting robot...")

        await self.conn.disconnect()

        self.conn = None

        print("Robot Disconnected")