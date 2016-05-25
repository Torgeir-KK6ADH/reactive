#!/usr/bin/python
import socket
s = socket.socket()
host = socket.gethostname()
print host
port = 5750

s.connect((host, port))
print s.recv(1024)
s.close()
