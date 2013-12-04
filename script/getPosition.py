# Get positions based on various requirements

# Called from many other scripts
from bge import logic

# Given a space (or position), find the position of the ground that is below/above
# that space
# Ex: if ground is uniform with height 4:
# [1, 3, 5.343] returns [1, 3, 4]
# Space must be in stage bounds!
def onGround(space):
	x = round(space[0])
	y = round(space[1])
	z = logic.globalDict['groundHeight'][x][y]
	
	return [x,y,z]

# If position is not within map bounds, wrap to other side
def onMap(position):
	x = round(position[0])
	y = round(position[1])
	
	if x < 0:
		position[0] = logic.globalDict['xLength'] - 1
		
	elif logic.globalDict['xLength'] <= x:
		position[0] = 0
		
	elif y < 0:
		position[1] = logic.globalDict['yLength'] - 1
		
	elif logic.globalDict['yLength'] <= y:
		position[1] = 0
	
	return position

# Returns the position, including z, of the unit given
def ofUnit(unitNumber):
	data = logic.globalDict['units'][unitNumber]
	position2D = data['position']
	
	# Position is only x and y, get z also
	position = onGround(position2D)
	
	return position

# Returns the position, including z, of the acting unit
def actor():
	unitNumber = int(logic.globalDict['selected'])
	
	# Return the position of the unit that is the actor 
	return ofUnit(unitNumber)
