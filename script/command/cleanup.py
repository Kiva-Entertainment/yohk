# Perform any cleanup necessary after command resolves
from bge import logic

from script import commandControl, objectControl
from script.time import displayTurnOrder 

# The message sent which causes command results to be displayed
DISPLAY_COMMAND_RESULTS_MESSAGE = 'displayCommandResults'

def do():
	# Clear list of spaces that command can target
	logic.globalDict['spaceTarget'] = []
	
	# Modify the actor's stats
	actor = logic.globalDict['selected']
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
	for unit in logic.globalDict['units']:
		if unit['hp'] <= 0:
			killUnit(unit)
def killUnit(unit):
	# Remove unit from list of units (Set its entry to 'None')
	unitList = logic.globalDict['units']
	for i in range(0, unitList):
		if unitList[i] == unit:
			unitList[i] = None

	# Update the time data and display to account for deaths
	updateTime(unitNumber)
	displayTurnOrder.do()
	
	# Delete unit object
	unitObject = objectControl.getUnit(unit)
	unitObject.endObject()

# Update the time array to account for units dying
def updateTime(unit):
	# Remove unit from timeline
	newTime = []
	
	for tic in logic.globalDict['time']:
		# NOTE(kgeffen) This retains all entries in the array that are != unitNumber
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
