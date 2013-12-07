# If space meets all requirements, mark it as within command range
# by placing a marker on it
# Also, make a list of all spaces within aoe that are effected, and all units on them
from bge import logic

from script import check, unitControl, marker, getPosition

# Mark space valid if it meets all requirements
def attempt(actorPosition, targetSpace, rng):
	# Space can be targetted by command
	if spaceValid(actorPosition, targetSpace, rng):
		
		markTargetableSpace(actorPosition, targetSpace, rng)

# If space is within range of command, add marker
# If space has a unit in its range (Ex: Range = plus centered on space)
# add that unit to validCommandTargets
def markTargetableSpace(actorPosition, targetSpace, rng):
	targetPosition = getPosition.onGround(targetSpace)
	
	# Add a standard marker on space
	marker.add(targetPosition)
	
	# Get a list of all spaces within area of effect
	effectedSpaces = getEffectedSpaces(actorPosition, targetSpace, rng)
	
	# List of all units effected by command
	effectedUnits = getEffectedUnits(effectedSpaces)
	
	# Record all spaces that have special meaning for command
	# Ex: Space that actor moves to, spaces that must be empty, etc.
	specialSpaces = attemptGetSpecialSpaces(actorPosition, targetSpace, rng)
	if specialSpaces == False: # If any of the special spaces are invalid
		return
	
	# Add given space to list of all spaces that command can target
	formattedEntry = {'space' : targetPosition,
					  'effectedSpaces' : effectedSpaces,
					  'units' : effectedUnits,
					  'specialSpaces' : specialSpaces}
	
	logic.globalDict['spaceTarget'].append(formattedEntry)

def spaceValid(actorPosition, targetSpace, rng):
	# Invalid if space out of bounds
	if check.outOfBounds(targetSpace):
		return False
	
	targetPosition = getPosition.onGround(targetSpace)

	# Invalid if target space has height 0
	if targetPosition[2] == 0:
		return False
	
	# Invalid if height difference outside acceptable bounds
	dz = targetPosition[2] - actorPosition[2]
	if dz > rng['okDz']['max'] or dz < rng['okDz']['min']:
		return False
	
	return True

# Return a list of all spaces in aoe of command
def getEffectedSpaces(actorPosition, targetSpace, rng):
	effectedSpaces = []
	
	# For each space in list centered on position, if space will be effected
	# by command targetting position, add space to list of effected
	for offset in rng['aoe']:
		offsetX = targetSpace[0] + offset[0]
		offsetY = targetSpace[1] + offset[1]
		offsetSpace = [offsetX, offsetY]
		
		if spaceValid(actorPosition, offsetSpace, rng):
			effectedSpaces.append(offsetSpace)
	
	return effectedSpaces

# Return a list of all special spaces command's range
# Return False if any of them are invalid
def attemptGetSpecialSpaces(actorPosition, targetSpace, rng):
	effectedSpaces = []
	
	# For each space in list centered on position, if space will be effected
	# by command targetting position, add space to list of effected
	for offset in rng['specialSpaces']:
		offsetX = targetSpace[0] + offset[0]
		offsetY = targetSpace[1] + offset[1]
		offsetSpace = [offsetX, offsetY]
		
		if not spaceValid(actorPosition, offsetSpace, rng):
			# Space is invalid
			return False
		else:
			unitInSpace = unitControl.get.inSpace(offsetSpace) != None

			if unitInSpace:
				# Space is occupied
				return False
			else:
				effectedSpaces.append(offsetSpace)
	
	return effectedSpaces

# Return a list of units in the given spaces
def getEffectedUnits(effectedSpaces):
	effectedUnits = []
	
	# For each space effected by command, add any units on it to list of effected units
	for space in effectedSpaces:
		
		unit = unitControl.get.inSpace(space)
		if unit is not None:
			effectedUnits.append(unit)
	
	return effectedUnits
