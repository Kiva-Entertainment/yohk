# Scripts relating to interacting with game objects for units
# Used throughout other scripts
from bge import logic

from script import check, sceneControl, getPosition, time

# Get the game object for a given unit
def get(unit):
	scene = sceneControl.get('battlefield')

	# Get the object that is a 'unit' and has matching position
	for obj in scene.objects:
		if obj.name == 'unit':
			
			objPosition = obj.worldPosition
			if check.eq2D(objPosition, unit['position']):
				return obj

# Add the unit specified by given unit to battlefield and store its data in gd
def add(unit):
	# Add data for unit to globalDict
	logic.globalDict['units'].append(unit)

	# Create game object
	obj = createGameObject(unit)
	switchMesh(obj, unit['model'])

	# Add first turn to time
	time.addNext.unitAction(unit)


# Create a game object for given unit at unit's position
def createGameObject(unit):
	battlefield = sceneControl.get('battlefield')

	# Add game object
	obj = battlefield.addObject('unit', 'ground')

	# Adjust objects position to match data
	obj.worldPosition = getPosition.onGround(unit['position'])

	return obj

# Switch given unit game object's mesh to match given model type
def switchMesh(obj, model):
	# Load mesh into memory only if it isn't already loaded
	filepath = logic.expandPath('//models/') + model + '.blend'
	if filepath not in logic.LibList():
		logic.LibLoad(filepath, 'Mesh')
	
	# Switch objects mesh
	obj.replaceMesh(model)

