import discord
import requests
from definitions import *

from discord.ext import commands

token = ""
prefix = "/"

client = commands.Bot(command_prefix = prefix) 
client.remove_command('help')


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='github.com/noor0x07/onyxium-bot'))

@client.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	embed=discord.Embed(title="onyxium", description="help commands", color=0x3eb489)
	embed.add_field(name="ping", value="Bot latency", inline=True)

	await author.send(embed=embed)

	last_message = ctx.channel.last_message_id
	message = await ctx.channel.fetch_message(int(last_message))

	await message.add_reaction(emoji = "<:checkedbox:781556049953423373>") # will probably mess up later on

@client.command()
async def ping(ctx):
	await ctx.send(f':hourglass_flowing_sand: Pong! **Latency**: {round(client.latency * 1000)}ms')

@client.command()
async def uptime(ctx):
    global start_time
    await ctx.send(":alarm_clock: **Bot uptime**: " + timedelta_str(datetime.datetime.now() - start_time))

@client.command()
async def ip(ctx, *, ip):
    r = requests.get('http://ip-api.com/json/{}'.format(ip))
    info = json.loads(r.text)

    embed = discord.Embed(title="IP", description="search", color=0x3eb489)
    for i in range(len(info)):
        embed.add_field(name=list(info)[i], value=nullFix(list(info.values())[i]))
    await ctx.send(embed=embed)

@client.command()
@commands.has_guild_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f":tools: {member.mention} has been kicked for **{reason}**")

@client.command()
@commands.has_guild_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f":tools: {member.mention} has been banned for **{reason}**")

@client.command()
@commands.has_guild_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discr = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discr): # only takes name and discrim
            await ctx.guild.unban(user)
            await ctx.send(f":tools: **{user.name}#{user.discriminator}** has been unbanned")
            return

@client.command()
@commands.has_guild_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)

client.run(token)