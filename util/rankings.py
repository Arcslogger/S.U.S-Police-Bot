import discord
import json
import util.readData as readData
import util.embeds as embeds

async def updateRoles(guild, userList):

    if discord.utils.get(guild.roles,name="not SUS™✓") is None:
        await guild.create_role(name="not SUS™✓", colour=discord.Colour(0x00D62E))
    if discord.utils.get(guild.roles,name="IMPOSTOR 👺") is None:
        await guild.create_role(name="IMPOSTOR 👺", colour=discord.Colour(0xFF0000))

    firstRole = discord.utils.get(guild.roles,name="not SUS™✓")
    lastRole = discord.utils.get(guild.roles,name="IMPOSTOR 👺")

    members = guild.members
    for member in members:
        if firstRole in member.roles and member.id != int(userList[0].id):
            await member.remove_roles(firstRole)
        if lastRole in member.roles and member.id != int(userList[-1].id):
            await member.remove_roles(lastRole)
    await guild.get_member(int(userList[0].id)).add_roles(firstRole)
    await guild.get_member(int(userList[-1].id)).add_roles(lastRole)

async def updateLeaderboard(client, guild):
    try:
        if discord.utils.get(guild.channels, name='sus-leaderboard') is None:
            lbChannel = await guild.create_text_channel('sus leaderboard')
            await lbChannel.edit(position=0, sync_permissions=True)
        else:
            lbChannel = discord.utils.get(guild.channels, name='sus-leaderboard')

        userList = readData.getUsers(str(guild.id))
        await updateRoles(guild, userList)
        topUser = await client.fetch_user(int(userList[0].id))
        messageID = lbChannel.last_message_id
        
        if messageID is None:
            await lbChannel.send(embed = embeds.leaderBoard(userList, topUser))
        else:
            try:
                lbMessage = await lbChannel.fetch_message(messageID)
                await lbMessage.edit(embed = embeds.leaderBoard(userList, topUser))
            except Exception as e: #if bot can't edit a message, reset channel and display a new leaderboard
                print(f"leaderboard edit error: {e}")
                await lbChannel.purge(limit=10)
                await lbChannel.send(embed = embeds.leaderBoard(userList, topUser))
    except Exception as e:
        print(f"leaderboard error in server {guild.name}")
        print(e)

async def score(client, serverDataPath, ctx, member):
    with open (serverDataPath, 'r') as f:
        data = json.load(f)
    
    userData = data[str(ctx.guild.id)]["users"].get(str(member.id))
    nick = member.nick
    if nick is None:
        nick = member.name

    if userData is not None:
        userObj = await client.fetch_user(member.id)
        await ctx.send(embed = embeds.score(userObj, nick, userData[0], int(userData[1]), int(userData[2])))
    else:
        await ctx.send(f"{nick} has never acted sussy!")