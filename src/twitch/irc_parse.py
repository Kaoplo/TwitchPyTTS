"""Parsing helpers for raw Twitch IRC lines.

Kept free of sockets/threads so the (fiddly, easy to get subtly wrong) parts
of IRC parsing can be unit tested directly. ``irc_client.py`` is the thin
networking layer that feeds real socket data through these functions.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class IrcLine:
    tags: dict[str, str]
    prefix: str | None
    command: str
    params: list
    trailing: str | None

    @property
    def username(self) -> str | None:
        if not self.prefix:
            return None
        return self.prefix.split("!")[0]


def split_lines(buffer: str):
    """Split a raw socket-recv buffer into complete IRC lines.

    Twitch terminates every IRC line with ``\\r\\n``, but TCP gives no
    guarantee a single ``recv()`` lines up with message boundaries - a chunk
    can contain several lines, or half of one. Returns
    ``(complete_lines, remainder)`` where ``remainder`` should be prepended
    to the next chunk read from the socket.
    """
    parts = buffer.split("\r\n")
    remainder = (
        parts.pop()
    )  # last element is "" if buffer ended cleanly, else a partial line
    return parts, remainder


def parse_line(raw: str) -> IrcLine | None:
    """Parse a single (already newline-stripped) IRC line, tags included."""
    if not raw:
        return None

    rest = raw
    tags: dict[str, str] = {}
    if rest.startswith("@"):
        tag_part, _, rest = rest.partition(" ")
        for pair in tag_part[1:].split(";"):
            if not pair:
                continue
            key, _, value = pair.partition("=")
            tags[key] = value

    prefix = None
    if rest.startswith(":"):
        prefix, _, rest = rest.partition(" ")
        prefix = prefix[1:]

    if " :" in rest:
        head, _, trailing = rest.partition(" :")
    else:
        head, trailing = rest, None

    head_parts = head.split()
    if not head_parts:
        return None
    command = head_parts[0]
    params = head_parts[1:]

    return IrcLine(
        tags=tags, prefix=prefix, command=command, params=params, trailing=trailing
    )


def badges_from_tags(tags: dict[str, str]):
    """Returns (is_mod, is_broadcaster) from a PRIVMSG's IRCv3 tags."""
    badges = tags.get("badges", "")
    badge_names = {b.split("/")[0] for b in badges.split(",") if b}
    is_broadcaster = "broadcaster" in badge_names
    is_mod = "moderator" in badge_names or is_broadcaster
    return is_mod, is_broadcaster


def make_anonymous_nick(random_int: int) -> str:
    return f"justinfan{random_int}"
