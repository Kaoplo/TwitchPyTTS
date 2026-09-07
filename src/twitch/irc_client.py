"""Anonymous Twitch chat client.

Twitch's IRC gateway lets you connect read-only with a throwaway
``justinfan<random digits>`` nick and no OAuth token / registered
application at all - that's the whole "anonymous login" feature. This
module finishes that off properly:

* requests the ``tags`` and ``commands`` IRCv3 capabilities, which is what
  lets us see a chatter's badges (needed for the mod-only skip command) and
  a stable per-message id (needed for highlighting "the message currently
  being read" in the UI);
* buffers partial TCP reads instead of assuming one ``recv()`` == one IRC
  line (the old code silently dropped every message after the first one in
  a busy chat - see irc_parse.split_lines / its tests);
* answers PING with PONG so Twitch doesn't drop the connection;
* reconnects with backoff on network errors instead of dying silently;
* shuts down promptly by using a socket timeout instead of blocking
  forever in recv().

Runs as a QObject moved to its own QThread (started from the GUI layer),
communicating back via signals only - it never touches the UI directly.
"""

from __future__ import annotations

import logging
import random
import socket
import time

from PySide6.QtCore import QObject, Signal, Slot

from src.core.chat_message import ChatMessage
from src.twitch import irc_parse

SERVER = "irc.chat.twitch.tv"
PORT = 6667
SOCKET_TIMEOUT_SECONDS = 15.0
RECONNECT_BACKOFF_SECONDS = (1, 2, 5, 10, 30)

logger = logging.getLogger(__name__)


class IrcClient(QObject):
    message_received = Signal(ChatMessage)
    status_changed = Signal(str)
    connection_error = Signal(str)
    stopped = Signal()

    def __init__(self):
        super().__init__()
        self._sock: socket.socket | None = None
        self._running = False
        self._channel = ""
        logger.debug("IrcClient created")

    @Slot(str)
    def start(self, channel: str):
        self._channel = channel.lstrip("#").lower()
        self._running = True
        logger.info("IRC client starting for #%s", self._channel)
        attempt = 0
        while self._running:
            try:
                logger.debug("Connecting attempt %s to #%s", attempt + 1, self._channel)
                self._connect_and_listen()
                attempt = 0  # clean disconnect (we were asked to stop) - reset backoff
            except OSError as exc:
                if not self._running:
                    break
                logger.warning("IRC connection error: %s", exc)
                self.connection_error.emit(str(exc))
                delay = RECONNECT_BACKOFF_SECONDS[
                    min(attempt, len(RECONNECT_BACKOFF_SECONDS) - 1)
                ]
                self.status_changed.emit(
                    f"Connection lost ({exc}). Reconnecting in {delay}s..."
                )
                attempt += 1
                self._sleep_while_running(delay)
        self.status_changed.emit("Disconnected")
        logger.info("IRC client stopped")
        self.stopped.emit()

    @Slot()
    def stop(self):
        logger.info("IRC client stopping")
        self._running = False
        sock = self._sock
        if sock is not None:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                sock.close()
            except OSError:
                pass

    def _sleep_while_running(self, seconds: float):
        logger.debug("Sleeping for %.1fs before reconnect", seconds)
        end = time.monotonic() + seconds
        while self._running and time.monotonic() < end:
            time.sleep(0.1)

    def _connect_and_listen(self):
        self.status_changed.emit(f"Connecting to #{self._channel}...")
        nickname = irc_parse.make_anonymous_nick(random.randint(100_000, 999_999))
        logger.info("Connecting to Twitch IRC as %s", nickname)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(SOCKET_TIMEOUT_SECONDS)
        self._sock = sock
        sock.connect((SERVER, PORT))
        logger.debug("Connected TCP socket to %s:%s", SERVER, PORT)

        self._send(sock, "PASS SCHMOOPIIE")
        self._send(sock, "CAP REQ :twitch.tv/tags twitch.tv/commands")
        self._send(sock, f"NICK {nickname}")
        self._send(sock, f"JOIN #{self._channel}")

        self.status_changed.emit(f"Connected to #{self._channel}")
        logger.info("Joined channel #%s", self._channel)
        self.status_changed.emit(f"Waiting for chat in #{self._channel}...")

        buffer = ""
        last_data_at = time.monotonic()
        while self._running:
            try:
                chunk = sock.recv(4096)
            except socket.timeout:
                if time.monotonic() - last_data_at > 6 * 60:
                    raise OSError("no data from Twitch for 6 minutes")
                logger.debug("IRC idle; waiting for more data")
                continue

            if not chunk:
                raise OSError("connection closed by server")

            last_data_at = time.monotonic()
            logger.debug("Received %s bytes from Twitch IRC", len(chunk))
            buffer += chunk.decode("utf-8", errors="ignore")
            lines, buffer = irc_parse.split_lines(buffer)
            logger.debug(
                "Parsed %s complete IRC lines; %s bytes buffered",
                len(lines),
                len(buffer),
            )
            for raw_line in lines:
                self._handle_line(sock, raw_line)

    def _handle_line(self, sock: socket.socket, raw_line: str):
        line = irc_parse.parse_line(raw_line)
        if line is None:
            logger.debug("Ignoring unparsable IRC line: %r", raw_line)
            return

        logger.debug(
            "IRC parsed line command=%s user=%s params=%s trailing=%r",
            line.command,
            line.username,
            line.params,
            line.trailing,
        )

        if line.command == "PING":
            logger.debug("Responding to IRC PING")
            self._send(sock, f"PONG :{line.trailing or 'tmi.twitch.tv'}")
            return

        if line.command == "PRIVMSG" and line.username and line.trailing is not None:
            is_mod, is_broadcaster = irc_parse.badges_from_tags(line.tags)
            msg_id = line.tags.get("id")
            kwargs = dict(
                username=line.username,
                text=line.trailing,
                is_mod=is_mod,
                is_broadcaster=is_broadcaster,
            )
            # Only pass id= when Twitch actually gave us one (tags capability
            # granted) - otherwise let ChatMessage's default_factory mint a
            # local id, since passing id="" would defeat that default.
            message = (
                ChatMessage(id=msg_id, **kwargs) if msg_id else ChatMessage(**kwargs)
            )
            logger.info("Received chat message from %s", line.username)
            self.message_received.emit(message)
        else:
            logger.debug("Ignoring non-chat IRC line command=%s", line.command)

    @staticmethod
    def _send(sock: socket.socket, line: str):
        logger.debug("IRC send: %s", line)
        sock.send(f"{line}\r\n".encode("utf-8"))
