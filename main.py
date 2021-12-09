import threading
import time

import ComunicareBroker
import client

Client=client.Client()
threading.Thread(target=ComunicareBroker.ComunicareBroker,args=(Client.socket,)).start()
Client.socket.send(bytes.fromhex('101400044d51545405c000c000000154000155000155'))



