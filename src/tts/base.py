"""Abstract voice-engine interface.

Anything that can turn text into (int16 PCM samples, sample_rate) can be
plugged in here - this is the seam the README's "support multiple TTS
engines" TODO hangs off of. PiperEngine is the only implementation for now.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple

import numpy as np


class VoiceEngine(ABC):
    @abstractmethod
    def synthesize(self, text: str) -> Tuple[np.ndarray, int]:
        """Return (int16 mono PCM samples, sample_rate_hz)."""
        raise NotImplementedError
