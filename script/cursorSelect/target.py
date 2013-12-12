# Attempt to perform command on target cursor is selecting
from script.command import perform

def attempt():
	# Success true even if command misses,
	# False if not valid target
	success = perform.attempt()
	
	if success:
		pass
		#utility.playSound('attack')
	
	else:
		pass
		#utility.playSound('negative')
