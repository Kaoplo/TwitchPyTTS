import socket
import random
import re
import threading

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'justinfan' + str(random.randint(100000, 999999))


class Twitch:
    def __init__(self):
        self.sock = socket.socket()
        self.handlers = []
        self.isRunning = False

    def register_event(self, handler):
        self.handlers.append(handler)

    def connect(self, channel):
        self.isRunning = True
        threading.Thread(target=self._open_socket, args=(channel,)).start()

    def close(self):
        self.isRunning = False
        self.sock.send("QUIT\n".encode('utf-8'))

    def _notify_event(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)

    def _parse_message(self, message):
        irc_message_pattern = re.compile(r'^(?::([^ ]+) )?([^ ]+)(?: ([^:]+) :(.+))?')
        match = irc_message_pattern.match(message)
        if match:
            prefix, command, params, trailing = match.groups()
            return {
                'username': prefix.split('!')[0] if prefix else None,
                'message': trailing
            }
        else:
            return None

    def _open_socket(self, channel):
        self.sock.connect((server, port))
        self.sock.send(f"NICK {nickname}\n".encode('utf-8'))
        self.sock.send(f"JOIN #{channel}\n".encode('utf-8'))
        if "Welcome" not in self.sock.recv(2048).decode('utf-8'):
            raise RuntimeError("Failed to connect to Twitch IRC")
        try:
            while self.isRunning:
                self._receive_message(self.sock.recv(2048).decode('utf-8'))
        finally:
            self.sock.close()

    def _receive_message(self, message):
        resp = message
        if resp.startswith('PING'):
            self.sock.send("PONG\n".encode('utf-8'))
        elif nickname in resp:
            pass
        elif len(resp) > 0:
            self._notify_event(self._parse_message(resp))
