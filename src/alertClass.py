import discord
class Alert:

	def __init__(self,missionType,location,reward,timeStart,timeLeft):
		self.missionType=missionType
		self.location=location
		self.reward=reward
		self.timeLeft=setTimeLeft(timeLeft)
		self.booleano,self.timeStart=setTimeStart(timeStart)
		self.color=setColor(timeLeft)

	def changeMessage(self,msg):
		self.msg=msg

	def toEmbed(self):
		embed=discord.Embed(title=self.reward, color=self.color)
		embed.add_field(name=self.missionType, value=self.location, inline=True)
		embed.add_field(name=self.timeStart, value=self.timeLeft if self.booleano else self.timeStart, inline=True)
		return embed	

	def __hash__(self):
		return hash((self.missionType,self.location,self.reward,\
			self.timeStart,self.timeLeft,self.color))

	def __eq__(self,other):
		if not isinstance(other,type(self)): return NotImplemented
		return self.location==other.location and \
			self.missionType==other.missionType


def setColor(timeLeft):
	if(timeLeft.hour<1):
		if(timeLeft.minute<15):
			return 0xff0000
		elif(timeLeft.minute<30):
			return 0xf7e10c
		else:
			return 0x01ff16
	else:
		return 0x01ff16

def setTimeLeft(timeLeft):
	if(timeLeft.hour==0):
		return "{} minutes".format(timeLeft.minute)
	else:
		return "{} hours {} minutes".format(timeLeft.hour, timeLeft.minute)

def setTimeStart(timeStart):
	if(timeStart.minute>=0 and timeStart.second>0):
		return False,"Starts In"
	else:
		return True,"Time Remaining"