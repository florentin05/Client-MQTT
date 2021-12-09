import datetime
import time

import Packets
import client


def ComunicareInterfata(Client):
    client_id=input('ClientID:')
    username=input('Username:')
    password=input('Password:')
    keepalive=int(input('keepalive:'))
    Client.KeepAlive=keepalive
    message = Packets.Connect(client_id,username,password,keepalive).pack()
    Client.socket.send(message)
    time.sleep(1)
    while Client.Connected:
        if((datetime.datetime.now()-Client.LastMessageSent).seconds>=Client.KeepAlive):
            Client.socket.send(Packets.PINGREQ().pack())
            Client.LastMessageSent=datetime.datetime.now()








