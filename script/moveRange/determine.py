# Create a list of all valid moves selected unit can perform
# Format is: [{'space' : [x,y], 'dMv' : c}, ...]
# List stored in globalDict 'validMove'
from bge import logic

from script import check, common

# NOTE(kgeffen) Since this method starts with lowest dMv and increases,
# it gets the smallest (lowest dMv) path possible
# Create a list of all valid moves for selected unit
def do(unit):
	# First move is from start, all others are from previous ring
	start = [{ 'space' : unit.space(),
			   'dMv' : 0 }]
	fromRing = start
	
	# final - List of all pairs (valid space/mv consumed)
	final = start
	for dMv in range(1, unit.stats['mv'] + 1): # dMv = How much movement is consumed
		
		newRing = spread(fromRing, dMv, unit.stats['jump'])
		fromRing = [] # Is repopulated in for loop
		
		# spaceWithDmv - a space in the newRing with the format: {'space' : [x,y], 'dMv' : c}
		for spaceWithDmv in newRing:
			space = spaceWithDmv['space']
			
			if spaceNotInDictionary(space, final):
				final.append(spaceWithDmv)
				fromRing.append(spaceWithDmv) # Ring to spread from next
	
	logic.globalDict['validMove'] = final

# Find each space accesible from a space in fromRing and return it paired to dMv
def spread(fromRing, dMv, maxDh):
	# List of all of the new spaces that unit can move to
	spaces = allValidSpreadSpaces(fromRing, maxDh)
	
	# Format and return spaces - Will contain duplicates
	newRing = []
	for space in spaces:
		spaceWithDmv = { 'space' : space, 'dMv' : dMv}
		newRing.append(spaceWithDmv)
	
	return newRing

# List all valid spaces 1 unit from fromRing
def allValidSpreadSpaces(fromRing, maxDh):
	validSpaces = []
	
	# For each space moved from
	for entry in fromRing:
		space = entry['space']
		
		x1 = space[0]
		y1 = space[1]
		h1 = round( logic.globalDict['groundHeight'][x1][y1] * 10 ) # In decimeters
		
		# Get each space 1 unit from spaces
		cardinalUnitVectors = [[1,0], [-1,0], [0,1], [0,-1]]
		for dp in cardinalUnitVectors:
			x2 = x1 + dp[0]
			y2 = y1 + dp[1]
			space = [x2, y2]
			
			if spaceValid(space, h1, maxDh):
				validSpaces.append(space)
	
	return validSpaces

# TODO(kgeffen) This code appear in multiple places, consider moving it to check.py
# Return true if space is valid in every way
def spaceValid(space, h1, maxDh):
	if check.outOfBounds(space):
		return False
	
	# The height of space in decimeters
	h2 = round( logic.globalDict['groundHeight'][space[0]][space[1]] * 10 )
	
	# Space invalid if its height is 0 (Gaps/unreachable have h = 0)
	if h2 == 0:
		return False
	
	# Space invalid if unit is already in it (Can't pass through unit)
	if common.unitInSpace(space) != None:
		return False
	
	# Space invalid if height too great
	if (h2 - h1) > maxDh:
		return False
		
	return True

# Return true if dictionary has no entry matching space
def spaceNotInDictionary(space, dictionary):
	# If any of the spaces in dictionary match the given space, space is already in dictionary
	for entry in dictionary:
		if entry['space'] == space:
			return False
	
	return True
