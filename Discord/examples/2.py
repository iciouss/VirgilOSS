import random
import asyncio
import aiohttp
import json
import discord
from discord import Game
from discord.ext.commands import Bot

#prefijos a usar por el bot
BOT_PREFIX = ("$", "%")
TOKEN = "NDY3NDYzOTAyOTc2OTMzODg4.Diq_fQ.mEQ1J4EgUjtUFFlAvphOAvSaVAo"  # Get at discordapp.com/developers/applications/me

#inicializacion de la clase
client = Bot(command_prefix=BOT_PREFIX)
channel = discord.Object(id='223751299160735744')

#definicion de comando, coge nombre de la funcion siguiente
@client.command(name = 'hello',
		description = "Writes hello in the server",
		brief = "Very kind bot")
async def hello():
    await client.send_message(channel, "Hello, prueba joaquin")

#----------------------------------------------------------

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Warframe: Fortuna"))
    print("Logged in as " + client.user.name)

client.loop.create_task(sayHello())
client.loop.create_task(sayGb())
client.run(TOKEN)
