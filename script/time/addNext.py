# Add unit's number to timeArray at next turn when unit acts
# Units act sooner/more often if they have higher speed
from bge import logic

def unitAction(unitNumber, timeArray):
	unitData = logic.globalDict['units'][unitNumber]
	speed = unitData['speed']
	
	firstTurn = 100 - speed
	
	timeArray[firstTurn].append(unitNumber)
