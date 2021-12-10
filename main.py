import sys
import threading
import time
import connectInterface
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import ComunicareBroker
import ComunicareInterfata
import Packets
import client

Client = client.Client()
threading.Thread(target=ComunicareBroker.ComunicareBroker, args=(Client,)).start()
threading.Thread(target=ComunicareInterfata.ComunicareInterfata, args=(Client,)).start()


while not Client.Connected:
    pass

threading.Thread(target=Client.MonitorizareKeepAlive).start()
threading.Thread(target=Client.TransmitereMesaj).start()
Client.VerificareDisconnect()


# app = QtWidgets.QApplication(sys.argv)
# connect_form = connectInterface.ConnectForm()
# print(connect_form.username_value)
# print(connect_form.password_value)
# connect_form.show()
# sys.exit(app.exec_())






