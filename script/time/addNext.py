# Add unit to timeArray at next turn when unit acts
# Units act sooner/more often if they have higher speed
from bge import logic

def unitAction(unit, timeArray):
	firstTurn = 100 - unit['speed']
	
	timeArray[firstTurn].append(unit)
