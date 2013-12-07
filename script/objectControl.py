# Scripts relating to interacting with game objects

# Used throughout other scripts
from bge import logic

ACTIVE_STATE = logic.KX_STATE1
INACTIVE_STATE = logic.KX_STATE2

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
