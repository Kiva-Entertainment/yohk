# Deselect the currently selected unit
# Based on that context, different cleanup actions must be performed
# Ex: Context could be deselecting from selecting command target
from bge import logic

from script import sceneControl, marker, objectControl, getPosition
from script.cursor.select import select

def attempt(cont):
	# NOTE(kgeffen) sensor 'xKey' belongs to timeControl
	# To avoid unintuive implementation detail, it is connected to
	# cursorSelection controller that calls this script instead
	# of churn.py calling deselect.do()
	if cont.sensors['wKey'].positive or cont.sensors['xKey'].positive:
		do()

# Handle deselection from different contexts (Choosing target, moving, etc.)
def do():
	# What the cursor is doing currently
	status = logic.globalDict['cursor']
	
	if status == 'wait':
		# Unit is selected and unitMenu is open
		fromUnitSelected()
	
	elif status == 'move':
		# Selecting a space for unit to move to
		fromUnitMoving()
	
	elif status == 'selecting':
		# Selecting a unit
		pass
	
	else:
		# Selecting command target
		fromUnitActing()


# <Unit is selected and unit menu is open
# Return to selecting a unit (Close unit menu)
def fromUnitSelected():
	logic.globalDict['cursor'] = 'selecting'
	logic.globalDict['actor'] = None
	logic.globalDict['extent'] = 0
	logic.globalDict['commandChoices'] = []
	
	# Clear movement range markers
	marker.clearMoveMarkers()
	
	sceneControl.hide('basicInfo')
	
	# Hide unitMenu
	menu = objectControl.getFromScene('unitMenu', 'battlefield')
	objectControl.hide(menu)

# <Cursor is selecting a space for unit to move to
# Return cursor to actor, open unit menu
def fromUnitMoving():
	moveCursorToActor()
	
	# NOTE(kgeffen) Clear because movement range markers added when unit is reselected
	marker.clearMoveMarkers()
	
	# NOTE(kgeffen) Cursor status must be 'selecting' to select a unit
	logic.globalDict['cursor'] = 'selecting'
	select.do()

# <Cursor is selecting a a target for actor's command
# Return cursor to actor, open commandSelect
def fromUnitActing():
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
