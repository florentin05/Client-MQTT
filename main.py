import sys
import threading
import time
import connectInterface
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import ComunicareBroker
import client

app = QtWidgets.QApplication(sys.argv)
connect_form = connectInterface.ConnectForm()
print(connect_form.username_value)
connect_form.show()
sys.exit(app.exec_())
# Client=client.Client()
# threading.Thread(target=ComunicareBroker.ComunicareBroker,args=(Client.socket,)).start()
# Client.socket.send(bytes.fromhex('101400044d51545405c000c000000154000155000155'))
