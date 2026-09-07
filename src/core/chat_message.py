"""Domain model for a single chat message flowing through the app.

Kept dependency-free (no Qt, no networking) so it can be constructed and
compared from any layer (twitch parsing, tts queue, gui) and unit tested
in isolation.
"""
from __future__ import annotations

import itertools
import time
from dataclasses import dataclass, field

_id_counter = itertools.count(1)


def _next_local_id() -> str:
    """Fallback id used when Twitch doesn't hand us a message id (e.g. the
    IRCv3 ``tags`` capability wasn't granted)."""
    return f"local-{next(_id_counter)}"


@dataclass
class ChatMessage:
    username: str
    text: str
    id: str = field(default_factory=_next_local_id)
    is_mod: bool = False
    is_broadcaster: bool = False
    timestamp: float = field(default_factory=time.time)

    @property
    def is_privileged(self) -> bool:
        """True for anyone Twitch marks as broadcaster or moderator."""
        return self.is_mod or self.is_broadcaster

    @property
    def is_command(self) -> bool:
        return self.text.strip().startswith(("!", "/"))

    def display(self) -> str:
        return f"{self.username}: {self.text}"
