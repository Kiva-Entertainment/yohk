# Setup cursor to be on ground (Not at 0 height)
from script import getPosition, objectControl

def do():
	cursor = objectControl.getFromScene('cursor', 'battlefield')
	
	# Raise/lower cursor to be directly on top of ground
	cursor.worldPosition = getPosition.onGround(cursor.worldPosition)
