import time
import datetime
import json
import asyncio

#Function to obtain current date in milliseconds
current_milli_time = lambda: int(round(time.time() * 1000))

#Function to convert milliseconds to minutes
millis_to_mins = lambda x: int((x/(1000*60))%60)

#Item dictionary
items = json.load(open('../res/items.json'))
#Mission Type dictionary
missions = json.load(open('../res/missiontype.json'))
#Solar Nodes Dictionary
location = json.load(open('../res/solarNodes.json'))

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

            #mission type
            await bot.send_message(channel, "Mission Type: {}".format(missions[alert['MissionInfo']['missionType']]['value']))

            #Location
            await bot.send_message(channel, "Location: {}".format(location[alert['MissionInfo']['location']]['value']))
    
            #Rewards
            if(case == 1):
                try:
                    await bot.send_message(channel, "Rewards: {}x {}".format(reward['ItemCount'],items[reward['ItemType']]))
                except KeyError:
                    pass
            else:
                try:
                    await bot.send_message(channel, "Rewards: {}".format(items[reward]))
                except KeyError:
                    pass

            #Remaining mission time
            millis = int(alert['Expiry']['$date']['$numberLong'])-current_milli_time()
            timeLeft = datetime.datetime.utcfromtimestamp(millis/1000.0)
            if(timeLeft.hour==0):
                await bot.send_message(channel, "Time remaining: {} minutes".format(timeLeft.minute))
            else:
                await bot.send_message(channel, "Time remaining: {} hours {} minutes".format(timeLeft.hour, timeLeft.minute))
            await bot.send_message(channel, '-----------------------------------------')
            case = 0
