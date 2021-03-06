# Attempt to perform command on target cursor is selecting
from script import soundControl
from script.command import perform

def attempt(position):
	# Success true even if command misses,
	# False if not valid target
	success = perform.attempt(position)
	
	if success:
		soundControl.play('attack')
	
	else:
		soundControl.play('negative')
