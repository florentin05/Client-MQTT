import socket
import time


import connect

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 1883))

m1=connect.MesajConnect()
m1.pack()
print(m1.message)
m1.TransmitereMesaj(s)
#data = bytes.fromhex('101200044D5154540500000005110000000A0000') mesaj de tip connect
#s.send(data)
data = s.recv(1024)
#data = bytes.fromhex('3009000154020101545454') mesaj de tip subscribe
#s.send(data)
# Asteapta date
print('Am receptionat: ', data)
# Asteapta o secunda
time.sleep(1)
# Inchide conexiune

#data=bytes.fromhex('820700010000015400') mesaj de tip publish
#s.send(data)
#while(1):
 #   data = s.recv(1024)
  #  print('Am receptionat: ', data)

s.close()