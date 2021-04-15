import discord
import util.readData as readData
from datetime import datetime
import math
import time

def leaderBoard (userList, topUser):
    userID = ""
    userWord = ""
    userTime = ""
    rank = 1

    for x in userList:
        if rank == 1:
            userID += f"🥇\t<@{x.id}>\n"
        elif rank == 2:
            userID += f"🥈\t<@{x.id}>\n"
        elif rank == 3:
            userID += f"🥉\t<@{x.id}>\n"
        else:
            userID += f"{rank}.\t<@{x.id}>\n"
        userWord += f"\"{x.word}\"\n"
        userTime += f"{x.score}\n"
        #userTime += f"**{x.score}** ({(datetime.utcfromtimestamp(int(x.time) - 14400).strftime('%Y-%m-%d %H:%M:%S'))})\n"
        rank += 1
        if rank == 21:
            break

    firstUserID = userList[0].id
    lastuserID = userList[-1].id
    
    embed = discord.Embed(title = "🏆 LEADERBOARDS", description = "List of the least sus members of the server. Your sus score is calculated using your server activity and the time since your last sus message\n\nDon't see your name? Our list only displays 20 members at most Use the `score` command to check how close you are to the top!", color=0xbe2d2d)
    embed.set_thumbnail(url = topUser.avatar_url)
    emoji = '\N{POSTBOX}'
    embed.add_field(name=f"{emoji} USERS", value=userID, inline = True)
    embed.add_field(name="💬 PHRASE", value=userWord, inline = True)
    embed.add_field(name="💯 SUS SCORE", value=userTime, inline = True)    
    embed.add_field(name="not SUS™✓", value=f"<@{firstUserID}>", inline = True)  
    embed.add_field(name="IMPOSTOR 👺", value=f"<@{lastuserID}>", inline = True) 
    embed.set_footer(text = 'Refreshed every minute. Force a refresh using the lb command.')    
    return embed

def help (guild, wordList):
    embed = discord.Embed(title = "List of Commands:", description=f"Current sussy words checked:\n`{wordList}`", color=0xbe2d2d)
    embed.set_thumbnail(url="https://i.postimg.cc/yd4Jm0FV/1f8.png")
    embed.add_field(name="Change prefix:", value='`changePrefix`', inline=True)
    embed.add_field(name="Check ping:", value='`sus`', inline=True)
    embed.add_field(name="Forceload Leaderboard:", value='`lb`', inline=True)
    embed.add_field(name="Check your stats:", value="`score`", inline=True)
    embed.add_field(name="Check stats of a user:", value="`score @<user>`", inline=True)
    embed.set_footer(text=f"Prefix: {readData.getPrefix(str(guild.id))}")
    return embed

def ping (client):
    emoji = '\N{POSTBOX}'
    embed = discord.Embed(title=f'sus! {emoji}', color=0xbe2d2d)    
    embed.add_field(name=f'⌛ Latency:', value=f'{round(client.latency * 1000)}ms')
    return embed

def score (user, nick, word, susTime, msgCount):
    currTime = int(time.time())
    secondsSince = int(currTime - susTime)
    timeFormatted = datetime.utcfromtimestamp(susTime - 14400).strftime('%Y-%m-%d %H:%M:%S')
    scoreFormatted = int(math.sqrt(secondsSince) + int(msgCount / 6))

    embed = discord.Embed(title = f"📃 STATS FOR: {nick}", description="Score is calculated using the formula:\n`√(seconds since sus message) + (messages since / 6)`\n \n _ _", color=0xbe2d2d)   
    embed.set_thumbnail(url = user.avatar_url)
    embed.add_field(name=f"💬 LAST SUS PHRASE:", value = f'`{word}`', inline = True)
    embed.add_field(name=f"🕜 TIME (EST):", value = f'`{timeFormatted}`', inline = True)
    embed.add_field(name=f"📈 MESSAGES SINCE:", value = f'`{msgCount}`', inline = True)
    embed.add_field(name=f"💯 SCORE:", value = f'```\n√({secondsSince}) + ({msgCount} / 6) = {scoreFormatted}```', inline = True)
    embed.set_footer(text="Note: Score will always be floored due to the nature of integer casting")
    return embed