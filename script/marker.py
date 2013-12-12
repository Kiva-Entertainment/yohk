# Perform common actions relating to markers
# Called from many other scripts
from bge import logic

from script import sceneControl, check, getPosition

# Add a given kind of marker at the given space
# Does not check if space is in stage bounds
def add(space, markerName):
	# If space is in bounds
	if not check.outOfBounds(space):
		position = getPosition.onGround(space)
		
		# Get battlefield scene
		battlefield = sceneControl.get('battlefield')
		
		# NOTE(kgeffen) Ground is arbitrarily the object adding the marker
		obj = battlefield.addObject(markerName, 'ground')
		obj.worldPosition = position

# Removes all markers of a given kind
def clear(markerName):
	scene = sceneControl.get('battlefield')
	
	# NOTE(kgeffen) Not using objectControl because have to get multiple markers
	for object in scene.objects:
		if object.name == markerName:
			object.endObject()


# Remove all markers that display command range
def clearCommandMarkers():
	COMMAND_MARKERS = ['markerRange', 'markerAoe', 'markerEmpty']

	for markerName in COMMAND_MARKERS:
		clear(markerName)


# Remove all markers that display movement range
def clearMoveMarkers():
	MOVE_MARKERS = ['markerMove']

	for markerName in MOVE_MARKERS:
		clear(markerName)

