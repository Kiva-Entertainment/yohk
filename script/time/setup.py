# Create starting time array
# Called from setup scripts
from bge import logic

from script.time import churn

# Number of entries in time array
QUANTITY_ENTRIES = 100

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
