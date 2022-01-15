import time

import client


def ComunicareBroker(socket):
    while 1:
        data = socket.recv(1024)
        if not data:
            break
        print('am receptionat: ', data)
