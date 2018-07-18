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
items = json.load(open('../res/items.json'))
#Mission Type dictionary
missions = json.load(open('../res/missiontype.json'))
#Solar Nodes Dictionary
locations = json.load(open('../res/solarNodes.json'))

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
        	#Mission Type String
            missionType = "{}".format(missions[alert['MissionInfo']['missionType']]['value'])
            #Location String
            location = "{}".format(locations[alert['MissionInfo']['location']]['value'])
            #Rewardss String
            if(case == 1):
                try:
                    reward = "{}x {}".format(reward['ItemCount'],items[reward['ItemType']])
                except KeyError:
                    pass
            else:
                try:
                    reward = "{}".format(items[reward])
                except KeyError:
                    pass
            
            #Time left String
            millis = int(alert['Expiry']['$date']['$numberLong'])-current_milli_time()
            timeLeft = datetime.datetime.utcfromtimestamp(millis/1000.0)
            if(timeLeft.hour==0):
                msgLeft="{} minutes".format(timeLeft.minute)
            else:
                msgLeft="{} hours {} minutes".format(timeLeft.hour, timeLeft.minute)

            #Color selection
            if(timeLeft.minute<15):
                color = 0xff0000
            elif(timeLeft.minute<30):
                color = 0xf7e10c
            else:
                color = 0x01ff16

            #Assemble message
            embed=discord.Embed(title="Capture", description=location, color=color)
            embed.add_field(name="Reward", value=reward, inline=True)
            embed.add_field(name="Time Remaining", value=msgLeft, inline=True)
            await bot.send_message(channel, embed=embed)
            case = 0
