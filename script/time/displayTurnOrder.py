# Display turn order for units
# TODO(kgeffen) This is a wip, when greater artistic vision is reached, update this script
from bge import logic

from script import objectControl

OVERLAY_SCENE_NAME = 'battlefieldOverlay'
# Name of the text object which displays turn order
TURN_ORDER_DISPLAY= 'displayTurnOrder'

def do():
	text = formDisplayedText()
	
	# Set the text of the object that displays turn order
	turnDisplay = objectControl.getFromScene(TURN_ORDER_DISPLAY, OVERLAY_SCENE_NAME)
	turnDisplay['Text'] = text


# For each turn with actors, add all of those actors, followed by
# a blank line to communicate which units act on same turn
def formDisplayedText():
	text = ''
	
	for turn in logic.globalDict['time']:

		turnHasActors = turn != []
		if turnHasActors:

			# Add name of each actor in turn
			for actor in turn:
				text += actor['name'] + '\n'
			
			# Follow (turn with actors) with a blank line
			text += '\n'
	
	return text
