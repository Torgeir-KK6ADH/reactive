#!/usr/bin/python -u
import reactive_f
import sys
from subprocess import call

################################################################################
media = [
    "../media/cn.mp4",
    "../media/road.mp4",
    "../media/ski.mp4",
    "../media/trailer.mp4"]
users = [
    {"name":"bob", "id": "0xE200322F81854F711306753C",
     "media": media[0], 'played': False,},
    {"name":"alice", "id": "0xE200322F8185517113067544",
     "media": media[1], 'played': False,},
    {"name":"jim", "id": "0x777000000000000000000000",
     "media": media[2], 'played': False,}
    ]

############################# Begin Program ####################################
reader_ip = '192.168.1.22'
# Handle command line argument for alternate ip address
if len(sys.argv) > 1:
    reader_ip = sys.argv[1]
print "Reader IP address is %s" % (reader_ip)

try:
    reactive_f.read_tags(reader_ip, "event.tag.report")
except Exception, e:
        print "Open failed: " + str(e)

call(['cat','tag_list.log'])

reactive_f.disp_user_media(users)
