# Exit the info scene and return to battlefield
from script import sceneControl

# Exit the Info scene
def attempt(cont):
	if cont.sensors['wKey'].positive:
		do()

def do():
	sceneControl.resume('battlefield')
	sceneControl.show('battlefieldOverlay', 'basicInfo')
	sceneControl.hide('info')

