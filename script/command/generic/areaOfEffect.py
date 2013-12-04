# Returns common areas of effect for commands
# Ex: AOE might be a plus sign centered on the selected space
# Called by commands.py and rangeFactors.py

# Describe a ring of radius _length_
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

def single():
	return [[0,0]]

# Diamond that hits all units _length_ spaces from center
# 'length' = the max offset from the center
# Ex: length = 2 describes a diamond with 13 spaces in it
def diamond(length):
	offsets = [[0,0]]
	
	# NOTE(kgeffen) Copied from script.command.generic.range.basic, altered slightly
	
	# Describes space in rings of radius r
	for r in range(1, length + 1):
		for space in ring(r):
			offsets.append(space)
	
	return offsets

# Two lines of equal length intersecting at a point (A plus sign)
# 'length' = the max offset from the center
# Ex: length = 1 describes a plus sign with 5 spaces in it
def cross(length):
	offsets = [[0,0]]
	
	for l in range(1, length + 1):
		# Point in each of 4 cardinal directions
		for dv in ([0, l], [0, -l], [l, 0], [-l, 0]):
			offsets.append(dv)
	
	return offsets

# 'length' = the max offset from the center
# Ex: length = 1 describes a line with 3 spaces, one left of center, one right
def line(length):
	offsets = [[0,0]]
	
	for l in range(1, length + 1):
		offsets.append([l, 0])
		offsets.append([-l, 0])
	
	return offsets

# Straight line of given length
def sightLine(length):
	offsets = []
	
	for l in range(0, length):
		offsets.append([0, l])
	
	return offsets
