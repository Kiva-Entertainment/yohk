# Create all units that start on the field and store their data in globalDict['units']
from bge import logic

from script import sceneControl, unitControl, getPosition

def do():
	filepath = logic.globalDict['stageFilepath']
	
	setupUnitData(filepath)
	createUnits()

# Store unit data loaded from txt in stage's dir
def setupUnitData(filepath):
	with open(filepath + 'unitData.txt') as unitsFile:
		# TODO(kgeffen) This is tamperable, improve means of loading/storing data
		logic.globalDict['units'] = eval(unitsFile.read())

# Create all of the unit objects that exist on battlefield
def createUnits():
	for unit in unitControl.get.allUnits():
		
		# Create unit in correct position
		obj = addUnitObject(unit)
		
		# Change units mesh to correct value
		modelType = unit['data']['model']
		
		loadUnitMesh(modelType)
		
		obj.replaceMesh(modelType)

# Add a unit object to battlefield based on its data
# Return the object added
def addUnitObject(unit):
	battlefield = sceneControl.get('battlefield')
	
	# Add the unit as an instance of the object with name = unitNumber
	# Ex: unitNumber 3 adds a preexisting object named 3
	obj = battlefield.addObject(str(unit['number']), 'ground')
	
	# Move unit to correct position based on its data
	position = getPosition.onGround(unit['data']['position'])
	obj.worldPosition = position
	
	return obj

# Load the given unit model into bge memory so that it can be used
def loadUnitMesh(model):
	filepath = logic.expandPath('//models/characters/') + model + '.blend'
	
	# Don't add the library if it exists already!
	if filepath not in logic.LibList():
		logic.LibLoad(filepath, 'Mesh')
