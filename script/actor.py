# TODO(kgeffen) Implement unit rotation when it becomes meaningful



# Rotate the actor in place
from bge import logic
from mathutils import Matrix
from math import radians
from script import objectControl, commandControl

QUARTER_ROTATION_Z = Matrix.Rotation(radians(90.0), 3, 'Z')

# Set rotation of actor to one of cardinal directions
def rotate(cont):
	# TODO(kgeffen) Allow this when it becomes meaningful
	return 'NOPE haha wait for it... one day'
	
	
	
	unitNumber = logic.globalDict['selected']
	
	# Actor's data - Rotated by the below if/elif
	unitData = logic.globalDict['units'][unitNumber]
	
	if cont.sensors['upKey'].positive:
		unitData['rotation'] = 0
	elif cont.sensors['leftKey'].positive:
		unitData['rotation'] = 1
	elif cont.sensors['downKey'].positive:
		unitData['rotation'] = 2
	elif cont.sensors['rightKey'].positive:
		unitData['rotation'] = 3
	else:
		# No direction pressed - No rotation needs to happen
		return
	
	# NOTE(kgeffen) Rotation of unit object should be default rotated by
	# a quarter circle x times where x is the value of the unit's rotation (Set above)
	newOrientation = Matrix.Identity(3)
	for i in range(0, unitData['rotation']):
		newOrientation *= QUARTER_ROTATION_Z
	
	# Set the orientation of the object
	unitObject = objectControl.getFromScene(str(unitNumber), 'battlefield')
	unitObject.worldOrientation = newOrientation

