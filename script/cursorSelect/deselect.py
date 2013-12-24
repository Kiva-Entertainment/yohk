# Deselect the currently selected unit
# Based on that context, different cleanup actions must be performed
# Ex: Context could be deselecting from selecting command target
from bge import logic

from script import sceneControl, marker, objectControl, getPosition, undoMove
from script.cursorSelect import select

def attempt(cont):
	# NOTE(kgeffen) sensor 'xKey' belongs to timeControl
	# To avoid unintuive implementation detail, it is connected to
	# cursorSelection controller that calls this script instead
	# of churn.py calling deselect.do()
	if cont.sensors['xKey'].positive:
		do(turnChanging = True)
	elif cont.sensors['wKey'].positive:
		do()

# Handle deselection from different contexts (Choosing target, moving, etc.)
def do(turnChanging = False):
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
		fromUnitActing(turnChanging)


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
# If deselect caused by turn ending, don't move cursor
def fromUnitActing(turnChanging):
	if not turnChanging:
		moveCursorToActor()
	
	# Clear data about which spaces can be targetted
	logic.globalDict['spaceTarget'] = []
	
	# NOTE(kgeffen) Cursor status must be 'selecting' to select a unit
	logic.globalDict['cursor'] = 'selecting'
	select.do()


def moveCursorToActor():
	cursor = objectControl.getFromScene('cursor', 'battlefield')

	actor = logic.globalDict['actor']

	cursor.worldPosition = getPosition.onGround(actor['position'])
