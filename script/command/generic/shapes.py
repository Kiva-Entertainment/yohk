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
# If _offset_ is provided, exclude that many rings
def diamond(length, offset = 0):
	spaces = []
	
	# Describes space in rings of radius r
	for r in range(offset, length + 1):
		for space in ring(r):
			spaces.append(space)
	
	return spaces

# Rectangle that extends left/right by _width_ spaces and up/down by _height_ spaces
# Ex: rectangle(0,1) Describes a 1x3 rectangle with height 3
# If offset is given, exclude that many rings from center
# If hollow, exclude center space
def rectangle(width, height, hollow = False):
	spaces = []

	for x in range(-width, width + 1):
		for y in range(-height, height + 1):
			spaces.append([x,y])

	if hollow:
		spaces.remove([0,0])

	return spaces

# Cross that includes all spaces _length_ spaces from center cardinally
# 'length' = the max offset from the center
# If _offset_ is provided, exclude that many spaces in each direction
def cross(length, offset = 0):
	spaces = []
	
	# Add center if shape has it
	if offset == 0:
		spaces.append([0,0])
		# Do not add center in below for loop
		offset += 1

	for r in range(offset, length + 1):
		for space in [[0,r], [0,-r], [r,0], [-r,0]]:
			spaces.append(space)
	
	return spaces

# Two diagonal lines crossing in an X
# Each line extends _length_ space in each direction from center space
# Ex: length = 1 describes an x with 5 spaces
# If _offset_ is provided, exclude that many spaces in each direction
def x(length, offset = 0):
	spaces = []

	# Add center if shape has it
	if offset == 0:
		spaces.append([0,0])
		# Do not add center in below for loop
		offset += 1
	
	for r in range(offset, length + 1):
		for space in [[r,r], [r,-r], [-r,r], [-r,-r]]:
			spaces.append(space)
	
	return spaces

# Straight line going out from center _length_ spaces
# If _offset_ is provided, put that many empty spaces before the line begins
def line(length, offset = 0):
	spaces = []
	
	for l in range(offset, length + offset):
		spaces.append([0, l])
	
	return spaces

# Line going out to the sides from center
# Extends _length_ spaces to the right/left of center
# 'length' = the max offset from the center
# Ex: length = 1 describes a line with 3 spaces, one left of center, one right
def flatLine(length, offset = 0):
	spaces = []

	for l in range(offset, length + 1):
		spaces.append([l, 0])
		
		# Don't add duplicate l=0
		if -l != l:
			spaces.append([-l, 0])
	
	return spaces

# A triangle extending outwards
# _length_ equals distance it extends
def triangle(length):
	spaces = []
	
	for x in range(0, length):
		for y in range(-x, x + 1):
			spaces.append([y, x])
	
	return spaces

'Operations done to shapes'
# Push each of given spaces by given offset
def push(spaces, offset):
	for i in range(0, len(spaces)):
		x = spaces[i][0] + offset[0]
		y = spaces[i][1] + offset[1]
		spaces[i]  = [x,y]

	return spaces
