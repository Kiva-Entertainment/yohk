# Common types of range for commands (Ex: cardinal)
# Called by commands.py
from bge import logic
from script.command import markSpaceValid
from script import getPosition

# Range is free - It is not bound by actor's rotation
# Ex: Fireball which hits a unit within 2 spaces of actor
def free(rng):
	actorPosition = getPosition.actor()

	# targetOffset - Offset from actor in form [x,y]
	for targetOffset in rng['range']:
		targetX = actorPosition[0] + targetOffset[0]
		targetY = actorPosition[1] + targetOffset[1]
		targetSpace = [targetX, targetY]

		markSpaceValid.attempt(actorPosition, targetSpace, rng)

# Range is rigid - It rotates in each of 4 cardinal directions
# Ex: Large sword slash which hits units up to 3 spaces away in line from actor
def rigid(rng):
	actorPosition = getPosition.actor()
	
	# Point in each of 4 cardinal directions
	# NOTE(kgeffen) Start with space rotated by quarter circle from front,
	# go to space rotated by half circle, etc.
	# Order matters!
	for dv in ([1, 0], [0, -1], [-1, 0], [0, 1]):

		# Rotate range by 90 degrees
		# Ex: special space [2,0] becomes [0,-2]
		rotateRange(rng)
		
		# targetOffset - Offset from space on given side of actor (space = actorPosition + dv)
		for targetOffset in rng['range']:
			targetX = actorPosition[0] + targetOffset[0] + dv[0]
			targetY = actorPosition[1] + targetOffset[1] + dv[1]
			targetSpace = [targetX, targetY]

			markSpaceValid.attempt(actorPosition, targetSpace, rng)

'Utilities'
# Rotate each space in command's range (aoe, specials, range) by 90
def rotateRange(rng):
	rng['range'] = rotateEachBy90(rng['range'])
	rng['aoe'] = rotateEachBy90(rng['aoe'])
	rng['specialSpaces'] = rotateEachBy90(rng['specialSpaces'])

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
