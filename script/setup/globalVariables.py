# Create all remaining global variables that are used in scripts
# TODO(kgeffen) Remove once these variables are instantiated at game startup,
# not battlefield startup
from bge import logic

# Create remaining used global variables
def do():
	logic.texture = {}
	logic.globalDict['infoLists'] = [[],[],[]]
	logic.globalDict['selected'] = None
	logic.globalDict['cursor'] = 'selecting'
	logic.globalDict['spaceTarget'] = []
	logic.globalDict['validMove'] = [] # Dictionary of spaces and dMv for current unit
	logic.globalDict['commandResults'] = []
	logic.globalDict['commandSpecialSpaces'] = []
	logic.globalDict['extent'] = 0
