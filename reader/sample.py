
#!/usr/bin/python -u

import rapid
import sys
import time

# Callback to handle events
def event_callback(event):
    rc = event.split("\r\n")
    for x in rc:
        if len(x) > 0:
            tagid = parse_event(event,'tag_id=',26)
            if tagid != 'NULL':
                print "Tag ID: %s " % tagid
            else :
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

reader = "192.168.1.22"
if len(sys.argv) > 1:
    reader = sys.argv[1]
    
try:
    # Open connection to the reader
    cmd = rapid.Command(reader)
    cmd.open()
    print "Connection Opened"

    # Get the reader's name    
    rc = cmd.get('info.name')
    print "Name: %s " % rc

    # Login in as administrator    
    cmd.execute("reader.login", ("admin", "readeradmin"))
    rc = cmd.execute("reader.who_am_i", ())
    print "Login: %s " % rc

    # Open an event channel and get it's id
    id = cmd.getEventChannel(event_callback)
    print "Event Channel ID: %s" % id
    
    # Register for event.tag.report
    cmd.execute("reader.events.register", (id, "event.tag.report"))
    print "Registered for event.tag.report"
    
    # Set operating mode to active
    cmd.set("setup.operating_mode", "active")
    print "Operating Mode: Active"
    
    # Sleep while handling tag events
    time.sleep(.5)        

    # set operating mode to standby
    cmd.set("setup.operating_mode", "standby")
    print "Operating Mode: Standby"

    # Unregister for event.tag.report
    cmd.execute("reader.events.unregister", (id, "event.tag.report"))
    print "Unregistered for event.tag.report"
    
    # Close the command connection and event channel
    cmd.close()
    print "Connection Closed"    
    
except Exception, e:
    print "Open failed: " + str(e)
    
    
