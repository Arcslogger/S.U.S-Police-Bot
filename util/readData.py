import json
import math
import time
from util.user import user

path = 'data/serverData.json'

def addServer(guildID):
    #open orig file as dict
    with open (path, 'r') as f:
        data = json.load(f)
    #append new server data to dict 
    append = {guildID:{'prefix': "%", 'users': {}}}
    data.update(append)
    #write updated dict to file
    with open (path, 'w') as f:
        json.dump(data, f, indent=4)
    
def addUser(guildID, user, word, time):
    #open orig file as dict
    with open (path, 'r') as f:
        data = json.load(f)
        #append user data to dict
        currUser = data[guildID]["users"].get(user)
        if word =='filler' and currUser is not None:
            append = {user: [str(currUser[0]), str(currUser[1]), str(int(currUser[2]) + 1)]}
            data[guildID]["users"].update(append)
        elif word != 'filler':
            append = {user: [word, time, "1"]}
            data[guildID]["users"].update(append)
        #append updated dict to file
        with open (path, 'w') as f:
            json.dump(data, f, indent=4)

def changePrefix(guildID, prefix):
    with open (path, 'r') as f:
        data = json.load(f)

    data[guildID]["prefix"] = prefix

    with open (path, 'w') as f:
        json.dump(data, f, indent=4)

def getPrefix(guildID):
    with open (path, 'r') as f:
        data = json.load(f)
    return data[guildID]["prefix"]

def getUsers(guildID):
    with open (path, 'r') as f:
        data = json.load(f)
    
    users = []
    for x in data[guildID]["users"].keys():
        currId = x
        currWord = data[guildID]["users"].get(x)[0]
        currTime = data[guildID]["users"].get(x)[1]
        msgCount = int(data[guildID]["users"].get(x)[2])
        score = int(math.sqrt(int(time.time()) - int(currTime)) + int(msgCount / 10)) #change this for the score
        users.append(user(currId, currWord, currTime, score))

    users.sort()

    return users