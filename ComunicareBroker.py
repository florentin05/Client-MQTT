import Packets
import datetime


def ComunicareBroker(Client):
    while not Client.Connected:
        data = Client.socket.recv(1024)
        if not data:
            print('renuntam')
            break
        if data[0] == 0x20:
            Packets.CONNACKparse(Client, data)
            Client.LastMessageSent = datetime.datetime.now()
    while Client.Connected:
        data = Client.socket.recv(1024)
        if not data:
            print('Disconnected')
            Client.Connected = 0
            break
        Client.LastMessageSent = datetime.datetime.now()
        if data[0] == 0x30 or data[0] == 0x32 or data[0] == 0x34:
            Packets.PUBLISHparse(Client, data)
        elif data[0] == 0x40:
            Packets.PUBACKparse(Client, data)
        elif data[0] == 0x50:
            Packets.PUBRECparse(Client, data)
        elif data[0] == 0x70:
            Packets.PUBCOMPparse(Client, data)
        elif data[0] == 0x62:
            Packets.PUBRELparse(Client, data)
        elif data[0] == 0x90:
            Packets.SUBACKparse(Client, data)
        elif data[0] == 0xb0:
            Packets.UNSUBACKparse(Client, data)
