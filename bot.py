import discord
import json
from discord.ext import commands

client = commands.Bot(command_prefix = '.')
with open('run.json') as f:
    token = json.load(f);

@client.event
async def on_ready():
    print('Kinda sus!')

@client.command(aliases=['sus'])
async def check(ctx):
    await ctx.send('sus!')

client.run(token['token']) 