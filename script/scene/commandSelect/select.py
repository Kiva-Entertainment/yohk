# Select command from list of commands
from bge import logic

from script import sceneControl, commandControl, soundControl

def attempt(cont):
	if cont.sensors['spaceKey'].positive:
		do()

def do():
	selectedCommand = getSelectedCommand()
	
	if selectedCommand != None:
		
		if commandIsAllowed(selectedCommand):
			selectCommand(selectedCommand)

			soundControl.play('confirmation')
			
		else:
			soundControl.play('negative')


# Get command selected in commandSelect
def getSelectedCommand():
	unitD = logic.globalDict['actor'].stats
	
	# List of commands displayed on screen
	# NOTE(kgeffen) Has multiple lists of commands, get the first one
	commands = unitD['commands'][0]
	
	# Assuming that current list of commands is not empty
	if len(commands) != 0:
		# First command in current list
		return commands[0]

# Select the current command and return to battlefield to choose target(s)
def selectCommand(command):
	logic.globalDict['cursor'] = command
	
	commandControl.determineRange(command)

	sceneControl.resume('battlefield')
	sceneControl.show('battlefieldOverlay', 'basicInfo')
	sceneControl.hide('commandSelect')

def commandIsAllowed(command):
	unitD = logic.globalDict['actor'].stats
	
	# Not allowed if unit can't afford it (In sp)
	cost = commandControl.cost(command)
	if cost > unitD['sp']:
		return False
	
	return True
