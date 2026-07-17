# import sounddevice as sd
# import soundfile as sf
# import time

# from pathlib import Path

# from whisper_service import WhisperService
# from tts import TextToSpeechService


# class EchoService:

#     def __init__(self):

#         self.sample_rate = 16000

#         self.whisper = WhisperService()

#         self.tts = TextToSpeechService()

#         # voice_assistant/
#         project_root = Path(__file__).resolve().parent.parent

#         # voice_assistant/shared/audio/
#         self.audio_dir = project_root / "shared" / "audio"

#         self.audio_dir.mkdir(
#             parents=True,
#             exist_ok=True,
#         )

#         self.output_file = self.audio_dir / "echo.wav"


#     def record(self):

#         print("\nRecording...")

#         audio = sd.rec(
#             self.sample_rate * 5,
#             samplerate=self.sample_rate,
#             channels=1,
#             dtype="float32",
#         )

#         sd.wait()

#         return audio.squeeze()
    
#     def listen(self, seconds=2):

#         print("Listening for wake word...")
        
#         audio = sd.rec(
#             int(self.sample_rate * seconds),
#             samplerate=self.sample_rate,
#             channels=1,
#             dtype="float32",
#         )

#         sd.wait()

#         text = self.transcribe(audio.squeeze())

#         return text


#     def transcribe(self, audio):

#         text = self.whisper.transcribe(audio)

#         if text is None:
#             return None

#         text = text.strip()

#         if text == "":
#             return None

#         return text


#     def synthesize(self, text):

#         sample_rate, audio = self.tts.long_form_synthesize(
#             text
#         )

#         return sample_rate, audio


#     def save(self, audio, sample_rate):

#         sf.write(
#             self.output_file,
#             audio,
#             sample_rate,
#         )

#         print(f"Saved: {self.output_file}")

#     def wait_until_robot_finished(self):

#         while self.output_file.exists():

#             time.sleep(0.2)

#     def run(self):

#         audio = self.record()

#         text = self.transcribe(audio)

#         if text is None:
#             return None

#         print(f"\nYou said:\n{text}")

#         sample_rate, audio = self.synthesize(text)

#         self.save(audio, sample_rate)

#         return text

import time
import os
from pathlib import Path

import sounddevice as sd
import soundfile as sf

from ai.whisper_service import WhisperService
from ai.llm import RobotLLM
from ai.tts import TextToSpeechService

class EchoService:

    def __init__(self):

        self.sample_rate = 16000

        print("Loading Whisper...")

        self.whisper = WhisperService()

        self.llm = RobotLLM()

        self.tts = TextToSpeechService()

        project_root = Path(__file__).resolve().parent.parent

        self.audio_dir = project_root / "shared" / "audio"

        self.audio_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.output_file = self.audio_dir / "echo.wav"

    ###############################################################
    # RECORD
    ###############################################################

    def record(self, seconds=5):

        print("\nRecording...")

        audio = sd.rec(
            int(self.sample_rate * seconds),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
        )

        sd.wait()

        return audio.squeeze()

    ###############################################################
    # WAKE WORD LISTEN
    ###############################################################

    def listen(self, seconds=2):

        audio = self.record(seconds)

        return self.transcribe(audio)

    ###############################################################
    # SPEECH TO TEXT
    ###############################################################

    def transcribe(self, audio):

        text = self.whisper.transcribe(audio)

        if text is None:
            return None

        text = text.strip()

        if text == "":
            return None

        return text

    ###############################################################
    # LLM
    ###############################################################

    def think(self, user_text):

        print("\nThinking...")

        reply = self.llm.chat(user_text)

        print(f"\nGo2:\n{reply}")

        return reply

    ###############################################################
    # TTS
    ###############################################################

    def synthesize(self, text):

        sample_rate, audio = self.tts.synthesize(text)

        return sample_rate, audio

    ###############################################################
    # SAVE AUDIO
    ###############################################################

    def save(self, audio, sample_rate):

        print(f"\nSaving to: {self.output_file}")
        print(f"Exists before save: {self.output_file.exists()}")

        sf.write(
            self.output_file,
            audio,
            sample_rate,
        )

        print("Absolute path:", os.path.abspath(self.output_file))

        print(f"Exists after save: {self.output_file.exists()}")

    ###############################################################
    # WAIT UNTIL ROBOT FINISHES PLAYING
    ###############################################################

    def wait_until_robot_finished(self):

        print("\nWaiting for robot...")

        while self.output_file.exists():

            time.sleep(0.2)

        print("Robot finished.")

    ###############################################################
    # SAY ANY TEXT
    ###############################################################

    def say(self, text):

        print(f"\nGo2:\n{text}")

        sample_rate, speech = self.synthesize(text)

        self.save(
            speech,
            sample_rate,
        )

        self.wait_until_robot_finished()

    ###############################################################
    # NORMAL CHAT
    ###############################################################

    def chat(self, user_text):

        reply = self.think(user_text)

        self.say(reply)

        return reply

    ###############################################################
    # COMPLETE CONVERSATION
    ###############################################################

    def run(self):

        audio = self.record()

        user_text = self.transcribe(audio)

        if user_text is None:

            return None

        print(f"\nYou:\n{user_text}")

        self.chat(user_text)

        return user_text