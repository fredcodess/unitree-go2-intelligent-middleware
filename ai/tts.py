from pathlib import Path
import numpy as np

from piper.voice import PiperVoice


class TextToSpeechService:

    def __init__(self, voice_path=None):

        if voice_path is None:
            voice_path = (
                Path(__file__).resolve().parent
                / "voices"
                / "en_US-lessac-medium.onnx"
            )

        self.voice = PiperVoice.load(voice_path)

    def synthesize(self, text: str):

        pieces = []

        sample_rate = None

        for chunk in self.voice.synthesize(text):

            sample_rate = chunk.sample_rate

            pieces.append(chunk.audio_float_array)

        if not pieces:

            raise RuntimeError("Piper produced no audio")

        audio = np.concatenate(pieces)

        return sample_rate, audio