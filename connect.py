from struct import *


class MesajConnect:
    def __init__(self):
        self.FixedHeaderbyte1 = bytes.fromhex('10')
        self.TotalLength = bytes.fromhex('0C')
        self.ProtocolNameLength = bytes.fromhex('0004')
        self.ProtocolName = bytes.fromhex('4D515454')
        self.ProtocolVersion = bytes.fromhex('05')
        self.ConnectFlags = bytes.fromhex('00')
        self.KeepAlive = bytes.fromhex('0000')
        self.PropertyLength = bytes.fromhex('00')
        self.Payload = bytes.fromhex('00')

    def pack(self):
        self.message = pack('ss2s4sss2sss', self.FixedHeaderbyte1, self.TotalLength, self.ProtocolNameLength,
                            self.ProtocolName, self.ProtocolVersion, self.ConnectFlags, self.KeepAlive,
                            self.PropertyLength, self.Payload)

    def TransmitereMesaj(self, socket):
        socket.send(self.message)
