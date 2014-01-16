# Control everything that happens in the start menu
from bge import logic, events
from mathutils import Vector
import copy, os

from script import objectControl, soundControl

ACTIVE = logic.KX_INPUT_JUST_ACTIVATED
# Distance in height between one field and the next
D_HEIGHT = 0.1
# A list of all fields by number
FIELDS = ['stages', 'party1', 'party2', 'players', 'start']

# List of valid choices for 'players'
PLAYERS = ['Single Player', 'Two Player']

def setup(cont):
	own = cont.owner

	if cont.sensors['start'].positive:
		logic.globalDict['mute'] = False

		# Get list of names of all stages
		stagesDir = logic.expandPath('//stages')
		stageNames = [x[1] for x in os.walk(stagesDir)][0]
		own['stages'] = stageNames

		setupParties(own)
		
		own['players'] = PLAYERS

def update(cont):
	own = cont.owner
	keyboard = logic.keyboard
	
	# Display each field's current choice
	for field in FIELDS:
		# Start is a button, not a field
		if field != 'start':
			obj = objectControl.getFromScene('text_' + field, 'main')
			obj.text = own[field][0]

	# Scale down the arrows if they are enlarged
	for arrowName in ['leftArrow', 'rightArrow']:
		arrow = objectControl.getFromScene(arrowName, 'main')
		if arrow.localScale.x > 1:
			arrow.localScale -= Vector((0.035, 0.035, 0.035))

	if keyboard.events[events.MKEY] == ACTIVE:
		soundControl.toggleMute()

	elif keyboard.events[events.UPARROWKEY] == ACTIVE:
		moveVertical(own, up = True)
	elif keyboard.events[events.DOWNARROWKEY] == ACTIVE:
		moveVertical(own, up = False)

	elif keyboard.events[events.LEFTARROWKEY] == ACTIVE:
		moveHorizontal(own, left = True)
	elif keyboard.events[events.RIGHTARROWKEY] == ACTIVE:
		moveHorizontal(own, left = False)

	elif keyboard.events[events.SPACEKEY] == ACTIVE:
		select(own)

# Refresh the list of parties that can be chosen
# Called after partyCreate screen has added/removed a party
def refreshParties(cont):
	if cont.sensors[0].positive:
		setupParties(cont.owner)

def setupParties(own):
	# Get list of parties
	partiesDir = logic.expandPath('//parties')
	partyNames = [x[2] for x in os.walk(partiesDir)][0]

	# NOTE(kgeffen) Strip off '.json' from each file (.json is last 5 chars)
	parties = [name[:-5] for name in partyNames if name.endswith('.json')]
	own['party1'] = parties
	own['party2'] = copy.deepcopy(parties)


# Move cursor to next selection up/down
def moveVertical(own, up):
	soundControl.play('navigate')
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

# Select a choice for current fieldNum
def moveHorizontal(own, left):
	field = FIELDS[ own['fieldNum'] ]

	# Start is a button, has no field
	if field == 'start':
		return

	soundControl.play('navigate')
	if left:
		objectControl.getFromScene('leftArrow', 'main').worldScale = [1.5, 1.5, 1.5]
		# Cycle list
		entry = own[field].pop()
		own[field].insert(0, entry)

	else:
		objectControl.getFromScene('rightArrow', 'main').worldScale = [1.5, 1.5, 1.5]
		# Cycle list
		entry = own[field].pop(0)
		own[field].append(entry)

# Select the option that selector is over currently
def select(own):
	field = FIELDS[ own['fieldNum'] ]

	if field == 'start':
		# Set all globalDicts based on fields
		logic.globalDict['stage'] = own['stages'][0]
		logic.globalDict['party1'] = own['party1'][0]
		logic.globalDict['party2'] = own['party2'][0]
		# 'players' must be handled a little differently

		# Start battlefield
		path = logic.expandPath('battlefield.blend')
		logic.startGame(path)

	elif field == 'party1' or field == 'party2':		
		# Set name of party being dealt with
		logic.globalDict['party'] = own[field][0]

		logic.addScene('partyCreate')
		logic.getCurrentScene().suspend()
