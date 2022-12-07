import socket


class Player:
    def __init__(self, username):
        self.socketName = socket.gethostname()
        self.username = username
