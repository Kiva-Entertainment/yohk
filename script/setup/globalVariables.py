# Create all remaining global variables that are used in scripts
# TODO(kgeffen) Remove once these variables are instantiated at game startup,
# not battlefield startup
from bge import logic

# Create remaining used global variables
def do():
	logic.texture = {}
	logic.globalDict['infoLists'] = [[],[],[]]
	logic.globalDict['units'] = []
	# A list of choices for current command
	logic.globalDict['commandChoices'] = []
	# Units that haven't been deployed from base yet
	logic.globalDict['inactiveUnits'] = []
	logic.globalDict['actor'] = None
	logic.globalDict['described'] = None
	logic.globalDict['cursor'] = 'selecting'
	logic.globalDict['spaceTarget'] = []
	logic.globalDict['validMove'] = [] # Dictionary of spaces and dMv for current unit
	logic.globalDict['commandResults'] = []
	logic.globalDict['commandSpecialSpaces'] = []
	logic.globalDict['extent'] = 0
	# List of all moves since last turn change/action
	# Entries in the form:
	# {'unit' : unit, 'start' : starting_space, 'mv' : mv_before_move_performed}
	logic.globalDict['moveLog'] = []
