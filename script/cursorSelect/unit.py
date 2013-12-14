# Select the unit that cursor is on if that unit acts currently
# Display its move range and unit menu
from bge import logic

from script import check, moveRange, objectControl

def attempt():
	cursor = objectControl.getFromScene('cursor', 'battlefield')
	cursorPosition = cursor.worldPosition
	
	# Check each unit, if its position matches cursor position,
	# and it acts this turn, select that unit
	for unit in logic.globalDict['units']:
		
		if check.eq2D(cursorPosition, unit['position']):
			if unitActsThisTurn(unit):

				do(unit)
				break

def do(unit):
	# While unit is selected, unitMenu is in control, and cursor is waiting
	logic.globalDict['cursor'] = 'wait'
	
	# Set 'selected unit' to the number of the unit being selected
	logic.globalDict['actor'] = unit
	
	# Display and store list of spaces unit can move to
	moveRange.determine.do(unit)
	moveRange.display.do()
	
	# Open unitMenu
	displayMenu()


# Return true if unit acts this turn in first group (Turns seperated into groups by alignment)
def unitActsThisTurn(unit):
	currentActors = logic.globalDict['time'][0][0]
	
	# Return true if unit is one of the actors this turn
	unitActsThisTurn = currentActors.count(unit) == 1
	if unitActsThisTurn:
		return True

def displayMenu():
	menu = objectControl.getFromScene('unitMenu', 'battlefield')
	objectControl.show(menu)
