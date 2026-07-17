import soundfile as sf

from streaming_track import StreamingAudioTrack


class RobotSpeaker:

    def __init__(self, conn):

        self.track = StreamingAudioTrack()

        self.conn = conn

        # Add ONE audio track when the connection is created.
        self.conn.pc.addTrack(self.track)

        print("Persistent audio track created.")

    async def play(self, wav_file):

        print(f"Loading {wav_file}")

        audio, sample_rate = sf.read(
            wav_file,
            dtype="float32",
        )

        print(
            f"Loaded {len(audio)} samples @ {sample_rate} Hz"
        )

        await self.track.enqueue_audio(
            audio,
            sample_rate,
        )

        print("Audio queued for playback.")