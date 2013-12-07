# Create all units that start on the field and store their data in globalDict['units']
from bge import logic

from script import sceneControl, getPosition

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
		
		# Create unit in correct position
		obj = addUnitObject(unit)
		
		# Change units mesh to correct value
		modelType = unit['model']
		
		loadUnitMesh(modelType)
		
		obj.replaceMesh(modelType)

# Add a unit object to battlefield based on its data
# Return the object added
def addUnitObject(unit):
	battlefield = sceneControl.get('battlefield')
	
	# Add a unit object to field
	obj = battlefield.addObject('unit', 'ground')
	
	# Move unit to correct position based on its data
	position = getPosition.onGround(unit['position'])
	obj.worldPosition = position
	
	return obj

# Load the given unit model into bge memory so that it can be used
def loadUnitMesh(model):
	filepath = logic.expandPath('//models/characters/') + model + '.blend'
	
	# Don't add the library if it exists already!
	if filepath not in logic.LibList():
		logic.LibLoad(filepath, 'Mesh')
