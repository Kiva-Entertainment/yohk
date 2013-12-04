# Get various kinds of active units and return in format:
# {'number' : c, 'data' : {DATA}}
from bge import logic

from script import check

# The unit currently performing a command
def actor():
	unitNumber = logic.globalDict['selected']
	data = logic.globalDict['units'][unitNumber]
	
	actor = {'number' : unitNumber,
			 'data' : data}
	
	return actor

# The unit in a given space
def inSpace(space):
	for unit in allUnits():
		
		if check.eq2D(unit['data']['position'], space):
			return unit

# List of all units
def allUnits():
	unitList = []
	
	for unit in logic.globalDict['units'].items():
		
		formattedUnit = {'number' : unit[0],
						'data' : unit[1]}
						
		unitList.append(formattedUnit)
	
	return unitList
