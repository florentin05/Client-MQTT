import datetime
import socket
import time

import Packets




class Client():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1', 1883))
        self.KeepAlive=0
        self.Connected=0
        self.clientid=0
        self.LastMessageSent=datetime.datetime.now()

    def MonitorizareKeepAlive(self):
        while self.Connected:
            if ((datetime.datetime.now() - self.LastMessageSent).seconds >= self.KeepAlive):
                self.socket.send(Packets.PINGREQ().pack())
                self.LastMessageSent = datetime.datetime.now()

    def VerificareDisconnect(self):
        time.sleep(30)
        self.socket.send(Packets.Disconnect().pack())
        self.Connected=0

    def TransmitereMesaj(self):
        while self.Connected:
            # self.socket.send(Packets.Publish('rc','LaboratorRC').pack())
            Packets.PUBLISHButton(self,'rc','Mesaj cu qos=2',0,0,0)
            time.sleep(30)


