# Select command from list of commands
from bge import logic

from script import sceneControl, commandControl, objectControl

# Message sent to battlefield that causes range to display
MESSAGE_TO_BATTLEFIELD = 'displayCommandRange'

def attempt(cont):
	if cont.sensors['spaceKey'].positive:
		do()

def do():
	selectedCommand = getSelectedCommand()
	
	if selectedCommand != None:
		
		if commandIsAllowed(selectedCommand):
			selectCommand(selectedCommand)
		else:
			pass
			#utility.playSound('negative')


# Get command selected in commandSelect
def getSelectedCommand():
	unit = logic.globalDict['actor']
	
	# List of commands displayed on screen
	# NOTE(kgeffen) Has multiple lists of commands, get the first one
	commands = unit['commands'][0]
	
	# Assuming that current list of commands is not empty
	if len(commands) != 0:
		# First command in current list
		return commands[0]

# Select the current command and return to battlefield to choose target(s)
def selectCommand(command):
	logic.globalDict['cursor'] = command
	
	sceneControl.resume('battlefield')
	sceneControl.show('battlefieldOverlay')
	sceneControl.hide('commandSelect')
	
	sendMessageToBattlefield(MESSAGE_TO_BATTLEFIELD)

def commandIsAllowed(command):
	unit = logic.globalDict['actor']
	
	# Not allowed if unit has no more actions left
	if unit['act'] == 0:
		return False
	
	# Not allowed if unit can't afford it (In sp)
	cost = commandControl.cost(command)
	if cost > unit['sp']:
		return False
	
	return True

def sendMessageToBattlefield(message):
	# Sender must be in same scene (battlefield) as receiver of message
	# Sender object is arbitrarily 'ground'
	object = objectControl.getFromScene('ground', 'battlefield')
	object.sendMessage(message)
