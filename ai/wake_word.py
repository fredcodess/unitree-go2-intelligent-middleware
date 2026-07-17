import numpy as np
import sounddevice as sd

from openwakeword.model import Model


class WakeWordDetector:

    def __init__(self):

        print("Loading wake word model...")

        self.model = Model(
            inference_framework="onnx"
        )

        self.sample_rate = 16000

        self.chunk_size = 1280

        self.threshold = 0.5

        print("Wake word ready.")

    def wait(self):

        print("Listening for wake word...")

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            blocksize=self.chunk_size,
        ) as stream:

            while True:

                audio, overflow = stream.read(
                    self.chunk_size
                )

                audio = audio.flatten()

                prediction = self.model.predict(audio)

                for score in prediction.values():

                    if score > self.threshold:

                        print("Wake word detected!")

                        return