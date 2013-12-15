# Add unit to time list at next turn when unit acts
# Units act sooner/more often if they have higher speed
from bge import logic

from script.time import displayTurnOrder

def unitAction(unit):
	# If unit has no/negative speed, it cannot act
	if unit['speed'] <= 0:
		return

	# The number of tics between each of unit's actions
	ticsBetween = round(100/unit['speed'])
	
	# Next action should never be added to current turn (Turn 0)
	firstTurnNumber = ticsBetween
	if ticsBetween == 0:
		firstTurnNumber = 1

	addUnitToTurn(unit, firstTurnNumber)

	displayTurnOrder.do()


def addUnitToTurn(unit, turnNumber):
	time = logic.globalDict['time']

	turn = time[turnNumber]

	# Turns are divided into each alignment
	# Add unit to the group that matchs its alignment
	addUnitToAlignGroup(unit, turn)

	time[turnNumber] = turn

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

