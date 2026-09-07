"""Single place that knows how the app's config.json is shaped.

Replaces the ad-hoc ``json.load(open('config.json'))`` calls that used to be
scattered across TTS.py / configWindow.py. Every other module talks to an
``AppConfig`` instance instead of touching the file directly.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict, field
from typing import List

CONFIG_PATH = "config.json"

DEFAULT_SKIP_COMMAND = "skip"
DEFAULT_VOICE_MODEL = "en_US-lessac-medium"


@dataclass
class AppConfig:
    channel: str = ""
    pronunciation: str = "{username} says {message}"
    ignore_list: List[str] = field(default_factory=list)

    # Chat-command settings (feature: moderator can interrupt the TTS)
    command_prefix: str = "!"
    skip_command: str = DEFAULT_SKIP_COMMAND
    mod_only_skip: bool = True

    # Voice model settings
    voice_model: str = DEFAULT_VOICE_MODEL
    speech_volume: float = 1.0

    @classmethod
    def load(cls, path: str = CONFIG_PATH) -> "AppConfig":
        if not os.path.isfile(path):
            cfg = cls()
            cfg.save(path)
            return cfg

        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        return cls._from_raw(raw)

    @classmethod
    def _from_raw(cls, raw: dict) -> "AppConfig":
        """Accepts both the new schema and the legacy
        ``{"Channel", "pronunciation", "ignorelist"}`` schema used by the
        original app, so upgrading doesn't wipe out a user's config."""
        cfg = cls()

        cfg.channel = raw.get("channel", raw.get("Channel", cfg.channel))
        cfg.pronunciation = raw.get("pronunciation", cfg.pronunciation)

        ignore_raw = raw.get("ignore_list")
        if ignore_raw is None:
            legacy = raw.get("ignorelist", "")
            ignore_raw = [name.strip() for name in legacy.split(",") if name.strip()]
        cfg.ignore_list = list(ignore_raw)

        cfg.command_prefix = raw.get("command_prefix", cfg.command_prefix)
        cfg.skip_command = raw.get("skip_command", cfg.skip_command)
        cfg.mod_only_skip = raw.get("mod_only_skip", cfg.mod_only_skip)

        cfg.voice_model = raw.get("voice_model", cfg.voice_model)
        cfg.speech_volume = raw.get("speech_volume", cfg.speech_volume)

        return cfg

    def save(self, path: str = CONFIG_PATH) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=4)

    def format_message(self, message: str, username: str) -> str:
        return self.pronunciation.replace("{username}", username).replace(
            "{message}", message
        )

    def is_ignored(self, username: str) -> bool:
        return username.lower() in (name.lower() for name in self.ignore_list)
