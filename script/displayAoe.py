# Display the area of effect of the current command
from bge import logic

from script import check, objectControl, marker

# TODO(kgeffen) This script also displays spaces that need to be empty during command
# which is only sort of aoe. Rename/split at next cleaning

# TODO(kgeffen) This happens every tic, but only needs to happen
# when cursor moves while selecting target
# When speeding up game, make this script fire less often

def attempt():
	# TODO(kgeffen) cursor should have setting for command
	# and specific command should be stored elsewhere
	selectingCommand = logic.globalDict['cursor'] != 'wait' and \
						logic.globalDict['cursor'] != 'move'
	if selectingCommand:
		do()

def do():
	# Clear markers
	marker.clear()
	marker.clear('markerEmpty')
	marker.clear('markerAoe')

	# Get spaces
	rangeSpaces = getRangeSpaces()
	aoeSpaces = getAoeSpaces()
	emptySpaces = getEmptySpaces()
	
	coveredSpaces = []
	
	# Add markers for each space, only if that space is uncovered
	for space in emptySpaces:
		marker.add(space, 'markerEmpty')
		coveredSpaces.append(space)

	for space in aoeSpaces:
		if space not in coveredSpaces:
			marker.add(space, 'markerAoe')
			coveredSpaces.append(space)

	for space in rangeSpaces:
		if space not in coveredSpaces:
			marker.add(space)
			coveredSpaces.append(space)

# Return a list of all spaces that could be selected as target center for command
def getRangeSpaces():
	spaces = []
	for space in logic.globalDict['spaceTarget']:
		spaces.append(space['space'])

	return spaces

# Return a list of all spaces that are in command's aoe if command is performed with cursor
# as target center
def getAoeSpaces():
	target = getTargetAtCursor()
	if target is not None:
		return target['effectedSpaces']
	else:
		return []

# Return a list of all spaces that must be empty for command to be performed with cursor
# as target center
def getEmptySpaces():
	target = getTargetAtCursor()
	if target is not None:
		return target['specialSpaces']
	else:
		return []

# Get the target dictionary (if any) for command occuring at cursor's position
def getTargetAtCursor():
	cursor = objectControl.getFromScene('cursor', 'battlefield')
	cursorPosition = cursor.worldPosition

	for target in logic.globalDict['spaceTarget']:
		
		# If target happens on same space as given position, return it 
		if check.eq2D(cursorPosition, target['space']):
			return target
