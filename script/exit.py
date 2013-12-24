# Do anything necessary before game ends
from bge import logic

from script import soundControl

def attempt(cont):
	if cont.sensors['exitKey'].positive:
		do()

# Exit the game
def do():
	# Ensure all sound handles are closed
	soundControl.exit()

	logic.endGame()
