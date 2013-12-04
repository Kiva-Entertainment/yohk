# Update the onscreen display which shows the cursor's height in decimeters
from bge import logic

from script import objectControl

HEIGHT_DISPLAY_NAME = 'heightDisplay'
OVERLAY_SCENE_NAME = 'battlefieldOverlay'

def do(height):
	heightInDm = round( height * 10 )
	
	text = str(heightInDm) + ' dm'
	
	heightDisplay = objectControl.getFromScene(HEIGHT_DISPLAY_NAME, OVERLAY_SCENE_NAME)
	heightDisplay['Text'] = text

