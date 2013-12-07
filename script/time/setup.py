# Create starting time array

# Called from setup.py
from bge import logic

from script.time import addNext, churn, displayTurnOrder

# Number of entries in time array
QUANTITY_ENTRIES = 100

# Create and populate the time array
# Ensure that it starts on a turn with actor(s)
def do():
	timeArray = createStartingTimeArray()
	
	logic.globalDict['time'] = timeArray
	
	# Ensure time starts with a turn that has actors
	noActors = logic.globalDict['time'][0] == []
	if noActors:
		churn.do()


# Create starting timeArray, complete with each unit's first action
def createStartingTimeArray():
	timeArray = []
	
	# Give timeArray appropriate number of entries
	for i in range(0, QUANTITY_ENTRIES):
		timeArray.append([])
	
	# Add each unit's first action to timeArray
	for unit in logic.globalDict['units']:
		addNext.unitAction(unit, timeArray)
	
	return timeArray
