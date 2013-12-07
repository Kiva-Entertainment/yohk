# Create all units that start on the field and store their data in globalDict['units']
from bge import logic

from script import unitControl

def do():
	filepath = logic.globalDict['stageFilepath']
	
	setupUnitData(filepath)
	createUnits()

# Store unit data loaded from file in stage's dir
def setupUnitData(filepath):
	with open(filepath + 'unitData.py') as unitsFile:
		# TODO(kgeffen) This is tamperable, improve means of loading/storing data
		logic.globalDict['units'] = eval(unitsFile.read())

# Create all of the unit objects that exist on battlefield
def createUnits():
	for unit in logic.globalDict['units']:
		unitControl.object.add(unit)

