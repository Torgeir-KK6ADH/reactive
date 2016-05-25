#!/usr/bin/python -u
import reactive_f
import sys
from subprocess import call

################################################################################
media = [
    "../media/jim_ski.mp4",
    "../media/shoe_alice.mp4",
    "../media/lego_bob.mp4",
    "../media/cn.mp4",
    "../media/road.mp4",
    "../media/ski.mp4",
    "../media/trailer.mp4"]
users = [
    {"name":"bob", "id": "0x303992AE4296FD4000003439",
     "media": media[2], 'color': 'white','played': False,},
    {"name":"alice", "id": "0x303992AE4296FD4000003438",
     "media": media[1], 'color': 'red', 'played': False,},
    {"name":"jim", "id": "0x303992AE4296FD400000343D",
     "media": media[0], 'color': 'yellow', 'played': False,}
    ]

############################# Begin Program ####################################
READER_IP = '192.168.1.22'
EVENT_TYPE = "event.tag.report"
# Handle command line argument for alternate ip address
if len(sys.argv) > 1:
    READER_IP = sys.argv[1]
print "Reader IP address is %s" % (READER_IP)

while True:
    try:
        reactive_f.read_tags(READER_IP, EVENT_TYPE)
    except Exception, e:
            print "Open failed: " + str(e)

    call(['cat','tag_list.log'])

    reactive_f.disp_user_media(users)

    for j in range(0,len(users)):
        users[j]["played"] = False
