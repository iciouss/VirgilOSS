import time
import datetime
import json
import asyncio
import discord

#Function to obtain current date in milliseconds
current_milli_time = lambda: int(round(time.time() * 1000))

#Function to convert milliseconds to minutes
millis_to_mins = lambda x: int((x/(1000*60))%60)

#Item dictionary
items = json.load(open('res/items.json'))
#Mission Type dictionary
missions = json.load(open('res/missiontype.json'))
#Solar Nodes Dictionary
locations = json.load(open('res/solarNodes.json'))

#Alert info output
async def alerts(data, bot, channel):
    alertList = data['Alerts']
    for i in range(0,len(alertList)):
        alert = alertList[i]
        case = 0

        #Rewards
        try:
            reward = alert['MissionInfo']['missionReward']['countedItems'][0]
            case = 1
        except KeyError:
            pass

        try:
            reward = alert['MissionInfo']['missionReward']['items'][0]
            case = 2
        except KeyError:
            pass

        if(case != 0):
            #Rewardss String
            if(case == 1 and items[reward['ItemType']] == "Nitain Extract"):
                await bot.send_message(channel, "@everyone Nitain Extract")
            #Time left String
                millis = int(alert['Expiry']['$date']['$numberLong'])-current_milli_time()

                print("Sleep")
                await asyncio.sleep((millis/1000)+60)
                print("Wake up")
                case = 0
