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
		
	if y < 0:
		position[1] = logic.globalDict['yLength'] - 1
		
	elif logic.globalDict['yLength'] <= y:
		position[1] = 0
	
	return onGround(position)
