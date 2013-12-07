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
	lastTurn = churnSingle(time)
	
	# Units that just acted must be added to time again
	# Also, they each have an upkeep
	for actor in lastTurn:
		upkeep.unit(actor)
		addNext.unitAction(actor, time)
	
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
	# The turn being removed
	churned = time.pop(0)
	
	# Add on a turn to keep time same size
	time.append([])
	
	# Return removed turn
	return churned
