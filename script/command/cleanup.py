# Perform any cleanup necessary after command resolves
from bge import logic

from script import commandControl, objectControl, unitControl
from script.time import displayTurnOrder 

# The message sent which causes command results to be displayed
DISPLAY_COMMAND_RESULTS_MESSAGE = 'displayCommandResults'

def do():
	# Clear list of spaces that command can target
	logic.globalDict['spaceTarget'] = []
	
	# Modify the actor's stats
	actor = logic.globalDict['actor']
	actor['act'] -= 1
	consumeSp(actor)
	
	# Kill any units with hp <= 0
	killDeadUnits()
	
	# Ensure all units stats are within acceptable bounds
	for unit in logic.globalDict['units']:
		ensureStatsWithinBounds(unit)
	
	# Display the results of the command that just resolved
	displayCommandResults()

# Lower unit's sp by cost of command that just resolved
def consumeSp(unit):
	command = logic.globalDict['cursor']
	cost = commandControl.cost(command)
	
	unit['sp'] -= cost

# Remove any units that have hp <= 0
def killDeadUnits():
	# A list of all units that will be deleted
	# NOTE(kgeffen) Wait until after iteration to remove units
	# so that dictionary does not change while being iterated over
	doomedList = []
	for unit in logic.globalDict['units']:
		if unit['hp'] <= 0:
			doomedList.append(unit)
	
	for unit in doomedList:
		killUnit(unit)

# Delete the units entry from all its locations and delete the game object for unit
def killUnit(unit):
	# Delete unit object
	unitObject = unitControl.object.get(unit)
	unitObject.endObject()

	# Remove unit from list of units
	unitList = logic.globalDict['units']
	unitList = list(filter((unit).__ne__, unitList))
	logic.globalDict['units'] = unitList

	# Update the time data and display to account for deaths
	updateTime(unit)
	displayTurnOrder.do()
	

# Update the time array to account for units dying
def updateTime(unit):
	# Remove unit from timeline
	newTime = []
	
	for tic in logic.globalDict['time']:
		# NOTE(kgeffen) This retains all entries in the array that are != unit
		# Remove unit's existance from current tic
		newTic = list(filter((unit).__ne__, tic))
		
		# Add new tic to new time
		newTime.append(newTic)
	
	# Set time array to newTime, which excludes dead unit's number
	logic.globalDict['time'] = newTime

# Send message displayCommandResults
def displayCommandResults():
	# Ground is arbitrarily the sender
	ground = objectControl.getFromScene('ground', 'battlefield')
	ground.sendMessage(DISPLAY_COMMAND_RESULTS_MESSAGE)

# Ensure hp/sp are not larger than health/spirit
def ensureStatsWithinBounds(unit):
	maxSp = unit['spirit']
	if unit['sp'] > maxSp:
		unit['sp'] = maxSP
	
	maxHp = unit['health']
	if unit['hp'] > maxHp:
		unit['hp'] = maxHp
