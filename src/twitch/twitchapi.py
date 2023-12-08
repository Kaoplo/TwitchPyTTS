import socket
import random
import re
import threading
import asyncio

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

    def notify_event(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)

    def parse_message(self, message):
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

    def connect(self, channel):
        self.isRunning = True
        threading.Thread(target=self._open_socket, args=(channel,)).start()

    def _open_socket(self, channel):
        self.sock.connect((server, port))
        self.sock.send(f"NICK {nickname}\n".encode('utf-8'))
        self.sock.send(f"JOIN #{channel}\n".encode('utf-8'))
        if "Welcome" not in self.sock.recv(2048).decode('utf-8'):
            raise RuntimeError("Failed to connect to Twitch IRC")
        while self.isRunning:
            resp = self.sock.recv(2048).decode('utf-8')
            if resp.startswith('PING'):
                self.sock.send("PONG\n".encode('utf-8'))
            elif nickname in resp:
                pass
            elif len(resp) > 0:
                self.notify_event(self.parse_message(resp))

    def close(self):
        self.sock.close()
        self.isRunning = False


def on_message(message):
    print(f'{message["username"]} said: {message["message"]}')


async def run():
    ttv = Twitch()
    channel = 'kaoplo'

    ttv.connect(channel)

    ttv.register_event(on_message)

    try:
        input("press enter to stop\n")
    finally:
        ttv.close()

asyncio.run(run())
