import discord
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime
import time
from user import user
import asyncio
import random
import json
import readData
import embeds
from itertools import cycle

serverDataPath = 'data/serverData.json'
wordList = ['sus', 'amogus', 'vent', 'red']

def get_prefix(client, message):
    with open(serverDataPath, 'r') as f:
        prefixes = json.load(f);
    return prefixes[str(message.guild.id)]["prefix"]

client = commands.Bot(command_prefix = get_prefix)

async def updateLeaderboard(guild):
    if discord.utils.get(guild.channels, name='sus-leaderboard') is None:
        lbChannel = await guild.create_text_channel('sus leaderboard')
        await lbChannel.edit(position=0, sync_permissions=True)
    else:
        lbChannel = discord.utils.get(guild.channels, name='sus-leaderboard')

    userList = readData.getUsers(str(guild.id))
    topUser = await client.fetch_user(int(userList[0].id))
    messages = await lbChannel.history(limit=123).flatten()

    if not messages:
        lbMessage = await lbChannel.send(embed = embeds.leaderBoard(userList, topUser))
    else:
        lbMessage = await lbChannel.fetch_message(lbChannel.last_message_id)
        await lbMessage.edit(embed = embeds.leaderBoard(userList, topUser))

@tasks.loop(seconds = 60)
async def update():
    print('loop')
    for x in client.guilds:
        await updateLeaderboard(x)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('AMOGUS'))
    print(int(time.time()))
    print('Kinda sus!')

#sets prefix after joining a server
@client.event
async def on_guild_join(guild):
    readData.addServer(str(guild.id))
    print(f'joined server {guild.id}')

#change prefix
@client.command()
@commands.has_permissions(administrator = True)
async def changePrefix(ctx, prefix):
    readData.changePrefix(str(ctx.guild.id), prefix)
    await ctx.send(f'prefix is now {prefix}')

@client.command()
async def lb(ctx):  
    userList = readData.getUsers(str(ctx.guild.id))
    topUser = await client.fetch_user(int(userList[0].id))
    await ctx.channel.send(embed = embeds.leaderBoard(userList, topUser))

@client.command(seconds = 5)
async def createLeaderboard(ctx):
    updateLeaderboard(ctx.guild)
    
#all client.event stuff
@client.event
async def on_message(msg):
    try:
        #sus word
        for x in wordList:
            if x in msg.content.lower() and not msg.author.bot:
                print("sus")
                emoji = '\N{POSTBOX}'
                await msg.add_reaction(emoji)
                readData.addUser(str(msg.guild.id), str(msg.author.id), x, str(int(time.time())))
        #help command
        if msg.mentions[0] == client.user:

            embed = discord.Embed(title = "List of Commands:")
            embed.set_thumbnail(url="https://i.postimg.cc/yd4Jm0FV/1f8.png")
            embed.add_field(name="List of sussy words:", value=f"{wordList}", inline=False)
            embed.add_field(name="Change prefix (requires admin perms)", value="changePrefix", inline=False)
            embed.set_footer(text=f"Prefix: {readData.getPrefix(str(msg.guild.id))}")
            await msg.channel.send(embed = embed)
           
    except IndexError:
        pass
    await client.process_commands(msg)    

#test command
@client.command(aliases=['sus'])
async def check(ctx):
    await ctx.send('sus!')

update.start()

with open('data/run.json') as f:
    token = json.load(f);
client.run(token['token']) 

