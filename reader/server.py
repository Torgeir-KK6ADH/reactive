#!/usr/bin/python

import socket

s=socket.socket()
host = socket.gethostname()
print host
port = 5750
s.bind((host, port))

s.listen(5)
while True:
  c, addr = s.accept()
  print 'Received connection from', addr
  c.send('Thanks you for connecting')
  c.close()
