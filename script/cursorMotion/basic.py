# Move the cursor in one of the cardinal directions 1 space
# Movement based on which keys are pressed
# Cursor moves only if just one of directional keys is pressed
from bge import logic, events
from mathutils import Vector

from script import getPosition, objectControl

# The number of game tics to wait between cursor movement if user if
# holding down key
WAIT_TIME = 6

def attempt(cont):
	# Wait time is the number of game tics that occur between cardinal movement
	waitTime = cont.owner['waitTime']

	cursor = objectControl.getFromScene('cursor', 'battlefield')

	offset = getOffset()

	# If cursor isn't trying to move, keys have been released and wait time should reset
	# to allow user to move by tapping directionals
	if offset is None:
		waitTime = 0

	else:
		# If cursor must wait before it can move, wait and decrement the wait time
		if waitTime > 0:
			waitTime -= 1
		else:
			do(cursor, offset)
			# Reset timer till cursor can move again
			waitTime = WAIT_TIME

	# Reassign new waitime to owner's property
	cont.owner['waitTime'] = waitTime

def do(cursor, offset):
	position = getNewPosition(cursor, offset)
	cursor.worldPosition = position

# Get cursor's offset caused by keystroke
# If multiple or no keys are being pressed, return None
# Otherwise, return a unit vector in the direction of the key pressed
def getOffset():
	keyboard = logic.keyboard
	
	# Determine which keys are active
	upKey = logic.KX_INPUT_ACTIVE == keyboard.events[events.UPARROWKEY]
	leftKey = logic.KX_INPUT_ACTIVE == keyboard.events[events.LEFTARROWKEY]
	downKey = logic.KX_INPUT_ACTIVE == keyboard.events[events.DOWNARROWKEY]
	rightKey = logic.KX_INPUT_ACTIVE == keyboard.events[events.RIGHTARROWKEY]
	
	offset = Vector((0.0, 0.0, 0.0))
	
	if upKey:
		offset += Vector((0.0, 1.0, 0.0))

	if leftKey:
		offset += Vector((-1.0, 0.0, 0.0))

	if downKey:
		offset += Vector((0.0, -1.0, 0.0))

	if rightKey:
		offset += Vector((1.0, 0.0, 0.0))

	# Return the offset, unless it is nothing
	if offset != Vector((0.0, 0.0, 0.0)):
		return offset

# Get the position that cursor is moving to
def getNewPosition(cursor, offset):
	'Calculate the potential global position'
	rotation = cursor.orientation
	
	# Displacement in local terms (Before taking rotation into consideration)
	localDisplacement = offset
	
	# Displacement in global terms
	globalDisplacement = rotation * localDisplacement
	
	# New position is current position plus displacement
	position = cursor.worldPosition + globalDisplacement
	
	'Adjust position to be on map (Wrap to other side of map if necessary)'
	position = getPosition.onMap(position)
	
	return position
