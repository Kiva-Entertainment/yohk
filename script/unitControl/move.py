# Move given unit to various places
from script import getPosition
from script.unitControl import object as unitObject

# Move given unit's object to given space
def toSpace(unit, space):
	# Move object
	# NOTE(kgeffen) This has to happen first because objects gotten based on position
	obj = unitObject.get(unit)
	obj.worldPosition = getPosition.onGround(space)

	# Adjust position stored in unit's data
	x = round(space[0])
	y = round(space[1])
	unit['position'] = [x,y]
