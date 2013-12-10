# Create all units that start on the field and store their data in globalDict['units']
from bge import logic

from script import unitControl

# TODO(kgeffen) Unit loading will change drastically (Probably in version 0.5)
# Until then, scaffolding is acceptable
def do():
	filepath = logic.globalDict['stageFilepath']
	
	unitData = getUnitData(filepath)

	# Add active units to field
	for unit in unitData['active']:
		unitControl.object.add(unit)

	# Add inactive units to list
	for unit in unitData['inactive']:
		logic.globalDict['inactiveUnits'].append(unit)

# Store unit data loaded from file in stage's dir
def getUnitData(filepath):
	with open(filepath + 'unitData.py') as unitsFile:
		# TODO(kgeffen) This is tamperable, improve means of loading/storing data
		return eval(unitsFile.read())

