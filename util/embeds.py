import discord
import util.readData as readData
from datetime import datetime

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
        userTime += f"**{x.score}** ({(datetime.utcfromtimestamp(int(x.time) - 14400).strftime('%Y-%m-%d %H:%M:%S'))})\n"
        rank += 1

    firstUserID = userList[0].id
    lastuserID = userList[-1].id
    
    embed = discord.Embed(title = "🏆 LEADERBOARDS", description = "List of most recent sussy activity of every user. The longer you can go without saying sus words, the higher ranked you are\n\nDon't see your name on the list? Say something sus in any text channel to qualify for a spot!", color=0xbe2d2d)
    embed.set_thumbnail(url = topUser.avatar_url)
    emoji = '\N{POSTBOX}'
    embed.add_field(name=f"{emoji} USERS", value=userID, inline = True)
    embed.add_field(name="🈲 PHRASE", value=userWord, inline = True)
    embed.add_field(name="⏰ SCORE AND TIME (EST)", value=userTime, inline = True)    
    embed.add_field(name="not SUS™✓", value=f"<@{firstUserID}>", inline = True)  
    embed.add_field(name="IMPOSTOR 👺", value=f"<@{lastuserID}>", inline = True) 
    embed.set_footer(text = 'Refreshed every minute. Force a refresh using the lb command.')    
    return embed

def help (guild, wordList):
    embed = discord.Embed(title = "List of Commands:", color=0xbe2d2d)
    embed.set_thumbnail(url="https://i.postimg.cc/yd4Jm0FV/1f8.png")
    embed.add_field(name="List of sussy words:", value=f"{wordList}", inline=False)
    embed.add_field(name="Change prefix", value='`changePrefix`', inline=True)
    embed.add_field(name="Check ping", value='`sus`', inline=True)
    embed.add_field(name="Forceload Leaderboard", value='`lb`', inline=False)
    embed.set_footer(text=f"Prefix: {readData.getPrefix(str(guild.id))}")
    return embed

def ping (client):
    emoji = '\N{POSTBOX}'
    embed = discord.Embed(title=f'sus! {emoji}', color=0xbe2d2d)    
    embed.add_field(name=f'⌛ Latency:', value=f'{round(client.latency * 1000)}ms')
    return embed