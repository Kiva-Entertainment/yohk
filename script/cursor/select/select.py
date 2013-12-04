# Call other select modules based on what type of selection is being made
# Ex: Command target, space to move to, unit to inspect/act
from bge import logic

from script.cursor import select

def attempt(cont):
	spaceKey = cont.sensors['spaceKey'].positive
	messaged = cont.sensors['selectMessage'].positive
	
	if spaceKey or messaged:
		do()

def do():
	# The type of selection being made
	status = logic.globalDict['cursor']
	
	if status == 'selecting':
		select.unit.attempt()
	
	elif status == 'move':
		select.move.attempt()
		
	elif status != 'wait':
		# Selecting the target for a command
		select.target.attempt()
