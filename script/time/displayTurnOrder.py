# Display turn order for units
# TODO(kgeffen) This is a wip, when greater artistic vision is reached, update this script
from bge import logic

from script import objectControl

OVERLAY_SCENE_NAME = 'battlefieldOverlay'
# Name of the text object which displays turn order
TURN_ORDER_DISPLAY= 'displayTurnOrder'

MAX_LINES = 30

def do():
	timeline = expectedTimeLine()
	text = formTimelineText(timeline)
	
	# Set the text of the object that displays turn order
	turnDisplay = objectControl.getFromScene(TURN_ORDER_DISPLAY, OVERLAY_SCENE_NAME)
	turnDisplay['Text'] = text

# The timeline that is expected if no units die/have their speed changed
def expectedTimeLine():
	expectedTime = []
	for i in range(101):
		expectedTime.append([])

	time = logic.globalDict['time']

	for turnNum in range(0, len(time)):
		turn = time[turnNum]

		turnHasActors = turn != []
		if turnHasActors:

			for groupNum in range(0, len(turn)):
				group = turn[groupNum]

				for actor in group:
					name = actor['name']

					expectedTime[turnNum].append(name)

					if actor['speed'] > 0:
						nextTurnNum = turnNum + round(100/actor['speed'])

						while nextTurnNum < 100:
							expectedTime[nextTurnNum].append(name)
							nextTurnNum += round(100/actor['speed'])
	return expectedTime

# For each turn with actors, add all of those actors, followed by
# a blank line to communicate which units act on same turn
def formTimelineText(timeline):
	text = ''
	
	# Form full text
	for turn in timeline:

		if turn != []:
			for unit in turn:
				text += unit + '\n'
			text += '\n'

	# Crop to fit max lines
	# NOTE(kgeffen) Even last line has a trailing newline
	if text.count('\n') > MAX_LINES:

		fittingText = ''
		textLines = text.split('\n')
		for i in range(MAX_LINES):
			fittingText += textLines[i] + '\n'

		return fittingText

	return text
