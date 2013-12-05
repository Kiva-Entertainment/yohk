# Returns common shapes in the form of lists of spaces

# A single space at center ([0,0])
def single():
	return [[0,0]]

# Ring of radius _radius_
# Ex: length = 1 describes a ring with 4 spaces, each adjacent to center
def ring(length):
	spaces = []
	
	# length = xMag + yMag for every int value pair of xMag and yMag
	for xMag in range(0, length + 1):
		yMag = length - xMag
		
		# Do for +/-x and +/-y
		for x in set([-xMag, xMag]):
			for y in set([-yMag, yMag]):
				
				spaces.append([x,y])
	
	return spaces

# Diamond the includes all spaces within _length_ of center
# 'length' = the max offset from the center
# Ex: length = 2 describes a diamond with 13 spaces in it
def diamond(length):
	spaces = [[0,0]]
	
	# Describes space in rings of radius r
	for r in range(1, length + 1):
		for space in ring(r):
			spaces.append(space)
	
	return spaces

# A diamond minus the center space
def emptyDiamond(length):
	return removeCenter(diamond(length))

# Straight line going out from center _length_ spaces
def line(length):
	spaces = []
	
	for l in range(0, length):
		spaces.append([0, l])
	
	return spaces

# Line going out to the sides from center
# Extends _length_ spaces to the right/left of center
# 'length' = the max offset from the center
# Ex: length = 1 describes a line with 3 spaces, one left of center, one right
def flatLine(length):
	spaces = [[0,0]]
	
	for l in range(1, length + 1):
		spaces.append([l, 0])
		spaces.append([-l, 0])
	
	return spaces


'Utility'
# Remove the center space from a list of spaces
CENTER_SPACE = [0,0]
def removeCenter(spaces):
	# Retain only space that do not equal CENTER_SPACE, return result
	return list(filter((CENTER_SPACE).__ne__, spaces))
