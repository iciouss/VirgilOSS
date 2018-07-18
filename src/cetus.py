import time
import json
import datetime
import asyncio
import discord

#Function to obtain current date in milliseconds
current_milli_time = lambda: int(round(time.time() * 1000))

nightTime = 3000 #time in seconds
delay = 22000 # time in miliseconds

async def cetusTime(data, bot, channel):
    expiry = int(data['SyndicateMissions'][9]['Expiry']['$date']['$numberLong'])
    now = current_milli_time()
    bountiesClone = expiry
    millisLeft = bountiesClone-now
    secondsToNightEnd = (millisLeft / 1000)
    dayTime = secondsToNightEnd > nightTime

    secondsRemainingInCycle = secondsToNightEnd - nightTime if dayTime else secondsToNightEnd
    millisLeft = secondsRemainingInCycle * 1000
    timeLeft = datetime.datetime.utcfromtimestamp(millisLeft/1000.0)

    if(dayTime==True):
        actualTime = "Day"
        #picture ="https://assets.pokemon.com/assets/cms2/img/pokedex/full/338.png"
        picture = "https://vignette.wikia.nocookie.net/warframe/images/6/66/EquinoxDay.png/revision/latest/scale-to-width-down/291?cb=20150731174046"
        color = 0xffffff
    else:
        actualTime = "Night"
        #picture ="https://assets.pokemon.com/assets/cms2/img/pokedex/full/337.png"
        picture = "https://vignette.wikia.nocookie.net/warframe/images/4/46/EquinoxNight.png/revision/latest/scale-to-width-down/291?cb=20150731174104"
        color = 0x000001

    if(timeLeft.hour==0):
        msgLeft = "{} minutes {} seconds".format(timeLeft.minute, timeLeft.second)
    else:
        msgLeft = "{} hours {} minutes {} seconds".format(timeLeft.hour, timeLeft.minute, timeLeft.second)

    embed=discord.Embed(title="Cetus", description=actualTime, color=color)
    embed.set_thumbnail(url=picture)
    embed.add_field(name="Time Remaining", value=msgLeft, inline=False)
    await bot.send_message(channel, embed=embed)

    return timeLeft, dayTime