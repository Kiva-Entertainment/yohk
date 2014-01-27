# Display the timeline
from bge import logic

from script import objectControl

# TODO(kgeffen) This method only needs to be called when time changes,
# currently it is called every tic

TIME_DISPLAY_NAME = 'timeDisplay'
OVERLAY_SCENE_NAME = 'battlefieldOverlay'
MAX_LINES = 40

def do():
	text = logic.globalDict['time'].asString()

	# Only display first N lines of text
	croppedText = ''
	for line in text.split('\n'):

		# If text has less lines than max, add another line
		if croppedText.count('\n') <= MAX_LINES:
			croppedText += line + '\n'
		else:
			break

	timeDisplay = objectControl.getFromScene(TIME_DISPLAY_NAME, OVERLAY_SCENE_NAME)
	timeDisplay['Text'] = croppedText
