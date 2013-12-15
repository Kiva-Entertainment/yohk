# Alter the extent of the current command
from bge import logic

from script import commandControl
from script.scene.commandSelect import setup

# Raise or lower the extent of the current command by 1
# Extent cannot go below 0
def alter(cont):
	aKey = cont.sensors['aKey'].positive
	dKey = cont.sensors['dKey'].positive
	
	if aKey and logic.globalDict['extent'] != 0:
		logic.globalDict['extent'] -= 1
		
	elif dKey:
		logic.globalDict['extent'] += 1
	
	# Display the new cost of the command
	setup.screen()

def max(cont):
	command = getSelectedCommand()
	if cont.sensors['gKey'].positive:
		if commandControl.hasTag(command, 'extends'):
			# Start extent at zero and increase until the first cost greater than actor's sp is found
			# If actor cannot afford to pay for command at extent = 0, set to 0 anyways (Not -1)
			ARBITRARILY_LARGE_NUMBER = 1000
			logic.globalDict['extent'] = 0

			# NOTE(kgeffen) Not 'while True' to prevent infinite loop if 'extends' tag wrongly added
			while logic.globalDict['extent'] < ARBITRARILY_LARGE_NUMBER:
				if commandControl.cost(command) > logic.globalDict['actor']['sp']:
					if logic.globalDict['extent'] != 0:
						logic.globalDict['extent'] -= 1
					break

				else:
					logic.globalDict['extent'] += 1

			# Display the new cost of the command
			setup.screen()

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
