# Add unit to timeArray at next turn when unit acts
# Units act sooner/more often if they have higher speed
from bge import logic

def unitAction(unit, timeArray):
	# If unit has no/negative speed, it cannot act
	if unit['speed'] <= 0:
		return

	# The turn number of the first turn in which unit acts
	turnNumber = 100 - unit['speed']
	turn = timeArray[turnNumber]

	# Turns are divided into each alignment
	# Add unit to the group that matchs its alignment
	turn = addUnitToAlignGroup(unit, turn)

	timeArray.append(turn)

	print(timeArray)


# Add unit to the group within turn that matchs unit's alignment
def addUnitToAlignGroup(unit, turn):
		# Find group with same align as unit and add unit to that group
		# If group doesn't yet exist, add new group below
		for i in range(0, len(turn)):

			group = turn[i]
			# Get first unit because there will be at least 1 and all grouped unit share align
			groupAlign = group[0]['align']

			if groupAlign == unit['align']:
				# Return turn with the unit added to correct group
				return turn[i].append(unit)

		# If turn was not returned in above, group must not yet exist
		newGroup = [unit]
		return turn.append(newGroup)


