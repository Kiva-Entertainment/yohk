# Handles all setup for game
from bge import logic

from script import setup

def attempt(cont):
	if cont.sensors['start'].positive:
		do()

def do():
	# TODO(kgeffen) Remove once these variables are instantiated at game startup,
	# not battlefield startup
	setup.globalVariables.do()
	
	# Setup the ground and all its vars
	setup.ground.do()

	# Primary setup for scenes
	setup.scenes.primary()

	setup.cursor.do()
