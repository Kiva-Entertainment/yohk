# Cycle through list of choices for commands
# Ex: Cycle through units to add for 'deploy'
from bge import logic

from script.scene.commandSelect import setup

# Cycle through choices forwards/backwards 1 choice
def cycle(cont):
	zKey = cont.sensors['zKey'].positive
	cKey = cont.sensors['cKey'].positive
	
	choices = logic.globalDict['commandChoices']

	if zKey:
		choice = choices.pop()
		choices.insert(0, choice)
		
	elif cKey:
		choice = choices.pop(0)
		choices.append(choice)
		
	# Display the new cost of the command
	setup.choiceText()

