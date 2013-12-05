# Returns common shapes in the form of lists of spaces

# A single space at center ([0,0])
def single():
	return [[0,0]]

# Ring of radius _radius_
# Ex: length = 1 describes a ring with 4 spaces, each adjacent to center
def ring(length):
	offsets = []
	
	# length = xMag + yMag for every int value pair of xMag and yMag
	for xMag in range(0, length + 1):
		yMag = length - xMag
		
		# Do for +/-x and +/-y
		for x in set([-xMag, xMag]):
			for y in set([-yMag, yMag]):
				
				offsets.append([x,y])
	
	return offsets

# Diamond the includes all spaces within _length_ of center
# 'length' = the max offset from the center
# Ex: length = 2 describes a diamond with 13 spaces in it
def diamond(length):
	offsets = [[0,0]]
	
	# Describes space in rings of radius r
	for r in range(1, length + 1):
		for space in ring(r):
			offsets.append(space)
	
	return offsets

# Straight line going out from center _length_ spaces
def line(length):
	offsets = []
	
	for l in range(0, length):
		offsets.append([0, l])
	
	return offsets

# Line going out to the sides from center
# Extends _length_ spaces to the right/left of center
# 'length' = the max offset from the center
# Ex: length = 1 describes a line with 3 spaces, one left of center, one right
def flatLine(length):
	offsets = [[0,0]]
	
	for l in range(1, length + 1):
		offsets.append([l, 0])
		offsets.append([-l, 0])
	
	return offsets
