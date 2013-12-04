# Adjust cursor's height so that it is on ground
# Cursor starts at height 0 and moves up to height of ground at space (0,0)
# Called on second tic in battlefield setup
from bge import logic

from script.cursor.motion import updateHeightDisplay
from script import getPosition, objectControl

def do():
	cursor = objectControl.getFromScene('cursor', 'battlefield')
	
	# Raise/lower cursor to be directly on top of ground
	cursor.worldPosition = getPosition.onGround(cursor.worldPosition)
	
	# Update the displayed height
	newHeight = cursor.worldPosition[2]
	updateHeightDisplay.do(newHeight)

