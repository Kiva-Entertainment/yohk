# Setup the starting environment for commandSelect
from script.scene.commandSelect import setup

def attempt(cont):
	if cont.sensors['startup'].positive:
		setup.screen()
