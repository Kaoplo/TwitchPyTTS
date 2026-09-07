"""Pure logic for deciding what a chat message that starts with the command
prefix should do. No Qt / networking here on purpose: this is the part of
the "moderator can interrupt the TTS" feature that's cheap to unit test.
"""
from __future__ import annotations

from enum import Enum, auto

from src.app_config import AppConfig
from src.core.chat_message import ChatMessage


class CommandOutcome(Enum):
    NOT_A_COMMAND = auto()      # regular chat message, should be spoken
    SKIP_REQUESTED = auto()     # a permitted user asked to skip the TTS
    SKIP_DENIED = auto()        # the skip command was used without permission
    UNKNOWN_COMMAND = auto()    # some other "!command", just ignore it


def evaluate_command(message: ChatMessage, config: AppConfig) -> CommandOutcome:
    text = message.text.strip()
    if not text.startswith(config.command_prefix):
        return CommandOutcome.NOT_A_COMMAND

    body = text[len(config.command_prefix):].strip()
    command_name = body.split(maxsplit=1)[0].lower() if body else ""
    skip_name = config.skip_command.lstrip(config.command_prefix).lower()

    if command_name == skip_name:
        if config.mod_only_skip and not message.is_privileged:
            return CommandOutcome.SKIP_DENIED
        return CommandOutcome.SKIP_REQUESTED

    return CommandOutcome.UNKNOWN_COMMAND
