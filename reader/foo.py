#!/usr/bin/python

import subprocess
from time import sleep

p = subprocess.Popen(['python', 'server.py'])
sleep(1)
print p.pid
subprocess.Popen(['kill', str(p.pid)])
print "Killin' it"
