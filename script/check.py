# Commonly used checks
from bge import logic

# NOTE(kgeffen) Position is stored/returned as 2d/3d for many reasons in many places
# To combat that, comparisons should be done with this method instead of standard eq.
# Return true if positions have same x and y as each other.
def eq2D(p1, p2):
	if p1[0] == p2[0]:
		if p1[1] == p2[1]:
			return True

# Test if space is out of bounds of the current map
def outOfBounds(space):
	x, y = round(space[0]), round(space[1])
	
	if (x < 0) or (x >= logic.globalDict['xLength']) or \
	   (y < 0) or (y >= logic.globalDict['yLength']):
		return True
