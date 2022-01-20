import datetime
import socket
import time

import Packets
import psutil


class Client():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1', 1883))
        self.KeepAlive = 0
        self.Connected = 0
        self.lastWillFlag = 0
        self.lastWillMessage = ""
        self.lastWillQOS = 0
        self.CleanStart = 0
        self.id = ""
        self.LastMessageSent = datetime.datetime.now()
        self.username = ""
        self.password = ""
        self.Topics = []
        self.lastWillTopic = ""
        self.PacketIdentifier = 0
        self.CurrentTopic = ""
        self.window = 0

    def MonitorizareKeepAlive(self):
        while not self.Connected:
            time.sleep(1)
        while self.Connected:
            if (datetime.datetime.now() - self.LastMessageSent).seconds >= 1.5 * self.KeepAlive:
                self.socket.send(Packets.PINGREQ().pack())
                self.LastMessageSent = datetime.datetime.now()

    def VerificareDisconnect(self):
        time.sleep(30)
        self.socket.send(Packets.Disconnect().pack())
        self.Connected = 0

    def TransmitereMesaj(self):
        while self.Connected:
            # self.socket.send(Packets.Publish('rc','LaboratorRC').pack())
            Packets.PUBLISHButton(self, 'rc', 'Mesaj cu qos=2', 0, 1, 0)
            time.sleep(30)

    def MonitorizareResurse(self):
        while self.Connected == 0:
            time.sleep(1)
        while self.Connected:
            CPUFreq = psutil.cpu_freq()
            CPUusage = psutil.cpu_percent()
            Memory = psutil.virtual_memory()[2]
            message = "CPU Frequency:%s <br> CPUusage=%s <br> Memory used=%s" % (CPUFreq, CPUusage, Memory)
            time.sleep(30)
            self.socket.send(Packets.Publish(0, 1, 0, "OS", message, 100).pack())
