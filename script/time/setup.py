# Create starting time array
# Called from setup scripts
from bge import logic

from script.time import churn

# Number of entries in time array
# NOTE(kgeffen) Add 1 because turn[0] is current turn,
# and a unit with speed 1 would need to be put in turn 100 (0 + 100)
QUANTITY_ENTRIES = 100 + 1

# Create the starting time array, store it in globalDict
def primary():
	timeArray = []
	
	# Give timeArray appropriate number of entries
	for i in range(0, QUANTITY_ENTRIES):
		timeArray.append([])
	
	logic.globalDict['time'] = timeArray

# Ensure time starts with a turn that has actors
def secondary():
	noActors = logic.globalDict['time'][0] == []
	if noActors:
		churn.do()
