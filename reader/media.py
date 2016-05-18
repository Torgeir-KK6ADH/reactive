#!/usr/bin/python -u

from subprocess import call

users = [
    {"name":"bob", "id": "0x0000000000000000000030C5", "media": "cn.mp4"},
    {"name":"alice", "id": "0x0000000000000000000030C8", "media": "road.mp4"},
    {"name":"jim", "id": "0x000000000000AB4D000030C6", "media": "ski.mp4"},
    ]
media = [
    "cn.mp4",
    "road.mp4",
    "ski.mp4",
    "trailer.mp4"]

#print users
print "\n\n"

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
            #print j
            #print trim_id
            #print users[j]["id"]
            #print trim_id == users[j]["id"]
            if trim_id == users[j]["id"]:
                print users[j]["name"]
        i += 1


        #if i < 3:
        #    users[i]["id"] = str(line[8:len(line)-1:1])
        #    i+=1

# check tag id, put in db
#if in db, increase (count)
