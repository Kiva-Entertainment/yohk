# Move cursor to next space that is a valid choice for current selection
# Ex: To next space that can be targeted if selecting command targets
# Ex: To next unit acting this turn if selecting actor
from bge import logic

from script import check, getPosition, objectControl

def attempt(cont):
	if cont.sensors['fKey'].positive:
		do()

def do():
	# What the cursor is doing
	status = logic.globalDict['cursor']
	
	selectingActor = status == 'selecting'
	selectingCommandTarget = status != 'wait' and status != 'move'

	if selectingActor:
		toNextActor()
	
	elif selectingCommandTarget:
		toNextTargetableSpace()


# Move cursor to the space where the (next acting unit this turn) is
def toNextActor():
	# Actors are grouped based on alignment
	groups = logic.globalDict['time'][0]
	if groups != []:

		actors = groups[0]
		if actors != []:
			# Position that cursor will move to
			position = getPosition.onGround(actors[0]['position'])
			
			# Cursor moved (Wasn't already in position)
			cursorMoved = moveToPosition(position)
			
			# NOTE(kgeffen) If cursor didn't move (is already at position),
			# cycle actors once, then get new first unit's position
			if not cursorMoved:
				cycleEntries(actors)
				
				# This is the position of the newly cycled list of actors
				position = getPosition.onGround(actors[0]['position'])
				
				moveToPosition(position)

# Move cursor to next space that could be selected as command target
# TODO(kgeffen) Moves to any space in range, even if that space is not a valid target
# Ex: lance can hit faraway spaces, but not if they are empty.
# Currently moves to them even if don't they contain units.
# This can be fixed fairly easily, but deal with after commands that target empty space
# Ex: Create a rock on an empty space
# Have been made to know best way to deal with
def toNextTargetableSpace():
	targets = logic.globalDict['spaceTarget']
	
	if targets != []:
		# Cursor moved (Wasn't already in position)
		cursorMoved = moveToPosition(targets[0]['space'])
		
		# NOTE(kgeffen) If cursor is already at position (Didn't move),
		# cycle targets once, then get new first target's position
		if cursorMoved == False:
			cycleEntries(targets)
			
			# Move to newly cycled first entry in list of spaces
			moveToPosition(targets[0]['space'])

# Move cursor to position of first entry in list of unitNumbers
# If cursor is already there, return False to say that no movement occured
def moveToPosition(position):
	cursor = objectControl.getFromScene('cursor', 'battlefield')
	
	cursorAlreadyInPosition = check.eq2D(position, cursor.worldPosition)
	if cursorAlreadyInPosition:
		return False # Movement did not happen
	
	else:
		cursor.worldPosition = position
		
		return True # Movement happened

def cycleEntries(list):
	entry = list.pop(0)
	list.append(entry)
