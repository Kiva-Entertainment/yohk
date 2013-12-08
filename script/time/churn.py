# Churn through entries in time until turn with actors comes up
from bge import logic

from script.time import addNext, upkeep, displayTurnOrder

# Number of entries in time array
QUANTITY_ENTRIES = 100

def attempt(cont):
	if cont.sensors['xKey'].positive:
		do()

def do():
	time = logic.globalDict['time']
	
	# Churn the turn that just finished
	lastActors = churnSingle(time)
	
	# Units that just acted must be added to time again
	# Also, they each have an upkeep
	for unit in lastActors:
		upkeep.unit(unit)
		addNext.unitAction(unit, time)
	
	churnUntilTurnWithActor(time)
	
	displayTurnOrder.do()


# Remove turns with no actors until current turn has actor(s)
def churnUntilTurnWithActor(time):
	# NOTE(kgeffen) while(true) but less hazardous
	for i in range (0, QUANTITY_ENTRIES):
		
		noActors = time[0] == []
		if noActors:
			churnSingle(time)
		else:
			# Current turn has actors
			return

# Remove current turn and add a blank turn on at end
# Returns turn removed
def churnSingle(time):

	turnHasActors = time[0] != []
	if turnHasActors:
		# Remove the first group from first turn
		churned = time[0].pop(0)
	else:
		# Else, no units were churned
		churned = []

	# If first turn is now empty, remove entire turn
	# and add one at end to maintain size
	if time[0] == []:
		time.pop(0)
		time.append([])

	# Return removed group
	return churned


