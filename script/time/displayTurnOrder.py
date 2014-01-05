# Display turn order for units
# TODO(kgeffen) This is a wip, when greater artistic vision is reached, update this script
from bge import logic

from script import objectControl, alignControl, dynamicMaterial

OVERLAY_SCENE_NAME = 'battlefieldOverlay'
# Name of the text object which displays turn order
TURN_ORDER_DISPLAY= 'displayTurnOrder'

# The greatest number of lines to display for timeline
MAX_LINES = 40

ALIGN_ICON_OBJECT_NAME = 'currentTurnAlignDisplay'

def do():
	timeline = expectedTimeLine()
	text = formTimelineText(timeline)
	
	# Set the text of the object that displays turn order
	turnDisplay = objectControl.getFromScene(TURN_ORDER_DISPLAY, OVERLAY_SCENE_NAME)
	turnDisplay['Text'] = text

	# Display the icon of whichever alignment is acting currently
	displayCurrentAlignIcon()

# The timeline that is expected if no units die/have their speed changed
def expectedTimeLine():
	expectedTime = []
	# NOTE(kgeffen) Only go to 30 because that allows for 2 instances of bases acting in timeline.
	# This entire module is temporary, and just has to serve until the next version release.
	for i in range(30):
		expectedTime.append([[], []])

	time = logic.globalDict['time']

	for turnNum in range(0, len(expectedTime)):
		turn = time[turnNum]

		turnHasActors = turn != []
		if turnHasActors:

			for groupNum in range(0, len(turn)):
				group = turn[groupNum]

				for unit in group:

					if unit['speed'] > 0:
						# The number for a turn that the unit acts on, is incremented below
						turnUnitActsOn = turnNum

						while turnUnitActsOn < 30:
							# NOTE(kgeffen) This is scaffolding that relies on solarServants going before
							# martialLegion. Time + time display will be changed in next release, so
							# scaffolding is acceptable.
							# IOW: It's a hack, but it's okay because it will disappear soon
							if unit['align'] == 'martialLegion':
								expectedTime[turnUnitActsOn][1].append(unit['name'])
							else: # solarServants
								expectedTime[turnUnitActsOn][0].append(unit['name'])
							
							turnUnitActsOn += round(100/unit['speed'])
	return expectedTime

# For each turn with actors, add all of those actors, followed by
# a blank line to communicate which units act on same turn
def formTimelineText(timeline):
	text = ''
	
	# Form full text
	for turn in timeline:

		for group in turn:

			if group != []:
				for unit in group:
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


# Display the icon of whichever alignment is acting currently
def displayCurrentAlignIcon():
	firstTurn = logic.globalDict['time'][0]

	if firstTurn != []:
		align = firstTurn[0][0]['align']

		filename = alignControl.icon(align)
		path = logic.expandPath('//images/icons/' + filename)
	
		dynamicMaterial.switchMaterialsImage(path, ALIGN_ICON_OBJECT_NAME)
