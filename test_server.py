import socketserver
import socket
clients = []
client_num=1
s = socket.socket()
host = 'localhost' 
port = 9995
s.bind((host, port))
for i in range(client_num):
    s.listen(1)
    clients.append(s.accept())
for conn,addr in clients:
    print(addr)