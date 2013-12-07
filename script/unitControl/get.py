# Get unit data for unit(s) based on various conditions
from bge import logic

from script import check

# The unit currently performing a command
def actor():
	unit = logic.globalDict['selected']
	return unit

# The unit in a given space
def inSpace(space):
	for unit in allUnits():
		
		if check.eq2D(unit['position'], space):
			return unit

# List of all units
def allUnits():
	unitList = []
	
	for unit in logic.globalDict['units']:
		unitList.append(unit)
	
	return unitList
