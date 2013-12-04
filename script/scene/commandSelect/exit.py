# Exit the 'commandSelect' scene and return to the battlefield with actor selected
from bge import logic

from script import sceneControl, objectControl

def attempt(cont):
	if cont.sensors['wKey'].positive:
		do()

def do():
	sceneControl.resume('battlefield')
	sceneControl.show('battlefieldOverlay')
	sceneControl.hide('commandSelect')
	
	# When exiting without selecting an action
	# selected unit must be selected again
	reselectActor()


def reselectActor():
	logic.globalDict['cursor'] = 'selecting'
	sendMessageToBattlefield('selectUnit')

def sendMessageToBattlefield(message):
	# Sender must be in same scene (battlefield) as receiver of message
	# Sender object is arbitrarily 'ground'
	object = objectControl.getFromScene('ground', 'battlefield')
	object.sendMessage(message)
