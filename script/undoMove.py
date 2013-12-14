# Undo last unit movement made, assuming that any have been made
# since turn switch/command was performed
from bge import logic

from script.unitControl import move

def attempt():
	endOfLog = len(logic.globalDict['moveLog']) == 0
	if not endOfLog:
		do()

def do():
	lastMove = logic.globalDict['moveLog'].pop()

	unit = lastMove['unit']
	oldSpace = lastMove['start']
	oldMv = lastMove['mv']

	# Move unit
	move.toSpace(unit, oldSpace)

	# Return unit's mv to previous amount
	unit['mv'] = oldMv
