import discord

token = "1234"
prefix = "/"

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='onyxium'))

client.run(token)

# small commits are for code management, not releases