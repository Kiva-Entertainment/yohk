# Perform the currently selected command
# Called by cursor.select.target.py
from bge import logic

from script import check, objectControl, commandControl, unitControl
from script.command import cleanup

def attempt():
	cursor = objectControl.getFromScene('cursor', 'battlefield')
	cursorPosition = cursor.worldPosition
	
	effectedUnits = unitsInSpacesAoe(cursorPosition)
	
	if effectedUnits is not None:
		
		actor = unitControl.get.actor()
		targets = effectedUnits
		command = logic.globalDict['cursor']
		
		# Store effected special spaces in 'commandSpecialSpaces'
		storeSpecialSpaces(cursorPosition)

		do(actor, targets, command)

		# Indicate that command was performed
		return True
def do(actor, targets, command):
	# Perform the command
	commandControl.perform(command, actor, targets)
	
	# Do any necessary post-command work (Lowering sp, etc.)
	cleanup.do()

# Store in globalDict a list of all special spaces for command targeting given position
def storeSpecialSpaces(space):
	# NOTE(kgeffen) Nearly identical copy of below method
	# NOTE(kgeffen) Check each space that could be targetted,
	# if one matchs _space_, assign all it special spaces to globalDict
	for targetCenter in logic.globalDict['spaceTarget']:
		if check.eq2D(space, targetCenter['space']):
			logic.globalDict['commandSpecialSpaces'] = targetCenter['specialSpaces']

# Return list of all units effected by current command targeting given space
def unitsInSpacesAoe(space):
	# NOTE(kgeffen) Check each space that could be targetted,
	# if one matchs _space_, return all units that are effected by
	# targetting it
	for targetCenter in logic.globalDict['spaceTarget']:
		if check.eq2D(space, targetCenter['space']):
			return targetCenter['units']
