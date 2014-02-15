# Deselect the currently selected unit
# Based on that context, different cleanup actions must be performed
# Ex: Context could be deselecting from selecting command target
from bge import logic

from script import sceneControl, marker, objectControl, getPosition, undoMove
from script.cursorSelect import select

def attempt(cont):
	if cont.sensors['wKey'].positive:
		do()

# Handle deselection from different contexts (Choosing target, moving, etc.)
def do():
	# What the cursor is doing currently
	status = logic.globalDict['cursor']
	
	if status == 'move':
		# Selecting a space for unit to move to
		fromUnitMoving()
	
	elif status == 'selecting':
		# Cursor does not have a unit selected
		fromSelectingUnit()
	
	else:
		# Selecting command target
		fromUnitActing()


# <No unit is selected, cursor is searching for unit to selected
# Undo the last move made
def fromSelectingUnit():
	undoMove.attempt()

# <Cursor is selecting a space for unit to move to
# Deselect unit and allow cursor to select another unit
def fromUnitMoving():
	logic.globalDict['cursor'] = 'selecting'
	logic.globalDict['actor'] = None
	logic.globalDict['extent'] = 0
	logic.globalDict['commandChoices'] = []
	
	# NOTE(kgeffen) Clear because movement range markers added when unit is reselected
	marker.clearMoveMarkers()

# <Cursor is selecting a a target for actor's command
# Return cursor to actor, open commandSelect
def fromUnitActing():
	# Clear data about which spaces can be targetted
	logic.globalDict['spaceTarget'] = []
	
	# Reselect the actor
	moveCursorToActor()
	# NOTE(kgeffen) Cursor status must be 'selecting' to select a unit
	logic.globalDict['cursor'] = 'selecting'
	select.do()


def moveCursorToActor():
	cursor = objectControl.getFromScene('cursor', 'battlefield')

	actor = logic.globalDict['actor']

	cursor.worldPosition = actor.position
