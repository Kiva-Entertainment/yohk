# Move cursor to next space that is a valid choice for current selection
# Ex: To next space that can be targeted if selecting command targets
# Ex: To next unit acting this turn if selecting actor
from bge import logic

from script import check, getPosition, objectControl, commandControl

def attempt(cont):
	fKey = cont.sensors['fKey'].positive
	gKey = cont.sensors['gKey'].positive

	if fKey:
		do(strict = False)
	elif gKey:
		do(strict = True)

def do(strict):
	# What the cursor is doing
	status = logic.globalDict['cursor']
	
	# Cursor is selecting a unit to act/move
	if status == 'selecting':
		toNextActor(strict)

	# Cursor is selecting a space for selected unit to move to
	elif status == 'move':
		toActor()

	# Cursor is selecting a space to target with selected command
	else:
		toNextTargetableSpace()

# Move cursor to selected unit
def toActor():
	actor = logic.globalDict['actor']

	position = getPosition.onGround(actor['position'])

	moveToPosition(position)

# Move cursor to the space where the (next acting unit this turn) is
def toNextActor(strict):
	# Units that act this turn (First turn, first group in turn)
	# NOTE(kgeffen) This relies on current turn always having actors
	actors = logic.globalDict['time'][0][0]

	# Cycle the list of actors until the first actor in list can move/act
	# If strict is True, first actor must have remaining act, not just mv
	# If no units are valid, return
	validUnitExists = cycleUntilFirstUnitActs(actors, strict)
	if not validUnitExists:
		return

	# Position that cursor will move to
	position = getPosition.onGround(actors[0]['position'])
	
	# cursorMoves == True if cursor didn't start at _position_
	cursorMoved = moveToPosition(position)

	# NOTE(kgeffen) If cursor didn't move (was already at position),
	# cycle units once, then get new first unit's position
	if not cursorMoved:

		# Cycle once so fresh entry is chosen
		cycleList(actors)	
		# NOTE(kgeffen) If code has gotten this far, valid unit must exist
		# because last cycle would have returned if not
		cycleUntilFirstUnitActs(actors, strict)
		
		# This is the position of the first unit in newly cycled list of actors
		position = getPosition.onGround(actors[0]['position'])
		
		moveToPosition(position)

	# NOTE(kgeffen) Necessarily cycle each time to ensure that
	# if cursor moves to unit A, then I act with it, move cursor,
	# next time I toNext, the cursor moves to unit B not A
	cycleList(actors)

# Cycle list of units until the first unit in the list can act or move this turn
# If strict is True, first unit must act this turn (Not just mv)
# Ex: strict == false will stop at a unit with 4mv + 0act, strict == true won't
def cycleUntilFirstUnitActs(units, strict):

	# NOTE(kgeffen) For loop runs up to length times, but since list is cycling,
	# first entry of list is always the one being considered
	for i in range(len(units)):

		# Unit is valid if it has remaining actions
		# If not strict, unit can also be valid if unit has remaining mv
		valid = units[0]['act'] > 0
		if not strict:
			valid = valid or units[0]['mv'] > 0

		# If first unit is valid, return true, otherwise, cycle list and try again
		# NOTE(kgeffen) For loop ends after each unit checked, and returns False
		if valid:
			return True
		else:
			cycleList(units)

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
