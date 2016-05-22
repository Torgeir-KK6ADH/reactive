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
    {"name":"bob", "id": "0x0000000000000000000030C5", "media": media[0]},
    {"name":"alice", "id": "0x0000000000000000000030C8", "media": media[1]},
    {"name":"jim", "id": "0x000000000000AB4D00000000", "media": media[2]}
    ]

############################# Begin Program ####################################
reader_ip = '192.168.1.22'
# Handle command line argument for alternate ip address
if len(sys.argv) > 1:
    reader_ip = sys.argv[1]
print "Reader IP address is %s" % (reader_ip)

try:
    reactive_f.read_tags(reader_ip, "event.tag.arrive")
except Exception, e:
        print "Open failed: " + str(e)

call(['cat','tag_list.log'])

reactive_f.disp_user_media(users)
