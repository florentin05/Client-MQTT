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
    message = Packets.Connect(client_id,username,password,keepalive,"Acesta este un mesaj lastWill").pack()
    Client.socket.send(message)
    time.sleep(1)
    while Client.Connected:
        TopicName=input('Topic abonare:')
        SubscribeQOS=int(input('QoS:'))
        Client.socket.send(Packets.Subscribe(TopicName,SubscribeQOS).pack())









