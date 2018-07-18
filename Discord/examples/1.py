# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import time

TOKEN = 'NDY3NDYzOTAyOTc2OTMzODg4.Diq_fQ.mEQ1J4EgUjtUFFlAvphOAvSaVAo'

client = discord.Client()
msg1 = 0
embed = 0

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = ':thinking:'.format(message)
        msg = await client.send_message(message.channel, msg)
        time.sleep(5)
        await client.edit_message(msg,"Cambio el mensaje")
        time.sleep(5)
        await client.delete_message(msg)
        time.sleep(5)
        await client.delete_message(message)
    
    if message.content.startswith('!embed'):
        global embed
        embed = discord.Embed(title="Tile", description="Desc", color=0x00ff00)
        embed.add_field(name="Field1", value="hi", inline=True)
        embed.add_field(name="Field2", value="hi2", inline=True)
        global msg1
        msg1 = await client.send_message(message.channel, embed=embed)

    if message.content.startswith('!edit'):
    	embed.remove_field(1)
    	await client.edit_message(msg1, embed=embed)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
