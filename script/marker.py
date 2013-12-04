# Perform common actions relating to markers
# Called from many other scripts
from bge import logic

from script import sceneControl, check, getPosition

# The most common type of marker
DEFAULT_MARKER = 'markerRange'

# Add a given kind of marker at the given space
# Does not check if space is in stage bounds
def add(space, markerName = DEFAULT_MARKER):
	# If space is in bounds
	if not check.outOfBounds(space):
		position = getPosition.onGround(space)
		
		# Get battlefield scene
		battlefield = sceneControl.get('battlefield')
		
		# NOTE(kgeffen) Ground is arbitrarily the object adding the marker
		obj = battlefield.addObject(markerName, 'ground')
		obj.worldPosition = position

# Removes all markers of a given kind
# TODO(kgeffen) Every call to this wants all markers removed,
# make a list of all marker names and clear all of them, not just the default marker
def clear(markerName = DEFAULT_MARKER):
	scene = sceneControl.get('battlefield')
	
	# NOTE(kgeffen) Not using objectControl because have to get multiple markers
	for object in scene.objects:
		if object.name == markerName:
			object.endObject()

