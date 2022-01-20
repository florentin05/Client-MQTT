import sys
import threading
import time
import windows
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import ComunicareBroker
import client

if __name__ == '__main__':
    Client = client.Client()
    threading.Thread(target=ComunicareBroker.ComunicareBroker, args=(Client,)).start()
    threading.Thread(target=Client.MonitorizareKeepAlive).start()
    threading.Thread(target=Client.MonitorizareResurse).start()
    app = QApplication(sys.argv)
    startWindow = windows.ConnectWindow(Client)
    Client.window = startWindow
    startWindow.show()
    app.exec()
