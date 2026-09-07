"""Local neural TTS backend using Piper (https://github.com/rhasspy/piper).

Piper is a small, fast, fully-offline neural TTS engine - a single voice is
typically 20-60MB and runs comfortably on CPU in real time, which is exactly
the profile this app needs (many short chat messages, no cloud round trip,
no API key). This replaces the old gTTS-over-the-network engine.
"""
from __future__ import annotations

import logging
import os
import shutil
import urllib.request
from urllib.error import URLError

import numpy as np

from src.tts.base import VoiceEngine
from src.tts.voice_models import voice_download_urls, voice_paths

VOICES_DIR = "voices"

logger = logging.getLogger(__name__)


class VoiceModelError(RuntimeError):
    """Raised when the voice model can't be loaded or downloaded."""


def _download_file(url: str, destination_path: str):
    """Download a file with a bounded timeout so a stalled network cannot hang forever."""
    logger.debug("Downloading %s -> %s", url, destination_path)
    with urllib.request.urlopen(url, timeout=30) as response, open(destination_path, "wb") as destination:
        shutil.copyfileobj(response, destination)
    logger.debug("Finished downloading %s", destination_path)


def ensure_voice_files(voice_name: str, voices_dir: str = VOICES_DIR, progress=None) -> tuple[str, str]:
    """Return (onnx_path, json_path) for a voice, downloading it first if
    it isn't on disk yet. `progress(message)` is called with human-readable
    status updates (e.g. to forward into the GUI's log)."""
    onnx_path, json_path = voice_paths(voice_name, voices_dir)
    logger.debug(
        "Checking voice files for %s: onnx=%s json=%s",
        voice_name,
        onnx_path,
        json_path,
    )
    if os.path.isfile(onnx_path) and os.path.isfile(json_path):
        logger.debug("Voice files already present for %s", voice_name)
        return onnx_path, json_path

    os.makedirs(voices_dir, exist_ok=True)
    onnx_url, json_url = voice_download_urls(voice_name)
    logger.info("Ensuring voice files for %s", voice_name)
    try:
        if not os.path.isfile(json_path):
            logger.info("Voice config missing for %s", voice_name)
            if progress:
                progress(f"Downloading voice config for {voice_name}...")
            _download_file(json_url, json_path)
        else:
            logger.debug("Voice config already cached for %s", voice_name)
        if not os.path.isfile(onnx_path):
            logger.info("Voice model missing for %s", voice_name)
            if progress:
                progress(f"Downloading voice model {voice_name} (this only happens once)...")
            _download_file(onnx_url, onnx_path)
        else:
            logger.debug("Voice model already cached for %s", voice_name)
    except (OSError, URLError) as exc:
        logger.exception("Voice file preparation failed for %s", voice_name)
        raise VoiceModelError(
            f"Could not download voice '{voice_name}': {exc}. "
            f"You can also manually place '{voice_name}.onnx' and "
            f"'{voice_name}.onnx.json' in the '{voices_dir}/' folder."
        ) from exc

    return onnx_path, json_path


class PiperEngine(VoiceEngine):
    def __init__(self, voice_name: str, voices_dir: str = VOICES_DIR, progress=None):
        try:
            from piper import PiperVoice
        except ImportError as exc:
            raise VoiceModelError(
                "The 'piper-tts' package isn't installed. Run: pip install piper-tts"
            ) from exc

        logger.info("Initializing Piper engine for voice %s", voice_name)
        logger.debug("PiperEngine using voices_dir=%s", voices_dir)
        onnx_path, json_path = ensure_voice_files(voice_name, voices_dir, progress=progress)
        logger.debug("Loading Piper voice from onnx=%s json=%s", onnx_path, json_path)
        self._voice = PiperVoice.load(onnx_path, config_path=json_path, use_cuda=False)
        self._sample_rate = getattr(self._voice.config, "sample_rate", 22050)
        logger.info("Piper engine loaded with sample rate %s", self._sample_rate)

    def synthesize(self, text: str):
        logger.debug("Synthesizing %s characters", len(text))
        pcm_bytes = self._synthesize_raw_bytes(text)
        samples = np.frombuffer(pcm_bytes, dtype=np.int16)
        return samples, self._sample_rate

    def _synthesize_raw_bytes(self, text: str) -> bytes:
        """Piper's Python API has changed shape across releases (a
        generator of raw bytes in older versions, a generator of
        AudioChunk-like objects in newer ones) - support both rather than
        pinning to one exact version."""
        voice = self._voice

        if hasattr(voice, "synthesize_stream_raw"):
            return b"".join(voice.synthesize_stream_raw(text))

        if hasattr(voice, "synthesize"):
            chunks = []
            for chunk in voice.synthesize(text):
                if isinstance(chunk, (bytes, bytearray)):
                    chunks.append(bytes(chunk))
                elif hasattr(chunk, "audio_int16_bytes"):
                    chunks.append(chunk.audio_int16_bytes)
                else:
                    raise VoiceModelError(
                        f"Unrecognized audio chunk type from piper: {type(chunk)!r}"
                    )
            return b"".join(chunks)

        raise VoiceModelError(
            "Installed piper-tts version exposes neither synthesize_stream_raw() "
            "nor synthesize() - try `pip install -U piper-tts`."
        )
