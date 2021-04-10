import discord
from discord.ext import commands
import datetime
import asyncio
import random
import json

prefixPath = 'data/prefix.json'

def get_prefix(client, message):
    with open(prefixPath, 'r') as f:
        prefixes = json.load(f);
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('AMOGUS'))
    print('Kinda sus!')

#sets prefix after joining a server
@client.event
async def on_guild_join(guild):
    print(f'joined server {guild.id}')
    with open(prefixPath, 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '.'
    with open(prefixPath, 'w') as f:
        json.dump(prefixes,f)

#change prefix
@client.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):
    with open(prefixPath, 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open(prefixPath, 'w') as f:
        json.dump(prefixes,f)
    await ctx.send(f'prefix is now {prefix}')

#probably should change this to a general help command some time soon
@client.event
async def on_message(msg):
    try:
        if msg.mentions[0] == client.user:
            with open (prefixPath, 'r') as f:
                prefixes = json.load(f)
            pre = prefixes[str(msg.guild.id)]
        await msg.channel.send(f'Prefix for this server is: {pre}')    
    except:
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