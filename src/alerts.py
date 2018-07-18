import time
import datetime
import json
import asyncio
import discord
from alertClass import *

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

ongoing = list()

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
            missionType = missions[alert['MissionInfo']['missionType']]['value']
            #Location String
            location = locations[alert['MissionInfo']['location']]['value']
            #Rewardss String
            if(case == 1):
                try:
                    reward = "{}x {}".format(reward['ItemCount'],items[reward['ItemType']])
                except KeyError:
                    pass
            else:
                try:
                    reward = items[reward]
                except KeyError:
                    pass

            #Time start String
            millis = int(alert['Activation']['$date']['$numberLong'])-current_milli_time()
            millis = millis if millis>0 else 0
            timeStart = datetime.datetime.utcfromtimestamp(millis/1000.0)

            #Time left String
            millis = int(alert['Expiry']['$date']['$numberLong'])-current_milli_time() 
            timeLeft = datetime.datetime.utcfromtimestamp(millis/1000.0)

            actualAlert = Alert(missionType,location,reward,timeStart,timeLeft)
            
            if(actualAlert not in ongoing):
                msg = await bot.send_message(channel, embed=actualAlert.toEmbed())
            else:
                oldAlert = ongoing.pop(ongoing.index(actualAlert))
                if(millis>0):
                    msg = await bot.edit_message(oldAlert.msg, embed=actualAlert.toEmbed())
                else:
                    await bot.delete_message(oldAlert.msg)
            	
            actualAlert.changeMessage(msg)
            if(millis>0):
                ongoing.append(actualAlert)
