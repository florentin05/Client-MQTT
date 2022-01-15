import sys
import threading
import time
import windows
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import ComunicareBroker
import client

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
