import json
from user import user

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
    append = {user: [word, time]}
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
        users.append(user(currId, currWord, currTime))
    users.sort()

    return users