import discord
from discord.ext import commands
import datetime
import asyncio
import random
import json
import readData

serverDataPath = 'data/serverData.json'
wordList = ['sus', 'amogus', 'vent', 'red']

def get_prefix(client, message):
    with open(serverDataPath, 'r') as f:
        prefixes = json.load(f);
    return prefixes[str(message.guild.id)]["prefix"]


client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('AMOGUS'))
    print('Kinda sus!')

#sets prefix after joining a server
@client.event
async def on_guild_join(guild):
    readData.addServer(str(guild.id))
    print(f'joined server {guild.id}')

#change prefix
@client.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):
    readData.changePrefix(prefix)
    await ctx.send(f'prefix is now {prefix}')

#all client.event stuff
@client.event
async def on_message(msg):
    
    try:
        #sus word
        for x in wordList:
            if x in msg.content.lower():
                print("sus")
                emoji = '\N{POSTBOX}'
                await msg.add_reaction(emoji)
                readData.addUser(str(msg.guild.id), str(msg.author.id), str(msg), -1)

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

# #leave server so no need to kick
# @client.command()
# async def leave(ctx):
#     await ctx.guild.leave()



with open('data/run.json') as f:
    token = json.load(f);
client.run(token['token']) 