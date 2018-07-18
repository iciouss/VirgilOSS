import discord
#from prueba import *
from discord.ext.commands import Bot
from discord import Game

import requests
import json
import time
import datetime
import sched
import asyncio
from alerts import *
from cetus import *

TOKEN = 'NDY4ODcyODU0Mjg1NTgyMzM2.Di_fkA.Cp8uHJ4FACkgojPpXrrBLZxUJtg'
#my server
#channel = discord.Object(id='223751299160735744')
#Warframe server
channel = discord.Object(id='455095784119992340')

#prefijos a usar por el bot
BOT_PREFIX = ("$", "%")

#Timed function
s = sched.scheduler(time.time, time.sleep)
data = 0

#Update JSON and call alerts
async def update():
    while not client.is_closed:
        while True:
            try:
                global data
                data = json.loads(requests.get("http://content.warframe.com/dynamic/worldState.php").text)
                print("JSON updated")
                break
            except requests.exceptions.ConnectionError:
                print("Cannot fetch JSON correctly. Retrying...")
                time.sleep(5) 
        #sleep timer for loop
        await asyncio.sleep(60)

#inicializacion de la clase
client = Bot(command_prefix=BOT_PREFIX)

#definicion de comando, coge nombre de la funcion siguiente
#@client.command(name = 'hello',
#		description = "Informs of the current alerts",
#		brief = "Informs of the current alerts")
async def loop():
    await client.wait_until_ready()
    while not client.is_closed:
        #await client.send_message(channel, "Hello")
        await alerts(data,client,channel)
        #timeLeft, dayTime = await cetusTime(data,client,channel)
        #if dayTime:
        #    await client.change_presence(game=Game(name="{}m to Night".format(timeLeft.minute)))
        #else:
        #    await client.change_presence(game=Game(name="{}m to Day".format(timeLeft.minute)))
        await asyncio.sleep(60)
    

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(update())
client.loop.create_task(loop())
client.run(TOKEN)
