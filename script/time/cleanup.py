# Perform any cleanup necessary after turn ends
# NOTE(kgeffen) Closely mimics deselect.py
from bge import logic

from script import marker

# NOTE(kgeffen) Cleanup from selecting command target includes cleanup from
# selecting space to move to


def do():
	status = logic.globalDict['cursor']

	# Reset log of unit movement
	logic.globalDict['moveLog'] = []

	if status == 'selecting':
		return

	elif status == 'move':
		cleanupFromMovement()

	else:
		cleanupFromTargetSelect()

# Cleanup from selecting space for unit to move to
def cleanupFromMovement():
	logic.globalDict['cursor'] = 'selecting'
	logic.globalDict['actor'] = None
	logic.globalDict['extent'] = 0
	logic.globalDict['commandChoices'] = []
	
	# NOTE(kgeffen) Clear because movement range markers added when unit is reselected
	marker.clearMoveMarkers()

# Cleanup from selecting command target
def cleanupFromTargetSelect():
	# Clear data about which spaces can be targetted
	logic.globalDict['spaceTarget'] = []

	# Any cleanup that happens when turn ends while unit is selecting a space to move to
	# also has to happen when turn ends while cursor is selecting a target
	cleanupFromMovement()
