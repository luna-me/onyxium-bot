import discord
import requests
from definitions import *
from discord.ext import commands

token = ""
prefix = "/"

client = commands.Bot(command_prefix=prefix)
client.remove_command('help')


@client.event
async def on_ready():
	print('Logged in as {0.user}'.format(client))
	print("Currently in "+str(len(client.guilds)) + " server(s)")
	await client.change_presence(activity=discord.Game(name="/help | https://github.com/noor0x07/onyxium-bot/"))


@client.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	embed = discord.Embed(title="Onyxium", description="This is a list of all the current commands", color=0x3eb489)
	embed.add_field(name="```ping```", value="Bot latency", inline=False)
	embed.add_field(name="```uptime```", value="see bot uptime", inline=False)
	embed.add_field(name="```ip```", value="see specific ip details", inline=False)
	embed.add_field(name="```kick```", value="kick a user from server", inline=False)
	embed.add_field(name="```ban```", value="ban a user from server", inline=False)
	embed.add_field(name="```unban```", value="unban a user from server", inline=False)
	embed.add_field(name="```purge```", value="purge a number of messages", inline=False)
	embed.add_field(name="```whois```", value="show info about an account", inline=False)
	embed.add_field(name="```avatar```", value="see a user's avatar", inline=False)
	embed.add_field(name="```info```", value="info about bot", inline=False)
	embed.add_field(name="```say```", value="make the bot say something", inline=False)
	embed.set_footer(text='https://github.com/noor0x07/onyxium-bot')
	last_message = ctx.channel.last_message_id
	message = await ctx.channel.fetch_message(int(last_message))

	await message.add_reaction(emoji="<:checkedbox:781556049953423373>")  # will probably mess up later on
	
	await author.send(embed=embed)


@client.command()
async def ping(ctx):
	await ctx.send(f':hourglass_flowing_sand: Pong! **Latency**: {round(client.latency * 1000)}ms')


@client.command()
async def uptime(ctx):

	await ctx.send(":alarm_clock: **Bot uptime**: " + timedelta_str(datetime.datetime.now() - start_time))


@client.command()
async def ip(ctx, *, address):
	r = requests.get('http://ip-api.com/json/{}'.format(address))
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

		if (user.name, user.discriminator) == (member_name, member_discr):  # only takes name and discrim
			# await ctx.guild.unban(user)
			await ctx.send(f":tools: **{user.name}#{user.discriminator}** has been unbanned")
			return


@client.command(aliases=["prune"])
@commands.has_guild_permissions(manage_messages=True)
async def purge(ctx, amount: int):
	await ctx.channel.purge(limit=amount + 1)


@client.command()
@commands.has_guild_permissions(administrator=True)
async def whois(ctx, member: discord.Member = None):
	roles = [role for role in member.roles if role != ctx.guild.default_role]
	embed = discord.Embed(color=0x3eb489, timestamp=ctx.message.created_at, title=f"Who is - {member}")
	embed.set_thumbnail(url=member.avatar_url)
	embed.set_footer(text=f"Requested by {ctx.author}")

	embed.add_field(name="ID:", value=member.id)
	embed.add_field(name="Name:", value=member.display_name)

	embed.add_field(name="Created account on:", value=member.created_at.strftime("%a, %#d %B %Y at %I:%M %p UTC"))
	embed.add_field(name="Joined server on:", value=member.joined_at.strftime("%a, %#d %B %Y at %I:%M %p UTC"))

	embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
	embed.add_field(name="Highest Role:", value=member.top_role.mention)
	await ctx.send(embed=embed)


@client.command(aliases=['pfp', 'av'])
async def avatar(ctx, member: discord.Member):
	show_avatar = discord.Embed(color=0x3eb489, description=f":bust_in_silhouette: **{member.display_name}**'s avatar : ")
	show_avatar.set_image(url='{}'.format(member.avatar_url))
	await ctx.send(embed=show_avatar)

	
@client.command(aliases=['about', 'info', 'links'])
async def invite(ctx):
	embed = discord.Embed(
		title='Onyxium',
		description='Information and links',
		colour=0x3eb489

	)

	embed.set_footer(text='')
	embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/772944435020431392/ecfa2b9967914c73faead132eb7b26f6.png?size=128')
	embed.add_field(name='Invite Link', value='[here](https://discord.com/api/oauth2/authorize?client_id=772944435020431392&permissions=8&scope=bot)', inline=False)
	embed.add_field(name='GitHub Repo', value='[here](https://github.com/noor0x07/onyxium-bot)', inline=False)
	embed.add_field(name='Discord Link', value='[here](https://discord.gg/adCPaYNEGv)', inline=False)
	await ctx.send(embed=embed)


@client.command()
@commands.has_guild_permissions(administrator=True)
async def say(ctx, *, message=None):
	await ctx.send(message)


client.run(token)
