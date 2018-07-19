import time
import json
import datetime
import asyncio
import discord
from cetusClass import *

#Function to obtain current date in milliseconds
current_milli_time = lambda: int(round(time.time() * 1000))

nightTime = 3000 #time in seconds
delay = 22000 # time in miliseconds

msg = 0

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

	cetus = Cetus(dayTime,timeLeft)

	try:
		global msg
		if (msg == 0):
			msg = await bot.send_message(channel, embed=cetus.toEmbed())
		else:
			await bot.edit_message(msg, embed=cetus.toEmbed())
			if millisLeft<0 and not dayTime:
				msg=0
	except IndexError:
		pass

	return timeLeft, dayTime
