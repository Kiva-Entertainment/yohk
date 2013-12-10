# Rotate cursor +/- 90 degrees based on which key was pressed
from math import pi

from script import objectControl

def attempt(cont):
	cursor = objectControl.getFromScene('cursor', 'battlefield')
	
	aKey = cont.sensors['aKey'].positive
	dKey = cont.sensors['dKey'].positive
	
	if aKey:
		cursor.applyRotation([0.0, 0.0, -pi/2])
	
	elif dKey:
		cursor.applyRotation([0.0, 0.0, pi/2])
