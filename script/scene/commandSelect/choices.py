# Cycle through list of choices for commands
# Ex: Cycle through units to add for 'deploy'
from bge import logic

from script import soundControl
from script.scene.commandSelect import setup

# NOTE(kgeffen) For now, choice cycling happens with directional keys because the only
# unit with a choice skill is the base, which only has 1 skill.
# This may change in the future

# Cycle through choices forwards/backwards 1 choice
def cycle(cont):
	leftKey = cont.sensors['leftKey'].positive
	rightKey = cont.sensors['rightKey'].positive

	# Do nothing if both or neither are pressed
	if (leftKey and rightKey) or (not leftKey and not rightKey):
		return

	choices = logic.globalDict['commandChoices']
	if choices != []:

		if leftKey:
			choice = choices.pop()
			choices.insert(0, choice)
			
		elif rightKey:
			choice = choices.pop(0)
			choices.append(choice)

		# Play sound
		soundControl.play('navigate')
			
		# Display the new cost of the command
		setup.choiceText()

