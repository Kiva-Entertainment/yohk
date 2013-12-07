# Select the unit that cursor is on, if any
# Display it's basic info and move range
# If it acts this turn, display unit menu
from bge import logic

from script import check, sceneControl, moveRange, objectControl, unitControl

# If a unit is in the same space as cursor, select it
def attempt():
	cursor = objectControl.getFromScene('cursor', 'battlefield')
	cursorPosition = cursor.worldPosition
	
	# Check each unit, if its position matches cursor position, select that unit
	# TODO(kgeffen) Unit lookup should be standardized and more intuitive
	for unit in unitControl.get.allUnits():
		unitPosition = unit['position']
		
		if check.eq2D(cursorPosition, unitPosition):
			do(unit)
			break

def do(unit):
	# While unit is selected, unitMenu is in control, and cursor is waiting
	logic.globalDict['cursor'] = 'wait'
	
	# Set 'selected unit' to the number of the unit being selected
	logic.globalDict['selected'] = unit
	
	# Display and store list of spaces unit can move to
	moveRange.determine.do(unit)
	moveRange.display.do()
	
	# Display basic info about unit
	sceneControl.show('basicInfo')
	
	# Open unitMenu if unit acts this turn
	if unitActsThisTurn(unit):
		displayMenu()


# If unit acts on the current turn
def unitActsThisTurn(unit):
	actorsThisTurn = logic.globalDict['time'][0]
	
	# Return true if unit is one of the actors this turn
	unitActsThisTurn = actorsThisTurn.count(unit) == 1
	if unitActsThisTurn:
		return True

def displayMenu():
	menu = objectControl.getFromScene('unitMenu', 'battlefield')
	objectControl.show(menu)
