import sys
import threading
import time
import windows
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
#Client.VerificareDisconnect()



# app = QtWidgets.QApplication(sys.argv)
# connect_form = connectInterface.ConnectForm()
# print(connect_form.username_value)
# print(connect_form.password_value)
# connect_form.show()
# sys.exit(app.exec_())






# app = QtWidgets.QApplication(sys.argv)
# connect_form = windows.StartWindow()
#
# connect_form.show()
# sys.exit(app.exec_())
# Client=client.Client()
# threading.Thread(target=ComunicareBroker.ComunicareBroker,args=(Client.socket,)).start()
# Client.socket.send(bytes.fromhex('101400044d51545405c000c000000154000155000155'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    startWindow = windows.ConnectWindow()
    startWindow.show()
    app.exec()
