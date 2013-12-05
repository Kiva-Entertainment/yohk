# Common types of range for commands (Ex: cardinal)
# Called by commands.py
from bge import logic
from script.command import markSpaceValid
from script import getPosition

# TODO(kgeffen) Duplicate code exists between this script and generic.areaOfEffect
# Change aoe to be list of spaces, and these methods should use those lists instead of generating their own
# Many methods here will become unnecessary - Probably only rigid/no will remain

# TODO(kgeffen) Describe
def free(rng):
	actorPosition = getPosition.actor()

	# targetOffset - Offset from actor in form [x,y]
	for targetOffset in rng['range']:
		targetX = actorPosition[0] + targetOffset[0]
		targetY = actorPosition[1] + targetOffset[1]
		targetSpace = [targetX, targetY]

		markSpaceValid.attempt(actorPosition, targetSpace, rng)

# TODO(kgeffen) Describe
# Spaces in 4 cardinal directions, up to _length_ spaces away
# Aoe rotates around actor
def rigid(rng):
	actorPosition = getPosition.actor()
	
	# Describe each adjacent space with cardinal unit vector
	# NOTE(kgeffen) Start with space rotated by quarter circle from front,
	# go to space rotated by half circle, etc.
	# Order matters!
	for dv in ([1, 0], [0, -1], [-1, 0], [0, 1]):
		
		# Rotate all aoe spaces by 90 degrees
		# Ex: [2,0] becomes [0,-2]
		rng['aoe'] = rotateEachBy90(rng['aoe'])
		rng['specialSpaces'] = rotateEachBy90(rng['specialSpaces'])
		
		# Describe each magnitude between 1 and _reach_
		for mag in range(1, rng['reach'] + 1):
			x = actorPosition[0] + mag * dv[0]
			y = actorPosition[1] + mag * dv[1]
			targetSpace = [x,y]
			
			markSpaceValid.attempt(actorPosition, targetSpace, rng)


'Utilities'
from mathutils import Matrix, Vector
from math import radians

QUARTER_TURN = Matrix.Rotation(radians(90.0), 2, 'Y')

# Rotate each space by 90, return results
def rotateEachBy90(spaces):
	newSpaces = []
	
	for space in spaces:
		# Must multiply vector, not list, by matrix
		newSpace = Vector(space) * QUARTER_TURN
		
		# Change resulting vector into list with int entries
		newX = round(newSpace[0])
		newY = round(newSpace[1])
		newSpace = [newX, newY]
		
		newSpaces.append(newSpace)
	
	return newSpaces

