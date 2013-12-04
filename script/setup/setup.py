# Handles all setup for game
from bge import logic

from script import objectControl, setup, time
from script.cursor.motion import setup as cursorSetup

def attempt(cont):
	if cont.sensors['start'].positive:
		do()

def do():
	# TODO(kgeffen) Remove once stage selection has been enabled
	setup.tempFilepathCreation.do()
	
	# TODO(kgeffen) Remove once these variables are instantiated at game startup,
	# not battlefield startup
	setup.globalVariables.do()
	
	setup.ground.do()
	setup.units.do()
	setup.scenes.do()
	
	# This triggers the below method on next tic
	ground = objectControl.getFromScene('ground', 'battlefield')
	ground.sendMessage('secondSetup')

# Some setup has to occur a tic after the above setup, that happens here
def attemptSecondSetup(cont):
	if cont.sensors['message'].positive:
		doSecondSetup()

def doSecondSetup():
	time.setup.do()
	
	# Move cursor to be on ground
	# NOTE(kgeffen) This relies on height display existing, so it must be done after
	# overlay scene added
	cursorSetup.do()
	
	setup.scenes.hideBackground()
