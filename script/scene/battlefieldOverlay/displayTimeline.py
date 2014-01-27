# Display the timeline
from bge import logic

from script import objectControl

# TODO(kgeffen) This method only needs to be called when time changes,
# currently it is called every tic

TIME_DISPLAY_NAME = 'timeDisplay'
OVERLAY_SCENE_NAME = 'battlefieldOverlay'

def do():
	text = logic.globalDict['time'].asString()

	timeDisplay = objectControl.getFromScene(TIME_DISPLAY_NAME, OVERLAY_SCENE_NAME)
	timeDisplay['Text'] = text
