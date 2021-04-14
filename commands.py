import discord
from discord.ext import commands, tasks
import time
import json
import util.readData as readData
import util.embeds as embeds
import util.rankings as rankings

serverDataPath = 'data/serverData.json'
wordList = ['sus', 'amog', 'vent', 'red', 'among', 'impostor', 'imposter', 'postbox', '\N{POSTBOX}']
intents = discord.Intents.default()
intents.members = True

# why does it break without this ;-;
def get_prefix(client, message):
    return readData.getPrefix(str(message.guild.id))

client = commands.Bot(command_prefix = get_prefix, intents=intents)

@tasks.loop(seconds = 60)
async def update():
    # print('loop')
    for x in client.guilds:
        await rankings.updateLeaderboard(client, x)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('AMOGUS'))
    print('Kinda sus!')

#Adds required roles and data to json file upon joining a server
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

#force update leaderboard
@client.command()
async def lb(ctx):  
    userList = readData.getUsers(str(ctx.guild.id))
    try:
        topUser = await client.fetch_user(int(userList[0].id))
        await ctx.channel.send(embed = embeds.leaderBoard(userList, topUser))
        await rankings.updateLeaderboard(client, ctx.guild)
    except IndexError:
        await ctx.send('No one has said a sussy word yet!')

#check ping
@client.command(aliases=['sus'])
async def check(ctx):
    await ctx.send(embed = embeds.ping(client))

#all client.event stuff
@client.event
async def on_message(msg):
    try:
        #delete messages in leaderboard channel
        if discord.utils.get(msg.guild.channels, name='sus-leaderboard') is not None and not msg.author.bot:
            lbChannel = discord.utils.get(msg.guild.channels, name='sus-leaderboard')
            if(msg.channel.id == lbChannel.id):
                await msg.delete()
        #sus word
        for x in wordList: #shove this into a method later
            if not msg.content.lower().startswith(('.', readData.getPrefix(str(msg.guild.id)))) and x in msg.content.lower() and not msg.author.bot:
                emoji = '\N{POSTBOX}'
                await msg.add_reaction(emoji)
                readData.addUser(str(msg.guild.id), str(msg.author.id), x, str(int(time.time())))
        #help command
        if msg.mentions[0] == client.user:
            await msg.channel.send(embed = embeds.help(msg.guild, wordList))
    except IndexError:
        pass
    await client.process_commands(msg)    

update.start()
with open('data/run.json') as f:
    token = json.load(f);
client.run(token['token']) 

