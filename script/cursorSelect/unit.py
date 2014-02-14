# Select the unit that cursor is on if that unit acts currently
# Display its move range and unit menu
from bge import logic

from script import moveRange, objectControl, common

def attempt(position):
	# Get unit in given space
	unit = common.unitInSpace(position)
	
	if unit is not None and unitActsThisTurn(unit):
		do(unit)

def do(unit):
	# Unit can now select a space to move to
	logic.globalDict['cursor'] = 'move'
	
	# Set unit selected as the current actor
	logic.globalDict['actor'] = unit
	
	# Display and store list of spaces unit can move to
	moveRange.determine.do(unit)
	moveRange.display.do()

# Return true if unit acts this turn in first group (Turns seperated into groups by alignment)
def unitActsThisTurn(unit):
	currentActors = logic.globalDict['time'][0][0]
	
	# Return true if unit is one of the actors this turn
	unitActsThisTurn = currentActors.count(unit) == 1
	if unitActsThisTurn:
		return True
