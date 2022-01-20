import struct
import time
from abc import ABC, abstractmethod
import random

puback = 0
pubrel = 0
pubrec = 0
pubcomp = 0
PacketIdentifier = 0


class Packet(ABC):
    @abstractmethod
    def pack(self):
        pass


class Connect(Packet):
    def __init__(self, id, usernameFlag, username, passwordFlag, password, keepAlive, lastWillFlag, lastWillMessage,
                 lastWillQOS, lastWillTopic, CleanStart):
        self.MessageType = 0x10
        self.ProtocolNameLength = 0x0004
        self.ProtocolName = 0x4D515454
        self.ProtocolVersion = 0x05
        self.ConnectFlags = (
                                        usernameFlag << 7 | passwordFlag << 6 | 0 | lastWillQOS << 3 | lastWillFlag << 2 | CleanStart << 1) & 0xfe
        self.PropertyLength = 0x00
        self.WillPropertyLength = 0x00
        self.id = id
        self.username = username
        self.password = password
        self.keepAlive = keepAlive
        self.lastWillPayload = lastWillMessage
        self.lastWillTopic = lastWillTopic
        self.lastWillFlag = lastWillFlag
        self.usernameFlag = usernameFlag
        self.passwordFlag = passwordFlag

    def pack(self):
        VariableHeader = self.ProtocolNameLength.to_bytes(2, byteorder='big')
        VariableHeader += self.ProtocolName.to_bytes(4, byteorder='big')
        VariableHeader += self.ProtocolVersion.to_bytes(1, byteorder='big')
        VariableHeader += self.ConnectFlags.to_bytes(1, byteorder='big')
        VariableHeader += self.keepAlive.to_bytes(2, byteorder='big')
        VariableHeader += self.PropertyLength.to_bytes(1, byteorder='big')
        Payload = len(self.id).to_bytes(2, byteorder='big')
        Payload += self.id.encode('UTF-8')  # self.id.to_bytes(len(self.id),byteorder='big')
        if self.lastWillFlag == 1:
            Payload += self.WillPropertyLength.to_bytes(1, byteorder='big')
            Payload += len(self.lastWillTopic).to_bytes(2, byteorder='big')
            Payload += self.lastWillTopic.encode('utf-8')
            Payload += len(self.lastWillPayload).to_bytes(2, byteorder='big')
            Payload += self.lastWillPayload.encode('utf-8')
        if self.usernameFlag:
            Payload += len(self.username).to_bytes(2, byteorder='big')
            Payload += self.username.encode('UTF-8')  # self.username.to_bytes(len(self.username), byteorder='big')
        if self.passwordFlag:
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


class Subscribe(Packet):
    def __init__(self, topic, qos):
        global PacketIdentifier
        self.MessageType = 0x82
        PacketIdentifier = random.randrange(2, 1000)
        self.PropertyLength = 0x00
        self.TopicName = topic
        self.qos = qos

    def pack(self):
        global PacketIdentifier
        VariableHeader = PacketIdentifier.to_bytes(2, byteorder='big') + self.PropertyLength.to_bytes(1,
                                                                                                      byteorder='big')
        Payload = len(self.TopicName).to_bytes(2, byteorder='big')
        Payload += self.TopicName.encode('UTF-8')
        Payload += self.qos.to_bytes(1, byteorder='big')

        FixedHeader = self.MessageType.to_bytes(1, byteorder='big')
        FixedHeader += len(VariableHeader + Payload).to_bytes(1, byteorder='big')

        message = FixedHeader + VariableHeader + Payload
        return message


class Unsubscribe(Packet):
    def __init__(self, topic):
        global PacketIdentifier
        self.MessageType = 0xa2
        PacketIdentifier = random.randrange(2, 1000)
        self.PropertyLength = 0x00
        self.TopicName = topic

    def pack(self):
        global PacketIdentifier
        VariableHeader = PacketIdentifier.to_bytes(2, byteorder='big') + self.PropertyLength.to_bytes(1,
                                                                                                      byteorder='big')
        Payload = len(self.TopicName).to_bytes(2, byteorder='big')
        Payload += self.TopicName.encode('UTF-8')

        FixedHeader = self.MessageType.to_bytes(1, byteorder='big')
        FixedHeader += len(VariableHeader + Payload).to_bytes(1, byteorder='big')

        message = FixedHeader + VariableHeader + Payload
        return message


class Disconnect(Packet):
    def __init__(self):
        self.MessageType = 0xE0
        self.DisconnectReason = 0x00
        self.PropertyLength = 0x00

    def pack(self):
        return self.MessageType.to_bytes(1, byteorder='big') + 0x02.to_bytes(1,
                                                                             byteorder='big') + self.DisconnectReason.to_bytes(
            1, byteorder='big') + self.PropertyLength.to_bytes(1, byteorder='big')


class Publish(Packet):
    def __init__(self, DUPflag, QoSlevel, Retain, TopicName, Information, PacketIdentifier):
        self.MessageType = 0x3 << 4 | DUPflag << 3 | QoSlevel << 1 | Retain
        self.PacketIdentifier = PacketIdentifier
        self.PropertyLength = 0x00
        self.TopicName = TopicName
        self.Information = Information

    def pack(self):
        VariableHeader = len(self.TopicName).to_bytes(2, byteorder='big')
        VariableHeader += self.TopicName.encode('UTF-8')
        if self.MessageType & 0x01 << 1 or self.MessageType & 0x02 << 1:
            VariableHeader += self.PacketIdentifier.to_bytes(2, byteorder='big')
        VariableHeader += self.PropertyLength.to_bytes(1, byteorder='big')
        Payload = len(self.Information).to_bytes(2, byteorder='big')
        Payload += self.Information.encode('UTF-8')
        message = self.MessageType.to_bytes(1, byteorder='big')
        message += len(VariableHeader + Payload).to_bytes(1, byteorder='big')
        message += VariableHeader
        message += Payload
        return message


class Pubrel(Packet):
    def __init__(self, ReasonCode, PacketIdentifier):
        self.MessageType = 0x62
        self.RemainingLength = 0x02
        self.PacketIdentifier = PacketIdentifier
        self.ReasonCode = ReasonCode

    def pack(self):
        if self.ReasonCode == 0:
            message = self.MessageType.to_bytes(1, byteorder="big")
            message += self.RemainingLength.to_bytes(1, byteorder="big")
            message += self.PacketIdentifier.to_bytes(2, byteorder="big")
        else:
            message = self.MessageType.to_bytes(1, byteorder="big")
            self.RemainingLength = 0x03
            message += self.RemainingLength.to_bytes(1, byteorder="big")
            message += self.PacketIdentifier.to_bytes(2, byteorder="big")
            message += self.ReasonCode.to_bytes(1, byteorder="big")
        return message


class PUBREC(Packet):
    def __init__(self, ReasonCode, PacketIdentifier):
        self.MessageType = 0x50
        self.RemainingLength = 0x03
        self.PacketIdentifier = PacketIdentifier
        self.ReasonCode = ReasonCode

    def pack(self):
        message = self.MessageType.to_bytes(1, byteorder="big")
        self.RemainingLength = 0x03
        message += self.RemainingLength.to_bytes(1, byteorder="big")
        message += self.PacketIdentifier.to_bytes(2, byteorder="big")
        message += self.ReasonCode.to_bytes(1, byteorder="big")
        return message


class PUBCOMP(Packet):
    def __init__(self, PacketIdentifier):
        self.MessageType = 0x70
        self.RemainingLength = 0x03
        self.PacketIdentifier = PacketIdentifier
        self.ReasonCode = 0x00

    def pack(self):
        message = self.MessageType.to_bytes(1, byteorder="big")
        self.RemainingLength = 0x03
        message += self.RemainingLength.to_bytes(1, byteorder="big")
        message += self.PacketIdentifier.to_bytes(2, byteorder="big")
        message += self.ReasonCode.to_bytes(1, byteorder="big")
        return message


class PUBACK(Packet):
    def __init__(self, PacketIdentifier):
        self.MessageType = 0x40
        self.RemainingLength = 0x03
        self.PacketIdentifier = PacketIdentifier
        self.ReasonCode = 0x00

    def pack(self):
        message = self.MessageType.to_bytes(1, byteorder="big")
        self.RemainingLength = 0x03
        message += self.RemainingLength.to_bytes(1, byteorder="big")
        message += self.PacketIdentifier.to_bytes(2, byteorder="big")
        message += self.ReasonCode.to_bytes(1, byteorder="big")
        return message


def CONNACKparse(Client, packet):
    if packet[3] == 0x00:  ## inseamna ca reason code-ul e pt succes
        Client.Connected = 1
        # success_window = windows.SuccessWindow()
        # success_window.show()
        # # QtCore.QTimer.singleShot(5000, success_window.close)
        print("Utilizator conectat")
        if packet[4] > 6:  # inseamna ca clientul nu a specificat un id si il iau din mesaj
            Client.clientid = packet[11:11 + packet[10]].decode('utf-8')
            print(Client.clientid)
    else:  # vom trimite un pachet de disconenct deoarece apare o eroare
        Client.Connected = 0


def PUBACKparse(Client, packet):
    global puback
    if struct.unpack('>h', packet[2:4])[0] == Client.PacketIdentifier:
        puback = 1


def SUBACKparse(Client, packet):
    global PacketIdentifier
    if struct.unpack('>h', packet[2:4])[0] == PacketIdentifier:
        # adaug in lista de topicuri , topicul la care tocmai m am abonat
        if (Client.Topics != ""):
            Client.Topics.append(Client.CurrentTopic)
            Client.window.mainWindow.MessageWindow.unsubscribe_combobox.addItem(Client.CurrentTopic)


def UNSUBACKparse(Client, packet):
    global PacketIdentifier
    if struct.unpack('>h', packet[2:4])[0] == PacketIdentifier:
        Client.window.mainWindow.MessageWindow.unsubscribe_combobox.removeItem(
            Client.window.mainWindow.MessageWindow.unsubscribe_combobox.currentIndex())


def PUBLISHparse(Client, packet):
    global pubrel
    # print('message length: ', packet[1])
    topic_length = struct.unpack('>h', packet[2:4])[0]
    # print('topic length:', topic_length)
    # print('topic name:' + packet[4:4 + topic_length].decode('utf-8'))
    text = "\n <br><b>Topic name:</b> " + packet[4:4 + topic_length].decode('utf-8') + "\n"
    if not ((packet[0] & (0x01 << 1)) or (packet[0] & (0x02 << 1))):
        message_length = packet[1] - 3 - topic_length
        message = packet[4 + topic_length:5 + topic_length + message_length].decode('utf-8')
        print('message:' + message)
        text += "\n" + "<br> <b>Message:</b>" + message
        Client.window.mainWindow.MessageWindow.messages.append(text)
    else:
        packet_identifier = struct.unpack('>h', packet[4 + topic_length:4 + topic_length + 2])[0]
        print('packet identifier:', packet_identifier)
        message_length = packet[1] - 3 - topic_length
        message = packet[5 + topic_length:5 + topic_length + message_length].decode('utf-8')
        print('message:' + message)
        text += "\n" + "<br><b>Message:</b>" + message
    print(text)
    if packet[0] & (0x01 << 1):
        Client.socket.send(PUBACK(packet_identifier).pack())
        print("Am primit mesajul cu qos1:" + text)
        Client.window.mainWindow.MessageWindow.messages.append(text)
    elif packet[0] & (0x02 << 1):
        Client.socket.send(PUBREC(0x00, packet_identifier).pack())
        time.sleep(1)
        # while pubrel==0 :
        #     pass
        # pubrel=0
        Client.socket.send(PUBCOMP(packet_identifier).pack())
        time.sleep(1)
        Client.window.mainWindow.MessageWindow.messages.append(text)
        print("Am primit mesajul cu qos2:" + text)


def PUBRECparse(Client, packet):
    global pubrec
    if struct.unpack('>h', packet[2:4])[0] == Client.PacketIdentifier:  # and (packet[4]==0x00 or packet[4]==0x10):
        pubrec = 1


def PUBCOMPparse(Client, packet):
    global pubcomp
    if struct.unpack('>h', packet[2:4])[0] == Client.PacketIdentifier:  # and packet[0]==0x00:
        pubcomp = 1


def PUBRELparse(Client, packet):
    global pubrel
    if packet[0] == 0x62:  # and packet[0]==0x00:
        pubrel = 1


def PUBLISHButton(Client, TopicName, Payload, DUP, QOS, Retain):
    global puback, pubrel, pubcomp, pubrec
    Client.PacketIdentifier = random.randrange(2, 10000)
    message = Publish(DUP, QOS, Retain, TopicName, Payload, Client.PacketIdentifier)
    Client.socket.send(message.pack())
    if QOS == 0:
        print("Mesajul a fost transmis!")
    elif QOS == 1:
        while puback != 1:
            time.sleep(1)
        print("Am primit puback")
        puback = 0
    elif QOS == 2:
        while pubrec != 1:
            time.sleep(1)
        print("Am primit pubrec")
        pubrec = 0
        Client.socket.send(Pubrel(0, Client.PacketIdentifier).pack())
        while pubcomp != 1:
            time.sleep(1)
        print("Mesajul cu qos 2 a fost trimis!")
        pubcomp = 0
