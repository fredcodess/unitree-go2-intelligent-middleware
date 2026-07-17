import asyncio
import numpy as np
import librosa
import soundfile as sf

class RobotMicrophone:

    def __init__(self):

        self.queue = asyncio.Queue()

    async def callback(self, frame):

        audio = frame.to_ndarray()

        # Shape is (1, 1920)
        audio = np.asarray(audio).astype(np.int16)

        await self.queue.put(audio)

    async def record(self, seconds=5):

        print(f"Recording from Go2 for {seconds} seconds...")

        chunks = []

        collected = 0

        target_samples = 48000 * seconds

        while collected < target_samples:

            chunk = await self.queue.get()

            chunks.append(chunk)

            collected += chunk.size

        audio = np.concatenate(chunks, axis=1)

        # (1,N) -> (N,)
        audio = audio.flatten()

        # int16 -> float32
        audio = audio.astype(np.float32) / 32768.0

        # 48k -> 16k
        audio = librosa.resample(
            audio,
            orig_sr=48000,
            target_sr=16000,
        )

        sf.write(
            "robot_mic.wav",
            audio,
            16000,
        )

        print("Saved robot_mic.wav")

        return audio