# Control everything that happens in the start menu
from bge import logic, events
import json, os

from script.command import commands


from mathutils import Vector
import copy, os

from script import objectControl, soundControl

ACTIVE = logic.KX_INPUT_JUST_ACTIVATED
# Distance in height between one field and the next
D_HEIGHT = 0.1
# A list of all fields by number
FIELDS = ['party', 'name', 'class', 'addSkill', 'removeSkill', 'button']
FIELDS_W_ARROWS = ['name', 'class', 'addSkill', 'removeSkill']
BUTTONS = ['exit', 'save', 'delete']

def setup(cont):
	own = cont.owner

	if cont.sensors['start'].positive:
		# Read party data from json
		partyName = logic.globalDict['party']

		filepath = logic.expandPath('//parties/') + partyName + '.json'
		with open(filepath) as partyFile:
			own['units'] = json.load(partyFile)

		own['party'] = partyName

		# Read list of commands to add from json
		filepath = logic.expandPath('//releasedCommands.json')
		with open(filepath) as commandsFile:
			own['addSkill'] = json.load(commandsFile)


def update(cont):
	own = cont.owner

	keyboard = logic.keyboard

	# TODO(kgeffen) Only if not editing field
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


	updateDisplay(own)

# Update screen display
def updateDisplay(own):
	# Update each text field
	updateTextFields(own)

	# Scale down the arrows if they are enlarged
	for arrowName in ['leftArrow2', 'rightArrow2']:
		arrow = objectControl.getFromScene(arrowName, 'partyCreate')
		if arrow.localScale.x > 1:
			arrow.localScale -= Vector((0.035, 0.035, 0.035))

	# Hide arrows if necessary
	field = FIELDS[ own['fieldNum'] ]
	if field not in FIELDS_W_ARROWS:
		objectControl.getFromScene('leftArrow2', 'partyCreate').setVisible(False)
		objectControl.getFromScene('rightArrow2', 'partyCreate').setVisible(False)
	else:
		objectControl.getFromScene('leftArrow2', 'partyCreate').setVisible(True)
		objectControl.getFromScene('rightArrow2', 'partyCreate').setVisible(True)

def updateTextFields(own):
	setTextFields(own)

	# Reset all fields to black
	for field in FIELDS:
		if field != 'button':
			objectControl.getFromScene('text_' + field, 'partyCreate').color = (0, 0, 0, 1)
		else:
			# Make all buttons black
			for buttonName in BUTTONS:
				objectControl.getFromScene('text_button_' + buttonName, 'partyCreate').color = (0, 0, 0, 1)

	# Make selected field white
	# If button is selected, make correct button white
	field = FIELDS[ own['fieldNum'] ]
	if field != 'button':
		objectControl.getFromScene('text_' + field, 'partyCreate').color = (1, 1, 1, 1)
	else:
		button = BUTTONS[ own['buttonNum'] ]
		objectControl.getFromScene('text_button_' + button, 'partyCreate').color = (1, 1, 1, 1)

def setTextFields(own):
	'''Party Text'''
	partyText = objectControl.getFromScene('text_party', 'partyCreate')
	partyText.text = own['party']

	'''Name Text'''
	nameText = objectControl.getFromScene('text_name', 'partyCreate')
	nameText.text = own['units'][0]['name']

	'''Class Text'''
	classText = objectControl.getFromScene('text_class', 'partyCreate')
	# TODO(kgeffen) Change 'model' to 'class' everywhere
	classText.text = own['units'][0]['model']	

	'''Add Skill Text'''
	addSkillText = objectControl.getFromScene('text_addSkill', 'partyCreate')
	# TODO(kgeffen) Change 'model' to 'class' everywhere
	addSkillText.text = own['addSkill'][0]
	
	# Add skill

	removeSkillText = objectControl.getFromScene('text_removeSkill', 'partyCreate')
	removeSkillText.text = own['units'][0]['commands'][0][0]

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

# Select a choice for current fieldNum
def moveHorizontal(own, left):
	field = FIELDS[ own['fieldNum'] ]

	callDict = {
		'party' : cycleParty,
		'name' : cycleName,
		'class' : cycleClass,
		'addSkill' : cycleAddSkill,
		'removeSkill' : cycleRemoveSkill,
		'button' : cycleButton
	}

	method = callDict[field]
	method(own, left)

	# Scale up arrow chosen
	if left:
		objectControl.getFromScene('leftArrow2', 'partyCreate').worldScale = [1.5, 1.5, 1.5]
	else:
		objectControl.getFromScene('rightArrow2', 'partyCreate').worldScale = [1.5, 1.5, 1.5]

	# Play sound
	soundControl.play('navigate')

def cycleParty(own, left):
	pass

def cycleName(own, left):
	if left:
		objectControl.getFromScene('leftArrow2', 'partyCreate').worldScale = [1.5, 1.5, 1.5]
		# Cycle list
		entry = own['units'].pop()
		own['units'].insert(0, entry)

	else:
		objectControl.getFromScene('rightArrow2', 'partyCreate').worldScale = [1.5, 1.5, 1.5]
		# Cycle list
		entry = own['units'].pop(0)
		own['units'].append(entry)

def cycleClass(own, left):
	pass

def cycleAddSkill(own, left):
	pass

def cycleRemoveSkill(own, left):
	pass

def cycleButton(own, left):
	if left:
		if own['buttonNum'] > 0:
			own['buttonNum'] -= 1
		else:
			own['buttonNum'] = len(BUTTONS) - 1
	else:
		if own['buttonNum'] < len(BUTTONS) - 1:
			own['buttonNum'] += 1
		else:
			own['buttonNum'] = 0

def dsahjkdsa():
	soundControl.play('navigate')
	if left:
		objectControl.getFromScene('leftArrow2', 'partyCreate').worldScale = [1.5, 1.5, 1.5]
		# Cycle list
		entry = own[field].pop()
		own[field].insert(0, entry)

	else:
		objectControl.getFromScene('rightArrow2', 'partyCreate').worldScale = [1.5, 1.5, 1.5]
		# Cycle list
		entry = own[field].pop(0)
		own[field].append(entry)

# Select the option that selector is over currently
def select(own):
	field = FIELDS[ own['fieldNum'] ]

	if field == 'button':
		button = BUTTONS[ own['buttonNum'] ]
		if button == 'exit':
			returnToMainScreen()

		elif button == 'save':
			pass

		elif button == 'delete':
			# Delete the json that has this parties information
			party = logic.globalDict['party']
			filepath = logic.expandPath('//parties/') + party + '.json'
			os.remove(filepath)

			own.sendMessage('partiesChanged')

			returnToMainScreen()

def returnToMainScreen():
	# Resume main screen, end this one
	for scene in logic.getSceneList():
		if scene.name == 'main':
			scene.resume()
			logic.getCurrentScene().end()



def mpmpfempmf():
	return
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
		screen1 = objectControl.getFromScene('screen1', 'main')
		screen1.worldPosition.z += 1.5
