# Get unit data for unit(s) based on various conditions
from bge import logic

from script import check

# The unit in a given space
def inSpace(space):
	for unit in logic.globalDict['units']:
		
		if check.eq2D(unit['position'], space):
			return unit
