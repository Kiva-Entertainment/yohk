# Perform any cleanup necessary after command resolves
from bge import logic

from script import unitControl, commandControl, objectControl
from script.time import displayTurnOrder 

# The message sent which causes command results to be displayed
DISPLAY_COMMAND_RESULTS_MESSAGE = 'displayCommandResults'

def do():
	# Clear list of spaces that command can target
	logic.globalDict['spaceTarget'] = []
	
	# Modify the actor's stats
	actor = unitControl.get.actor()
	consumeAction(actor)
	consumeSp(actor)
	
	# Kill any units with hp <= 0
	killDeadUnits()
	
	# Ensure all units stats are within acceptable bounds
	for unitNumber in logic.globalDict['units'].keys():
		ensureStatsWithinBounds(unitNumber)
	
	# Display the results of the command that just resolved
	displayCommandResults()

# Lower unit's remaining actions by 1
def consumeAction(unit):
	logic.globalDict['units'][unit['number']]['act'] -= 1

# Lower unit's sp by cost of command that just resolved
def consumeSp(unit):
	command = logic.globalDict['cursor']
	cost = commandControl.cost(command)
	
	logic.globalDict['units'][unit['number']]['sp'] -= cost

# Remove any units that have hp <= 0
def killDeadUnits():
	# NOTE(kgeffen) Wait until after iteration to remove units
	# so that dictionary does not change while being iterated over
	
	unitsToKill = [] # list of unitNumbers
	for unit in logic.globalDict['units'].items():
		if unit[1]['hp'] <= 0:
			unitsToKill.append(unit[0])
	
	for unitNumber in unitsToKill:
		killUnit(unitNumber)

def killUnit(unitNumber):
	# Delete unit from dictionary
	del logic.globalDict['units'][unitNumber]
	
	# Update the time data and display to account for deaths
	updateTime(unitNumber)
	displayTurnOrder.do()
	
	# Delete unit object
	unitObject = objectControl.getFromScene(str(unitNumber), 'battlefield')	
	unitObject.endObject()

# Update the time array to account for units dying
def updateTime(unitNumber):
	# Remove unit from timeline
	newTime = []
	
	for tic in logic.globalDict['time']:
		# NOTE(kgeffen) This retains all entries in the array that are != unitNumber
		# Remove unit's existance from current tic
		newTic = list(filter((unitNumber).__ne__, tic))
		
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
def ensureStatsWithinBounds(unitNumber):
	sp = logic.globalDict['units'][unitNumber]['sp']
	maxSp = logic.globalDict['units'][unitNumber]['spirit']
	if sp > maxSp:
		logic.globalDict['units'][unitNumber]['sp'] = maxSp
	
	hp = logic.globalDict['units'][unitNumber]['hp']
	maxHp = logic.globalDict['units'][unitNumber]['health']
	if hp > maxHp:
		logic.globalDict['units'][unitNumber]['hp'] = maxHp
