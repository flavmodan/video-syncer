import socket

HOST = 'localhost'    # The remote host
PORT = 9995              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.close()