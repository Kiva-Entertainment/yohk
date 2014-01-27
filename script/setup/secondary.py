# Perform setup necessary on second tic
from script import objectControl, setup, time

# Some setup has to occur a tic after the above setup, that happens here
def attempt(cont):
	if cont.sensors[0].positive:
		do()

def do():
	# NOTE(kgeffen) Overlay scene must exist before units added to time so that they can be displayed
	# NOTE(kgeffen) Time array must exist before units are added so that they can be added to it
	time.setup()

	setup.units.do()

	setup.scenes.secondary()
