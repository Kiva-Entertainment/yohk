# Called 1 tic after command is selected from 'commandSelect'
# Displays all spaces that command can hit
# Generates a dictionary of units that can be targeted by command
from bge import logic

from script import commandControl

DISPLAY_RANGE_METHOD_NAME = 'displayRange'

def attempt(cont):
	if cont.sensors['message'].positive:
		do()

def do():
	commandName = logic.globalDict['cursor']
	commandControl.displayRange(commandName)
