# View the info of the unit that cursor is over currently
from bge import logic

from script import sceneControl, objectControl, common

# Display the unit's info
def attempt(cont):
	if cont.sensors['iKey'].positive:
		# Get unit under cursor, if any
		cursor = objectControl.getFromScene('cursor', 'battlefield')
		unit = common.unitInSpace(cursor.worldPosition)

		if unit is not None:
			do(unit)

def do(unit):
	# The unit that the info is about
	logic.globalDict['described'] = unit

	sceneControl.show('info')
	sceneControl.hide('battlefieldOverlay', 'basicInfo')
	sceneControl.suspend('battlefield')

