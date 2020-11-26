import discord

from discord.ext import commands

token = ""
prefix = "/"

client = commands.Bot(command_prefix = prefix) 
client.remove_command('help')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='onyxium'))

@client.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	embed=discord.Embed(title="onyxium", description="help commands", color=0x7CFC00)
	embed.add_field(name="ping", value="Bot latency", inline=True)

	await author.send(embed=embed)

	last_message = ctx.channel.last_message_id
	message = await ctx.channel.fetch_message(int(last_message))

	await message.add_reaction(emoji = "<:checkedbox:781556049953423373>") # will probably mess up later on

client.run(token)