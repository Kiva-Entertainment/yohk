# Basic cursor movement based on which keys are pressed
# Motion is cardinal (up, down, left, right)
from bge import logic, events
from mathutils import Vector

from script import getPosition, objectControl
from script.cursor.motion import updateHeightDisplay

def attempt():
	movementAllowed = not logic.globalDict['cursor'] == 'wait'
	if movementAllowed:
		do()

def do():
	cursor = objectControl.getFromScene('cursor', 'battlefield')
	
	# Get the new position that cursor should move
	position = getNewPosition(cursor)
	cursor.worldPosition = position
	
	# Display position
	height = position[2]
	updateHeightDisplay.do(height)


# Get the position that the cursor is moving to
def getNewPosition(cursor):
	'Calculate the potential global position'
	rotation = cursor.orientation
	
	# Displacement in local terms (Before taking rotation into consideration)
	localDisplacement = getDisplacement()
	
	# Displacement in global terms
	globalDisplacement = rotation * localDisplacement
	
	# New position is current position plus displacement
	position = cursor.worldPosition + globalDisplacement
	
	'Adjust position to be correct height/On map (Wrap to other side of map if necessary)'
	position = getPosition.onMap(position)
	position = getPosition.onGround(position)
	
	return position

# Get local displacement caused by keypress
def getDisplacement():
	direction = getKeyPressed()
	
	dict = {'none' : Vector((0.0, 0.0, 0.0)),
			'multiple' : Vector((0.0, 0.0, 0.0)),
			'up' : Vector((0.0, 1.0, 0.0)),
			'left' : Vector((-1.0, 0.0, 0.0)),
			'down' : Vector((0.0, -1.0, 0.0)),
			'right' : Vector((1.0, 0.0, 0.0))}
	
	return dict[direction]

# Determine which directional keys were pressed
def getKeyPressed():
	keyboard = logic.keyboard
	
	upKey = logic.KX_INPUT_ACTIVE == keyboard.events[events.UPARROWKEY]
	leftKey = logic.KX_INPUT_ACTIVE == keyboard.events[events.LEFTARROWKEY]
	downKey = logic.KX_INPUT_ACTIVE == keyboard.events[events.DOWNARROWKEY]
	rightKey = logic.KX_INPUT_ACTIVE == keyboard.events[events.RIGHTARROWKEY]
	
	if upKey + leftKey + downKey + rightKey > 1:
		return 'multiple'
	elif upKey:
		return 'up'
	elif leftKey:
		return 'left'
	elif downKey:
		return 'down'
	elif rightKey:
		return 'right'
	else:
		return 'none'

