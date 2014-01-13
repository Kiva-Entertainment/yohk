# Update the onscreen display which shows the cursor's height in decimeters
from bge import logic

from script import objectControl

# TODO(kgeffen) This method only needs to be called when cursor moves,
# currently it is called every tic

HEIGHT_DISPLAY_NAME = 'heightDisplay'
OVERLAY_SCENE_NAME = 'battlefieldOverlay'

def do():
	cursor = objectControl.getFromScene('cursor', 'battlefield')
	cursorHeight = cursor.worldPosition[2]

	heightInDm = round( cursorHeight * 10 )
	
	text = str(heightInDm) + ' dm'
	
	heightDisplay = objectControl.getFromScene(HEIGHT_DISPLAY_NAME, OVERLAY_SCENE_NAME)
	heightDisplay['Text'] = text

