# Cycle through current list of commands
# or list of lists of commands
from bge import logic

from script import soundControl
from script.scene.commandSelect import setup

# NOTE(kgeffen) Both methods are called by game.
# Commands are stored as lists of lists of commands,
# cycle.commandLists cycles through the lists of commands
# cycle.commands cycles through the commands in the current list
# They are different

# Cycle through the list of lists of commands being viewed
# Ex: cycle from ['slash','smack'] to ['defend','dash']
def commandLists(cont):
	# Get list of command
	unit = logic.globalDict['actor']
	commandsList = unit.stats['commands']

	# Don't cycle lists if there is only 1 list
	if len(commandsList) == 1:
		return
	
	leftKey = cont.sensors['leftKey'].positive
	rightKey = cont.sensors['rightKey'].positive

	# Do nothing if both or neither are pressed
	if (leftKey and rightKey) or (not leftKey and not rightKey):
		return
	
	if leftKey:
		# 'commands' - A list of commands
		commands = commandsList.pop()
		commandsList.insert(0, commands)
	elif rightKey:
		# 'commands' - A list of commands
		commands = commandsList.pop(0)
		commandsList.append(commands)
	
	# Reset extent
	cont.owner['extent'] = 0
	# Reset choices
	logic.globalDict['commandChoices'] = []

	# Play sound
	soundControl.play('navigate')
	
	setup.screen()

# Cycle through the current list of commands being viewed
# Ex: Cycle ['slash','smack','defend'] to ['defend','slash','smack']
def commands(cont):
	# Get the first list of commands (The one onscreen)
	unit = logic.globalDict['actor']
	commandsList = unit.stats['commands']
	commands = commandsList[0]

	# Don't cycle commands if there are only 1 or 0 commands
	if len(commands) <= 1:
		return
	
	upKey = cont.sensors['upKey'].positive
	downKey = cont.sensors['downKey'].positive

	# Do nothing if both or neither are pressed
	if (upKey and downKey) or (not upKey and not downKey):
		return

	if upKey:
		command = commands.pop()
		commands.insert(0, command)
	elif downKey:
		command = commands.pop(0)
		commands.append(command)
	
	# Reset extent
	cont.owner['extent'] = 0
	# Reset choices
	logic.globalDict['commandChoices'] = []
	
	# Play sound
	soundControl.play('navigate')

	setup.screen()
