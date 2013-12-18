# Call other select modules based on what type of selection is being made
# Ex: Command target, space to move to, unit to inspect/act
from bge import logic

from script import cursorSelect, sceneControl, objectControl, check, marker

def attempt(cont):
	spaceKey = cont.sensors['spaceKey'].positive
	messaged = cont.sensors['selectMessage'].positive
	
	if spaceKey or messaged:
		do()

def do():
	cursor = objectControl.getFromScene('cursor', 'battlefield')
	cursorPosition = cursor.worldPosition

	# The type of selection being made
	status = logic.globalDict['cursor']
	
	if status == 'selecting':
		cursorSelect.unit.attempt(cursorPosition)
	
	elif status == 'move':
		# NOTE(kgeffen) When user is selecting a space to move unit,
		# is user selects unit, commandSelect opens
		unitPosition = logic.globalDict['actor']['position']

		# If cursor is not over unit, move unit to space cursor is on
		if not check.eq2D(cursorPosition, unitPosition):
			cursorSelect.move.attempt(cursorPosition)
		# Else, open commandSelect screen
		else:
			openCommandSelect()

	elif status != 'wait':
		# Selecting the target for a command
		cursorSelect.target.attempt(cursorPosition)


def openCommandSelect():
	# Clear all movement range markers
	marker.clearMoveMarkers()
		
	sceneControl.show('commandSelect')
	sceneControl.hide('battlefieldOverlay')
	sceneControl.suspend('battlefield') # Battlefield is still visible
