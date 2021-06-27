from collections import UserDict
import discord
from discord.ext import commands, tasks
import time
import json
import util.readData as readData
import util.embeds as embeds
import util.rankings as rankings

serverDataPath = 'data/serverData.json'
wordList = ['sus', '5u5', 'amog', 'am0g', 'vent', 'v3nt', 'red', 'r3d', 'among', 'am0ng', 'impostor', 'imposter', 'postbox', 'flower playing cards', '月', 'ඞ', '\N{POSTBOX}', '\N{FLOWER PLAYING CARDS}', '\N{SQUARED SOS}', '\N{SUSHI}', '\N{SUSPENSION RAILWAY}']
intents = discord.Intents.default()
intents.members = True
intents.messages = True

# why does it break without this ;-;
def get_prefix(client, message):
    return readData.getPrefix(str(message.guild.id))

#sus word detector
def check_sus(msg):
    word = 'filler'
    for x in wordList: #shove this into a method later
        if not msg.content.lower().startswith(('.', readData.getPrefix(str(msg.guild.id)))) and x in msg.content.lower():
            word = x
    return word

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

#bot stats
@client.command()
async def stats(ctx):
    if ctx.author.id == 358028710827261964:
        await ctx.channel.send(embed = embeds.devStats(client, int(round((time.time() - startTime)))))
    else:
        await ctx.channel.send('You are not premitted to use this command')

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

#check score of member
@client.command()
async def score(ctx, member : discord.Member):
    await rankings.score(client, serverDataPath, ctx, member)

#check score of self
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) and ctx.message.content.lower().startswith(str(readData.getPrefix(str(ctx.guild.id))) + "score"):
        await rankings.score(client, serverDataPath, ctx, ctx.author)

#all client.event stuff
@client.event
async def on_message(msg):
    if not msg.author.bot:
        try:
            #delete messages in leaderboard channel
            if discord.utils.get(msg.guild.channels, name='sus-leaderboard') is not None:
                lbChannel = discord.utils.get(msg.guild.channels, name='sus-leaderboard')
                if(msg.channel.id == lbChannel.id):
                    await msg.delete()
            #sus word
            word = check_sus(msg)
            if word != 'filler':
                await msg.add_reaction('\N{POSTBOX}')
            readData.addUser(str(msg.guild.id), str(msg.author.id), word, str(int(time.time())))
            #help command
            if msg.mentions[0] == client.user:
                await msg.channel.send(embed = embeds.help(msg.guild, wordList))
        except IndexError:
            pass
        await client.process_commands(msg)   

@client.event
async def on_member_remove(member):
    readData.removeUser(str(member.guild.id), str(member.id))

@client.event
async def on_message_edit(before, after):
    if not before.author.bot and before.content != after.content: #if edited message contains sus word
        word = check_sus(after)
        if word != 'filler':
            await after.add_reaction('\N{POSTBOX}')
        readData.addUser(str(after.guild.id), str(after.author.id), word, str(int(time.time())))

startTime = time.time()
update.start()
with open('data/run.json') as f:
    token = json.load(f);
client.run(token['token']) 

