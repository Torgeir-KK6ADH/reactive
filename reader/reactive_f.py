#!/usr/bin/python -u

import sys
import rapid
import time
import csv
from subprocess import call

# Callback to handle events
def event_callback(event):
    rc = event.split("\r\n")
    for x in rc:
        if len(x) > 0:
            tagid = parse_event(event,'tag_id=',26)
            if tagid != 'NULL':
                print "Tag ID: %s " % tagid
            else:
                print "No tag id found: %s" % event

# Parse an event, looking for a field name.  if found, return
# the value of the field, up to the field size
def parse_event(event, field_name, field_size):
      rdata = "NULL"
      # try to find the field name in the event
      field_index=event.find(field_name)
      if field_index != -1:
        # field the found, skip over the field name
        field_index += len(field_name)
        # extract the value of the field
        rdata=event[field_index:field_index+field_size]
      #print "parse_event %s" % rdata

      return rdata

def read_tags(reader_ip, event_type):
    """
    Opens a socket to the ip address, generates a tag list,
    then closes the socket
    """
    # Open socket using reader IP address
    cmd = rapid.Command(reader_ip)
    cmd.open()
    print "Connection to %s opened" % (reader_ip)

    # Reader Login
    cmd.execute("reader.login", ("admin", "readeradmin"))
    rc = cmd.execute("reader.who_am_i", ())
    print "Logged in as: %s " % rc

    # Open an event channel and get id
    id = cmd.getEventChannel(event_callback)
    print "Event Channel ID %s created" % id

    # Register for event_type
    cmd.execute("reader.events.register", (id, event_type))
    print "Registered for event_type on Ch. %s" % id

    # start tag read in active mode
    cmd.set("setup.operating_mode", "active")
    print "Mode: Active"

    # stdout redirection for creating tag list
    stdout = sys.stdout #backup original stdout to console
    sys.stdout = open("tag_list.log", "w")

    # wait for some tag reads
    time.sleep(1)

    # stop tag read in standby mode
    cmd.set("setup.operating_mode", "standby")
    sys.stdout.close()  # close log file
    sys.stdout = stdout # revert to console output
    print "Mode: Standby"
    print "./tag_list.log generated"

    # Unregister for event_type
    cmd.execute("reader.events.unregister", (id, event_type))
    print "Unregistered for %s" % event_type

    # Close the command connection and event channel
    cmd.close()
    print "Connection Closed"


#######################################################3
def disp_user_media(users):
    """
    Parse tag_list. Search for tag-user matches and display their media.
    """
    with open("tag_list.log", "r") as tag_list:
        eof = False
        i = 0
        while eof == False:
            line = tag_list.readline()
            if line == "":
                eof = True
            #strip "Tag ID:" field and \n char
            trim_id = str(line[8:len(line)-2:1])
            for j in range(0,len(users)):
                if trim_id == users[j]["id"] and users[j]["played"] == False:
                    users[j]["played"] = True
                    print "Match user %s" % users[j]["name"]
                    play_media = users[j]["media"]
                    call(['omxplayer', play_media])
            i += 1
