# Common types of range for commands (Ex: cardinal)
# Called by commands.py
from bge import logic
from script.command import markSpaceValid
from script import getPosition

# TODO(kgeffen) Duplicate code exists between this script and generic.areaOfEffect
# Change aoe to be list of spaces, and these methods should use those lists instead of generating their own
# Many methods here will become unnecessary - Probably only rigid/no will remain

'Common types of range'
# self is only valid target
def self(rng):
	actorPosition = getPosition.actor()
	targetPosition = actorPosition
	
	# NOTE(kgeffen) Command is centered on self, but could be larger than 1 space
	# Ex: Plus sign centered on space
	markSpaceValid.attempt(actorPosition, targetPosition, rng)

# Single target within _reach_ spaces of actor
# Actor is not valid target
def basic(rng):
	actorPosition = getPosition.actor()
	
	# Describes space in rings of radius r
	for r in range(1, rng['reach'] + 1):
		
		# mag(dx) + mag(dy) = r
		for dx in range(-r, r + 1):
			dyMag = r - abs(dx)
			
			# Do for positive and negative dy
			# NOTE(kgeffen) negative dx already covered in above loop
			for dy in set([-dyMag, dyMag]):
				x = actorPosition[0] + dx
				y = actorPosition[1] + dy
				targetSpace = [x,y]
				
				markSpaceValid.attempt(actorPosition, targetSpace, rng)

# Single target within _reach_ spaces along actor's viewline (cardinal)
# Actor is not valid target
def cardinal(rng):
	actorPosition = getPosition.actor()
	
	# Describe space in lines of length between 1 and range
	for l in range(1, rng['reach'] + 1):
		
		# Point in each of 4 cardinal directions
		for dv in ([0, l], [0, -l], [l, 0], [-l, 0]):
			x = actorPosition[0] + dv[0]
			y = actorPosition[1] + dv[1]
			targetSpace = [x,y]
			
			markSpaceValid.attempt(actorPosition, targetSpace, rng)

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

