from abc import ABC, abstractmethod
from struct import pack


class Packet(ABC):
    @abstractmethod
    def pack(self):
        pass


class Connect(Packet):
    def __init__(self, id, username, password, keepAlive):
        self.MessageType = 0x10
        self.ProtocolNameLength = 0x0004
        self.ProtocolName = 0x4D515454
        self.ProtocolVersion = 0x05
        self.ConnectFlags = 0xc0
        self.PropertyLength = 0x00
        self.id = id
        self.username = username
        self.password = password
        self.keepAlive = keepAlive

    def pack(self):
        VariableHeader = self.ProtocolNameLength.to_bytes(2, byteorder='big')
        VariableHeader += self.ProtocolName.to_bytes(4, byteorder='big')
        VariableHeader += self.ProtocolVersion.to_bytes(1, byteorder='big')
        VariableHeader += self.ConnectFlags.to_bytes(1, byteorder='big')
        VariableHeader += self.keepAlive.to_bytes(2, byteorder='big')
        VariableHeader += self.PropertyLength.to_bytes(1, byteorder='big')
        Payload = len(self.id).to_bytes(2, byteorder='big')
        Payload += self.id.encode('UTF-8')  # self.id.to_bytes(len(self.id),byteorder='big')
        Payload += len(self.username).to_bytes(2, byteorder='big')
        Payload += self.username.encode('UTF-8')  # self.username.to_bytes(len(self.username), byteorder='big')
        Payload += len(self.password).to_bytes(2, byteorder='big')
        Payload += self.password.encode('UTF-8')  # self.password.to_bytes(len(self.password), byteorder='big')
        FixedHeader = self.MessageType.to_bytes(1, byteorder='big') + len(VariableHeader + Payload).to_bytes(1,
                                                                                                             byteorder='big')

        message = FixedHeader + VariableHeader + Payload
        return message


class PINGREQ(Packet):
    def __init__(self):
        self.MessageType = 0xC0
        self.RemainingLength = 0x00

    def pack(self):
        return self.MessageType.to_bytes(1, byteorder='big') + self.RemainingLength.to_bytes(1, byteorder='big')
