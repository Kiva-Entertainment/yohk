# Scripts relating to interacting with game objects

# Used throughout other scripts
from bge import logic

ACTIVE_STATE = logic.KX_STATE1
INACTIVE_STATE = logic.KX_STATE2

# Get the game object for a given unit
def getUnit(unit):
	# NOTE(kgeffen) Must import here (not above) so circular importing doesn't happen
	from script import sceneControl, check
	
	scene = sceneControl.get('battlefield')

	# Get the object that is a 'unit' and has matching position
	for obj in scene.objects:
		if obj.name == 'unit':

			objPosition = obj.worldPosition
			if check.eq2D(objPosition, unit['position']):
				return obj

# Get a given object from a given scene
def getFromScene(objectName, sceneName):
	for scene in logic.getSceneList():
		if scene.name == sceneName:
			return scene.objects[objectName]

# Makes object invisible and changes it to an inactive state
def hide(object):
	object.state = INACTIVE_STATE
	object.setVisible(False)

# Makes object visible and changes it to an active state
def show(object):
	object.state = ACTIVE_STATE
	object.setVisible(True)
