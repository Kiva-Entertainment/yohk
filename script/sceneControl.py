# Various methods for dealing with scenes

# Called by many scripts
from bge import logic

from script import objectControl

# Get the scene with the given name
# Scene must be in scene list (Can be suspended)
def get(sceneName):
	for scene in logic.getSceneList():
		if scene.name == sceneName:
			return scene

# Suspend scene(s)
def suspend(*scenes):
	for scene in logic.getSceneList():
		if scenes.count(scene.name) != 0:
			scene.suspend()

# Resume scene(s)
def resume(*scenes):
	for scene in logic.getSceneList():
		if scenes.count(scene.name) != 0:
			scene.resume()

# Make all objects in given scene(s) invisible/inactive
def hide(*scenes):
	for scene in logic.getSceneList():
		if scenes.count(scene.name) != 0:
			hideObjectsInScene(scene)

# Make all objects in given scene(s) visible/active
def show(*scenes):
	for scene in logic.getSceneList():
		if scenes.count(scene.name) != 0:
			showObjectsInScene(scene)


# Make all objects in scene invisible/inactive
def hideObjectsInScene(scene):
	for object in scene.objects:
		objectControl.hide(object)

# Make all objects in scene visible/active
def showObjectsInScene(scene):
	for object in scene.objects:
		objectControl.show(object)
