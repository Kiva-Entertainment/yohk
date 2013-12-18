# Move cursor to next space that is a valid choice for current selection
# Ex: To next space that can be targeted if selecting command targets
# Ex: To next unit acting this turn if selecting actor
from bge import logic

from script import check, getPosition, objectControl, commandControl

def attempt(cont):
	if cont.sensors['fKey'].positive:
		do()

def do():
	# What the cursor is doing
	status = logic.globalDict['cursor']
	
	selectingActor = status == 'selecting'
	# TODO(kgeffen) Status should be 'command' instead of the specific command
	# and seperate gd should exist for which command
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
				cycleList(actors)
				
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

		# Cycle list until first entry is a valid target for command
		validTargetExists = cycleUntilValidTarget(targets)
		if not validTargetExists:
			return

		# Position that cursor will move to
		position = getPosition.onGround(targets[0]['space'])

		# Cursor moved (Wasn't already in position)
		cursorMoved = moveToPosition(position)
		
		# NOTE(kgeffen) If cursor is already at position (Didn't move),
		# cycle targets at least once, then get new first target's position
		if cursorMoved == False:
			# Cycle once so fresh entry is chosen
			cycleList(targets)
			# Cycle until valid target is found
			cycleUntilValidTarget(targets)
			
			# Move to newly cycled first entry in list of spaces
			position = getPosition.onGround(targets[0]['space'])

			moveToPosition(position)

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

# Cycle the given list until first entry is valid target for command
def cycleUntilValidTarget(targets):
	commandName = logic.globalDict['cursor']
	# If command can only be performed if it targets units
	# Conversely, if requiresUnits is False, command MUST not target any units
	requiresUnits = commandControl.hasTag(commandName, 'targets')

	# NOTE(kgeffen) For loop runs up to length times, but since targets list is cycling,
	# first entry of targets is always the one being considered
	for i in range(len(targets)):

		# If no units are hit for first entry in targets
		if targets[0]['units'] == []:
			if requiresUnits:
				cycleList(targets)
			else:
				return True
		else:
			if requiresUnits:
				return True
			else:
				cycleList(targets)

def cycleList(list):
	entry = list.pop(0)
	list.append(entry)
