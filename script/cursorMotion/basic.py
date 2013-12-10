# Move the cursor in one of the cardinal directions 1 space
# Movement based on which keys are pressed
# Cursor moves only if just one of directional keys is pressed
from bge import logic, events
from mathutils import Vector

from script import getPosition, objectControl

def attempt():
	cursor = objectControl.getFromScene('cursor', 'battlefield')

	offset = getOffset()

	if cursor['moveable']:
		if offset is not None:
			do(cursor, offset)

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
	
	# Return unit vector or None based on which key(s) are pressed
	if upKey + leftKey + downKey + rightKey > 1:
		return None

	elif upKey:
		return Vector((0.0, 1.0, 0.0))

	elif leftKey:
		return Vector((-1.0, 0.0, 0.0))

	elif downKey:
		return Vector((0.0, -1.0, 0.0))

	elif rightKey:
		return Vector((1.0, 0.0, 0.0))

	else:
		return None

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
