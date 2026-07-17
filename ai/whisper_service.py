import torch
import whisper
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline,
)


class WhisperService:

    def __init__(self):

        print("Loading Whisper...")

        self.model = whisper.load_model("base.en")

    def transcribe(self, audio):

        result = self.model.transcribe(
            audio,
            fp16=False
        )

        return result["text"]