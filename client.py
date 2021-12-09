import datetime
import socket

import Packets


class Client():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1', 1883))
        self.KeepAlive=0
        self.Connected=0
        self.LastMessageSent=datetime.datetime.now()

