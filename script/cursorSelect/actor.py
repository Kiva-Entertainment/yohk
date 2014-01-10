# Open commandSelect screen for selected unit if it has actions left
from bge import logic

from script import sceneControl, soundControl, marker

def attempt():
	actor = logic.globalDict['actor']

	if actor['act'] > 0:
		do()
	else:
		soundControl.play('negative')

def do():
	# Clear all movement range markers
	marker.clearMoveMarkers()
	
	sceneControl.show('commandSelect')
	sceneControl.hide('battlefieldOverlay', 'basicInfo')
	sceneControl.suspend('battlefield') # Battlefield is still visible
