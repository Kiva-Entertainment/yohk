# Cycle through list of choices for commands
# Ex: Cycle through units to add for 'deploy'
from bge import logic

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
	setup.costText()

