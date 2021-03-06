# Setup various graphical aspects of the 'commandSelect' scene
from bge import logic

from script import sceneControl, dynamicMaterial, objectControl, commandControl, textControl

# The max number of characters in a line of text
WRAP_AT = 50

LIST_OBJECT_NAME = 'commandSelect_list'
COST_OBJECT_NAME = 'commandSelect_cost'
DESCRIPTION_OBJECT_NAME = 'commandSelect_description'
ICON_OBJECT_NAME = 'commandSelect_icon'
CHOICE_OBJECT_NAME = 'commandSelect_choice'
EXTENT_OBJECT_NAME = 'commandSelect_extent'
SCENE_NAME = 'commandSelect'

# Setup the entire screen in commandSelect
def screen():
	listText()
	iconImage()
	choiceText()
	costText()
	descriptionText()
	extentText()


# Alter the icon diplayed
def iconImage():
	iconObject = objectControl.getFromScene(ICON_OBJECT_NAME, SCENE_NAME)
	
	# Get the first list of commands
	commands = getCommandsList()[0]
	if len(commands) == 0:
		# No commands to display icon for, make icon invisible
		iconObject.setVisible(False)

	else:
		iconObject.setVisible(True)
		
		filename = commandControl.icon(commands[0])
		# The path to the icon's image file
		path = logic.expandPath('//images/icons/' + filename)
		
		dynamicMaterial.switchMaterialsImage(path, ICON_OBJECT_NAME)

# Alter the text of the 'list of actions' text object
def listText():
	# Get the first list of commands
	commands = getCommandsList()[0]
	
	# Form list of all commands in first list seperated by newlines
	text = ''
	for command in commands:
		text += commandControl.name(command) + '\n'
	
	# Set the text of the object
	object = objectControl.getFromScene(LIST_OBJECT_NAME, SCENE_NAME)
	object['Text'] = text

# Alter the text of the 'cost of command' text object
def costText():
	# Get the first list of commands
	commands = getCommandsList()[0]
	
	# Form displayed text
	text = ''
	if len(commands) != 0:
		# Get the cost of the first command in the list
		cost = commandControl.cost(commands[0])
		
		# Get actor's current sp
		unit = logic.globalDict['actor']
		currentSp = unit['sp']
		
		text = 'Cost: ' + str(cost) + '/' + str(currentSp)
	
	# Set the text of the object
	object = objectControl.getFromScene(COST_OBJECT_NAME, SCENE_NAME)
	object['Text'] = text

# Alter the text of the 'description of action' text object
def descriptionText():
	# Get the first list of commands
	commands = getCommandsList()[0]
	
	# Get description text
	text = ''
	if len(commands) != 0: # Only if there are commands to describe
		text = commandControl.description(commands[0])
		text = textControl.wrap(text, WRAP_AT)
	
	# Set the text of the object
	obj = objectControl.getFromScene(DESCRIPTION_OBJECT_NAME, SCENE_NAME)
	obj['Text'] = text

# Alter the text of the 'command choice' text object
def choiceText():
	# Get the command currently being considered
	command = getCommandsList()[0][0]

	choices = logic.globalDict['commandChoices']
	if choices == []:
		# Form list of choices for command, if any
		commandControl.determineChoices(command)

	# Display choice, if any
	# NOTE(kgeffen) determineChoices may have populated choices
	text = ''
	if choices != []:
		text = choices[0]['display']

	# Set the text of the object
	object = objectControl.getFromScene(CHOICE_OBJECT_NAME, SCENE_NAME)
	object['Text'] = text

# Alter the text of the 'current extent' text object
def extentText():
	# Get the command currently being considered
	command = getCommandsList()[0][0]

	text = ''
	if commandControl.hasTag(command, 'extends'):
		extent = logic.globalDict['extent']
		text = 'Extent: ' + str(extent)
	
	# Set the text of the object
	object = objectControl.getFromScene(EXTENT_OBJECT_NAME, SCENE_NAME)
	object['Text'] = text

def getCommandsList():
	unit = logic.globalDict['actor']
	commandsList = unit['commands']
	
	return commandsList

