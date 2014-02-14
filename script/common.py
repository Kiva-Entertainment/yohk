# Commonly used methods
from bge import logic

def unitInSpace(space):
	''' Get the unit in given space, if any '''
	for unit in logic.globalDict['units']:
		if round(space[0]) == round(unit.position[0]):
			if round(space[1]) == round(unit.position[1]):
				return unit
