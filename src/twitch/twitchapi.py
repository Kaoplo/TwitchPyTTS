import socket
import random
import re

class Twitch:
    def __init__(self):
        self.sock = socket.socket()
        self.handlers = []

    def register_event(self, handler):
        self.handlers.append(handler)

    def notify(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)

    def parse_message(self, message):
        irc_message_pattern = re.compile(r'^(?::([^ ]+) )?([^ ]+)(?: ([^:]+) :(.+))?')
        match = irc_message_pattern.match(message)
        if match:
            prefix, command, params, trailing = match.groups()
            return {
                'username': prefix.split('!')[0] if prefix else None,
                # 'command': command,
                # 'params': params.split() if params else [],
                'message': trailing
            }
        else:
            return None

    def connect(self, channel):
        server = 'irc.chat.twitch.tv'
        port = 6667
        nickname = 'justinfan' + str(random.randint(100000, 999999))
        self.sock.connect((server, port))
        self.sock.send(f"NICK {nickname}\n".encode('utf-8'))
        self.sock.send(f"JOIN #{channel}\n".encode('utf-8'))
        if "Welcome" not in self.sock.recv(2048).decode('utf-8'):
            raise RuntimeError("Failed to connect to Twitch IRC")
        while True:
            resp = self.sock.recv(2048).decode('utf-8')
            if resp.startswith('PING'):
                self.sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                self.notify(self.parse_message(resp))


def on_message(message):
    print(f'{message["username"]} said: {message["message"]}')

Twitch = Twitch()

channel = 'kaoplo'

Twitch.register_event(on_message)

Twitch.connect(channel)
