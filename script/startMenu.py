# Control everything that happens in the start menu
from bge import logic, events

from script import objectControl

ACTIVE = logic.KX_INPUT_JUST_ACTIVATED
# Distance in height between one field and the next
D_HEIGHT = 0.1
# A list of all fields by number
FIELDS = ['stage', 'characters', 'goal', 'players', 'start']

def update(cont):
	own = cont.owner
	keyboard = logic.keyboard
	
	if keyboard.events[events.UPARROWKEY] == ACTIVE:
		moveVertical(own, up = True)
	elif keyboard.events[events.DOWNARROWKEY] == ACTIVE:
		moveVertical(own, up = False)

# Move cursor to next selection up/down
def moveVertical(own, up):
	if up:
		# Move up unless at top, otherwise loop to bottom
		if own['fieldNum'] != 0:
			own.worldPosition.y += D_HEIGHT
			own['fieldNum'] -= 1

		else:
			# How many fields own must move down to get to bottom
			movesDown = len(FIELDS) - 1

			own.worldPosition.y -= D_HEIGHT * movesDown
			own['fieldNum'] = movesDown

	else:
		# Move down unless at bottom, otherwise loop to top
		if own['fieldNum'] != len(FIELDS) - 1:
			own.worldPosition.y -= D_HEIGHT
			own['fieldNum'] += 1

		else:
			# How many fields own must move up to get to top
			movesUp = len(FIELDS) - 1

			own.worldPosition.y += D_HEIGHT * movesUp
			own['fieldNum'] = 0

	# Reset all fields to black/Ensure arrows visible
	for field in FIELDS:
		objectControl.getFromScene('text_' + field, 'main').color = (0, 0, 0, 1)
	
	# Make selected field white
	field = FIELDS[ own['fieldNum'] ]
	objectControl.getFromScene('text_' + field, 'main').color = (1, 1, 1, 1)

	# If selection is start button, make arrows invisible
	if field == 'start':
		objectControl.getFromScene('leftArrow', 'main').setVisible(False)
		objectControl.getFromScene('rightArrow', 'main').setVisible(False)
	else:
		objectControl.getFromScene('leftArrow', 'main').setVisible(True)
		objectControl.getFromScene('rightArrow', 'main').setVisible(True)
