# Move actor to selected space if move is allowed
from bge import logic

from script import check, objectControl, marker, unitControl, soundControl
from script.cursorSelect import unit as selectUnit

def attempt(position):
	if moveAllowed(position):
		do(position)

		soundControl.play('move')

	else:
		soundControl.play('negative')

def do(position):
	unit = logic.globalDict['actor']

	# Remove markers which display unit's range of motion
	marker.clearMoveMarkers()
	
	# Store move in undoList
	# NOTE(kgeffen) Must happen before stats are adjusted (particularly mv)
	storeMove(unit)

	unitControl.move.toSpace(unit, position)
	adjustUnitStats(unit, position)
	
	# Select current unit again
	selectUnit.attempt(position)


# Store the move that is occuring in globalDict 'moveList'
def storeMove(unit):
	start = unit['position']
	mv = unit['mv']

	move = {'unit' : unit,
			'start' : start,
			'mv' : mv}

	logic.globalDict['moveLog'].append(move)

# True if validMove dictionary has a move with same space as 'position'
def moveAllowed(position):
	# If any of the validMoves match position, return True
	for move in logic.globalDict['validMove']:
		validSpace = move['space']
		
		if check.eq2D(validSpace, position):
			return True

# Adjust units data in 'unit' dict, including position
def adjustUnitStats(unit, position):
	# Calculate and store the remaining movement for unit this turn
	dMv = getMovementConsumed(position)
	unit['mv'] -= dMv

# Return the amount of movement consumed by moving to 'position'
def getMovementConsumed(position):
	
	# Search through all valid moves until you find the one performed
	for move in logic.globalDict['validMove']:
		
		# If this was the move made, return the amount of mv it costs
		if check.eq2D(move['space'], position):
			return move['dMv']

