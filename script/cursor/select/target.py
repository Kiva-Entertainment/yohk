# Attempt to perform command on target cursor is selecting
# Clear markers if command was performed
from script import marker
from script.command import perform

def attempt():
	# Success true even if command misses,
	# False if not valid target
	success = perform.attempt()
	
	if success:
		marker.clear()
		marker.clear('markerAoe') # Clear any aoe markers
		#utility.playSound('attack')
	
	else:
		pass
		#utility.playSound('negative')
