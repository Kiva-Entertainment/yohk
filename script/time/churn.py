# Churn through entries in time until turn with actors comes up
from bge import logic

from script.time import addNext, upkeep

# Number of entries in time array
QUANTITY_ENTRIES = 100

def attempt(cont):
	if cont.sensors['xKey'].positive:
		do()

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

