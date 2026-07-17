import asyncio
import fractions
import time

import numpy as np
from scipy.signal import resample_poly

from aiortc import AudioStreamTrack
from aiortc.mediastreams import AUDIO_PTIME, MediaStreamError
from av import AudioFrame


TARGET_SAMPLE_RATE = 48000


class StreamingAudioTrack(AudioStreamTrack):

    kind = "audio"

    def __init__(self):

        super().__init__()

        #
        # Keep ONE sample rate for the lifetime of the track.
        #

        self.sample_rate = TARGET_SAMPLE_RATE

        self.samples_per_frame = int(
            AUDIO_PTIME * self.sample_rate
        )

        self.queue = asyncio.Queue()

    ############################################################

    async def enqueue_audio(
        self,
        audio,
        sample_rate,
    ):

        #
        # Mono
        #

        if audio.ndim > 1:

            audio = audio[:, 0]

        #
        # Normalize
        #

        audio = np.clip(audio, -1.0, 1.0)

        #
        # Convert everything to 48 kHz
        #

        if sample_rate != TARGET_SAMPLE_RATE:

            audio = resample_poly(
                audio,
                TARGET_SAMPLE_RATE,
                sample_rate,
            )

        #
        # Convert to int16 PCM
        #

        pcm = (audio * 32767).astype(np.int16)

        #
        # Queue fixed-size frames
        #

        i = 0

        while i < len(pcm):

            chunk = pcm[
                i : i + self.samples_per_frame
            ]

            if len(chunk) < self.samples_per_frame:

                chunk = np.pad(
                    chunk,
                    (
                        0,
                        self.samples_per_frame - len(chunk),
                    ),
                    mode="constant",
                )

            await self.queue.put(chunk)

            i += self.samples_per_frame

    ############################################################

    async def recv(self):

        if self.readyState != "live":

            raise MediaStreamError

        ########################################################
        # Timing
        ########################################################

        if hasattr(self, "_timestamp"):

            self._timestamp += self.samples_per_frame

            wait = (
                self._start
                + self._timestamp / self.sample_rate
                - time.time()
            )

            if wait > 0:

                await asyncio.sleep(wait)

        else:

            self._start = time.time()

            self._timestamp = 0

        ########################################################
        # Audio
        ########################################################

        try:

            chunk = self.queue.get_nowait()

        except asyncio.QueueEmpty:

            chunk = np.zeros(
                self.samples_per_frame,
                dtype=np.int16,
            )

        frame = AudioFrame.from_ndarray(
            chunk.reshape(1, -1),
            format="s16",
            layout="mono",
        )

        frame.sample_rate = self.sample_rate

        frame.time_base = fractions.Fraction(
            1,
            self.sample_rate,
        )

        frame.pts = self._timestamp

        return frame