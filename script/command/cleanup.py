# Perform any cleanup necessary after command resolves
from bge import logic

from script import commandControl, objectControl

# The message sent which causes command results to be displayed
DISPLAY_COMMAND_RESULTS_MESSAGE = 'displayCommandResults'

# Cleanup all variables set while selecting command target
# Also perform any cleanup that happens after an effect resolves
def fromUnitActing():
	# Clear list of spaces that command can target
	logic.globalDict['spaceTarget'] = []
	
	# Clear list of choices for command
	logic.globalDict['commandChoices'] = []

	# Modify the actor's stats
	actor = logic.globalDict['actor']
	actor.stats['act'] -= 1
	consumeSp(actor)

	# Reset extent
	# NOTE(kgeffen) This must happen after sp consumed because
	# sp consumption based on extent
	logic.globalDict['extent'] = 0
	
	# Perform cleanup that happens after every effect resolves
	fromEffectResolving()

	# Change cursor to select a unit to act
	logic.globalDict['cursor'] = 'selecting'

# Perform all cleanup that happens after each effect resolves
def fromEffectResolving():
	# Clear list of previous unit movement
	logic.globalDict['moveLog'] = []

	# Kill any units with hp <= 0
	killDeadUnits()
	
	# Ensure all units stats are within acceptable bounds
	for unit in logic.globalDict['units']:
		ensureStatsWithinBounds(unit.stats)
	
	# Display the results of the command that just resolved
	displayCommandResults()

'''Internal (Private) Methods'''
# Lower unit's sp by cost of command that just resolved
def consumeSp(unit):
	command = logic.globalDict['cursor']
	cost = commandControl.cost(command)
	
	unit.stats['sp'] -= cost

# Remove any units that have hp <= 0
def killDeadUnits():
	# A list of all units that will be deleted
	# NOTE(kgeffen) Wait until after iteration to remove units
	# so that dictionary does not change while being iterated over
	doomedList = []
	for unit in logic.globalDict['units']:
		if unit.stats['hp'] <= 0:
			doomedList.append(unit)
	
	for unit in doomedList:
		unit.die()

# TODO(kgeffen) Remove
# Delete the units entry from all its locations and delete the game object for unit
# def killUnit(unit):
# 	# Delete unit object
# 	unitObject = unitControl.object.get(unit)
# 	unitObject.endObject()

# 	# Remove unit from list of units
# 	unitList = logic.globalDict['units']
# 	unitList = list(filter((unit).__ne__, unitList))
# 	logic.globalDict['units'] = unitList
	
# 	# Update the time data and display to account for deaths
# 	logic.globalDict['time'].remove(unit)

# Update the time array to account for units dying
def updateTime(unit):
	# Remove unit from timeline
	newTime = []
	
	for turn in logic.globalDict['time']:
		newTurn = []

		for group in turn:
			# NOTE(kgeffen) This retains all entries in the array that are != unit
			# Remove unit's existance from current turn
			newGroup = list(filter((unit).__ne__, group))
			
			# Only add group if it isn't empty
			if newGroup != []:
				# Add new tic to new time
				newTurn.append(newGroup)

		newTime.append(newTurn)
	
	# Set time array to newTime, which excludes dead unit's number
	logic.globalDict['time'] = newTime

# Send message displayCommandResults
def displayCommandResults():
	# Ground is arbitrarily the sender
	ground = objectControl.getFromScene('ground', 'battlefield')
	ground.sendMessage(DISPLAY_COMMAND_RESULTS_MESSAGE)

# Ensure hp/sp are not larger than health/spirit
def ensureStatsWithinBounds(unitStats):
	maxSp = unitStats['spirit']
	if unitStats['sp'] > maxSp:
		unitStats['sp'] = maxSp
	
	maxHp = unitStats['health']
	if unitStats['hp'] > maxHp:
		unitStats['hp'] = maxHp
