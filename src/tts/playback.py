"""Plays synthesized audio in a way that can be interrupted immediately.

The old engine used `playsound()`, which blocks until the file finishes
with no way to cut it short - there was no way to implement "moderator
interrupts the TTS" on top of it. sounddevice gives us `sd.stop()`, which
kills whatever's currently playing right away.
"""

from __future__ import annotations

import threading
import time

import numpy as np
import sounddevice as sd

POLL_INTERVAL_SECONDS = 0.02


class InterruptiblePlayer:
    def __init__(self):
        self._stop_event = threading.Event()

    def play(self, samples: np.ndarray, sample_rate: int, volume: float = 1.0):
        """Blocks until playback finishes or `interrupt()` is called."""
        self._stop_event.clear()
        audio = samples.astype(np.float32) / 32768.0
        if volume != 1.0:
            audio = audio * max(0.0, min(volume, 2.0))

        sd.play(audio, samplerate=sample_rate)
        try:
            while True:
                stream = sd.get_stream()
                if stream is None or not stream.active:
                    break
                if self._stop_event.is_set():
                    sd.stop()
                    break
                time.sleep(POLL_INTERVAL_SECONDS)
        finally:
            pass

    def interrupt(self):
        self._stop_event.set()
        sd.stop()
