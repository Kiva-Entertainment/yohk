# Display the area of effect of the current command
from bge import logic

from script import check, objectControl, marker

# TODO(kgeffen) This script also displays spaces that need to be empty during command
# which is only sort of aoe. Rename/split at next cleaning

# TODO(kgeffen) This happens every tic, but only needs to happen
# when cursor moves while selecting target
# When speeding up game, make this script fire less often

# TODO(kgeffen) 'Standard' range markers are added when command is selected from commandSelect
# But they should be added every time this script executes so that markers do not overlap
# No 2 markers should be added to the same space, and aoe takes precedence

def do(aoe):
	# Clear any markers from last tic
	marker.clear('markerAoe')
	marker.clear('markerEmpty')
	
	cursor = objectControl.getFromScene('cursor', 'battlefield')
	cursorPosition = cursor.worldPosition
	
	# Get data for command targetted at cursor's position
	target = getTargetAtPosition(cursorPosition)
	if target is not None:
		
		# Add a marker at each space command requires be empty
		for specialSpace in target['specialSpaces']:
			marker.add(specialSpace, 'markerEmpty')
		
		# Add a marker at each space that command would hit in its aoe
		for aoeSpace in target['effectedSpaces']:
			marker.add(aoeSpace, 'markerAoe')

# Get the target dictionary for command occuring at _position_, if any
def getTargetAtPosition(position):
	for target in logic.globalDict['spaceTarget']:
		
		# If target happens on same space as given position, return it 
		if check.eq2D(position, target['space']):
			return target
