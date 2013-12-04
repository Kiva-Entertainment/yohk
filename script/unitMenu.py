# Methods called by menuMain
from bge import logic

from script import sceneControl, objectControl, marker

# Display the unit's info
def info(cont):
	# TODO(kgeffen) Fix info scene
	return
	
	if cont.sensors['downKey'].positive:
		sceneControl.show('info')
		sceneControl.hide('battlefieldOverlay')
		sceneControl.suspend('battlefield')

# Change target to select a space for the unit to move to
def move(cont):
	if cont.sensors['upKey'].positive:
		logic.globalDict['cursor'] = 'move'
		
		# Hide unitMenu
		menu = objectControl.getFromScene('unitMenu', 'battlefield')
		objectControl.hide(menu)
		
		sceneControl.hide('basicInfo')

# Change to action select
def skill(cont):
	if cont.sensors['leftKey'].positive:
		# Clear all movement range markers
		marker.clear()
		
		# Hide the unit menu
		menu = objectControl.getFromScene('unitMenu', 'battlefield')
		objectControl.hide(menu)
		
		sceneControl.show('commandSelect')
		sceneControl.hide('battlefieldOverlay', 'basicInfo')
		sceneControl.suspend('battlefield') # Battlefield is still visible
