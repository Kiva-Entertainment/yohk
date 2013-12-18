# Perform the currently selected command
# Called by cursor.select.target.py
from bge import logic

from script import check, objectControl, commandControl
from script.command import cleanup

def attempt(cursorPosition):
	# List of units effected by command happening at given position
	effectedUnits = unitsInSpacesAoe(cursorPosition)

	# If list is None (None, not empty list) command cannot target given position, thus can't be performed
	# TODO(kgeffen) This is an implementation detail, make the check for valid space more obvious
	if effectedUnits is None:
		return False

	commandName = logic.globalDict['cursor']
	requiresTarget = commandControl.hasTag(commandName, 'targets')

	if requiresTarget and effectedUnits == []:
		return False
	else:
		# Store effected special spaces in 'commandSpecialSpaces'
		storeSpecialSpaces(cursorPosition)
		
		do(effectedUnits)

		# Indicate that command was performed
		return True

def do(targets):
	actor = logic.globalDict['actor']
	command = logic.globalDict['cursor']

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
