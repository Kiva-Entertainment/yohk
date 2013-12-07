# Get unit data for unit(s) based on various conditions
from script import getPosition
from script.unitControl import object as unitObject

# Move given unit's object to given space, and store new position
def toSpace(unit, position):
	# Move object
	# NOTE(kgeffen) This has to happen first because objects gotten based on position
	obj = unitObject.get(unit)
	obj.worldPosition = getPosition.onGround(position)

	# Adjust position stored in unit's data
	x = round(position[0])
	y = round(position[1])
	unit['position'] = [x,y]
