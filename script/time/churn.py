# Churn through entries in time until turn with actors comes up
from bge import logic

from script.time import addNext, upkeep, displayTurnOrder, cleanup

# Number of entries in time array
# NOTE(kgeffen) Add 1 because turn[0] is current turn,
# and a unit with speed 1 would need to be put in turn 100 (0 + 100)
QUANTITY_ENTRIES = 100 + 1

def attempt(cont):
	if cont.sensors['xKey'].positive:
		do()

		# Also perform cleanup between turns
		cleanup.do()

def do():
	time = logic.globalDict['time']
	
	turnHasActors = time[0] != []
	if turnHasActors:
		# Remove the actors that just acted from time
		# time[0] is current turn, first entry in it is first group of units
		actors = time[0].pop(0)

		# Units that just acted must be added to time again
		# Also, they each have an upkeep
		for unit in actors:
			upkeep.unit(unit)
			addNext.unitAction(unit)

	churnUntilTurnWithActor(time)

	# Reset log of unit movement
	logic.globalDict['moveLog'] = []

	displayTurnOrder.do()


# Remove turns with no actors until current turn has actor(s)
def churnUntilTurnWithActor(time):
	# NOTE(kgeffen) while(true) but less hazardous
	for i in range (0, QUANTITY_ENTRIES):
		
		noActors = time[0] == []
		if noActors:
			time.pop(0)
			time.append([])
		else:
			# Current turn has actors
			return

