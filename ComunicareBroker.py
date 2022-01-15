import time


import client
def ComunicareBroker(Client):
    while not Client.Connected :
        data=Client.socket.recv(1024)
        if not data:
            print('renuntam')
            break
        if(data[0]==0x20 and data[3]==0x00): #daca este pachet de tip CONNACK iar reason code e 0 inseamna ca a fost acceptata conexiunea
            print("Utilizator conectat!")
            Client.Connected=1
    while Client.Connected:
        data = Client.socket.recv(1024)
        if not data:
            print('renuntam')
            break


