import json

path = 'data/serverData.json'

def addServer(guildID):
    #open orig file as dict
    with open (path, 'r') as f:
        data = json.load(f)
    #append new server data to dict 
    append = {guildID:{'prefix': ".", 'users': {}}}
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

def main ():
    addServer('test')
    addUser('test', 'arcs', 'sus', '1000')
    addUser('test', 'antichess', 'vent', '1000')
    addUser('test', 'arcs', 'red', '2000')
    changePrefix('test', '?')

if __name__ == "__main__":
    main()