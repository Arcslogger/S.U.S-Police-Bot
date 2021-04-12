import discord
from datetime import datetime
import readData

def leaderBoard (userList, topUser):
    userID = ""
    userWord = ""
    userTime = ""
    rank = 1

    for x in userList:
        
        userID += f"{rank}.\t<@{x.id}>\n"
        userWord += f"`{x.word}`\n"
        userTime += f"{(datetime.utcfromtimestamp(int(x.time) - 14400).strftime('%Y-%m-%d %H:%M:%S'))}\n"
        rank += 1
        
    embed = discord.Embed(title = "🏆 LEADERBOARD")
    embed.set_thumbnail(url = topUser.avatar_url)
    embed.add_field(name="USERS", value=userID, inline = True)
    embed.add_field(name="PHRASE", value=userWord, inline = True)
    embed.add_field(name="TIME", value=userTime, inline = True)    
    embed.set_footer(text = "Refreshed every minute.")    
    return embed