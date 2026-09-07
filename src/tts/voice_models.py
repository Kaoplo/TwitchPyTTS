"""Knows how Piper voice names map to files on disk and on Hugging Face.

Piper voices are named ``<lang>_<REGION>-<voice>-<quality>``, e.g.
``en_US-lessac-medium``. Each voice is a small (order of tens of MB) ONNX
model plus a JSON config - this is the "small AI voice model" the app reads
chat with, running fully offline once downloaded.
"""
from __future__ import annotations

import os

HF_BASE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main"


def voice_file_names(voice_name: str) -> tuple[str, str]:
    return f"{voice_name}.onnx", f"{voice_name}.onnx.json"


def voice_paths(voice_name: str, voices_dir: str) -> tuple[str, str]:
    onnx_name, json_name = voice_file_names(voice_name)
    return os.path.join(voices_dir, onnx_name), os.path.join(voices_dir, json_name)


def voice_download_urls(voice_name: str) -> tuple[str, str]:
    """Build the Hugging Face download URLs for a Piper voice name.

    ``en_US-lessac-medium`` -> .../en/en_US/lessac/medium/en_US-lessac-medium.onnx
    """
    lang_region, voice, quality = voice_name.split("-")
    lang = lang_region.split("_")[0]
    onnx_name, json_name = voice_file_names(voice_name)
    dir_path = f"{lang}/{lang_region}/{voice}/{quality}"
    return f"{HF_BASE_URL}/{dir_path}/{onnx_name}", f"{HF_BASE_URL}/{dir_path}/{json_name}"
