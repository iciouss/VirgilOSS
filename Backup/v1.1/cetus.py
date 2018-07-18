import time
import json
import datetime
import asyncio

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

    if(dayTime):
        await bot.send_message(channel, "It is daytime in the Plains")
    else:
        await bot.send_message(channel, "It is nighttime in the Plains")
    
    if(timeLeft.hour==0):
        await bot.send_message(channel, "Time remaining: {} minutes {} seconds".format(timeLeft.minute, timeLeft.second))
    else:
        await bot.send_message(channel, "Time remaining: {} hours {} minutes {} seconds".format(timeLeft.hour, timeLeft.minute, timeLeft.second))
    await bot.send_message(channel, '-----------------------------------------')
    return timeLeft, dayTime

