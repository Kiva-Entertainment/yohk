# Add unit to time list at next turn when unit acts
# Units act sooner/more often if they have higher speed
from bge import logic

from script.time import displayTurnOrder

def unitAction(unit):
	time = logic.globalDict['time']

	# If unit has no/negative speed, it cannot act
	if unit['speed'] <= 0:
		return

	# The turn number of the first turn in which unit acts
	turnNumber = 100 - unit['speed']
	if turnNumber < 1:
		turnNumber = 1

	turn = time[turnNumber]

	# Turns are divided into each alignment
	# Add unit to the group that matchs its alignment
	addUnitToAlignGroup(unit, turn)

	time[turnNumber] = turn

	displayTurnOrder.do()

# Add unit to the group within turn that matchs unit's alignment
def addUnitToAlignGroup(unit, turn):
	unitAdded = False

	# Find group with same align as unit and add unit to that group
	# If group doesn't yet exist, add new group below
	for i in range(0, len(turn)):

		group = turn[i]
		# Get first unit because there will be at least 1 and all grouped unit share align
		groupAlign = group[0]['align']

		if groupAlign == unit['align']:
			# Return turn with the unit added to correct group
			turn[i].append(unit)
			unitAdded = True

	# If unit wasn't added, its group doesn't exist yet
	# Add unit in new group
	if not unitAdded:
		newGroup = [unit]
		# NOTE(kgeffen) Prepend so that order of teams switchs after each split turn
		# Ex: Team A -> Team B first turn, teamB -> Team A second turn
		turn.insert(0, newGroup)

