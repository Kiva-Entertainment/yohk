# Actions relating to camera
from mathutils import Vector

MAX_ZOOM = 0.1
MIN_ZOOM = 5
ZOOM_INCREMENT = 0.05

def zoom(cont):
	own = cont.owner

	qKey = cont.sensors["qKey"].positive
	eKey = cont.sensors["eKey"].positive
	
	# Return if trying to zoom in and out at same time
	if qKey and eKey:
		return
	
	if qKey and own.localScale.x > MAX_ZOOM:
		# Zoom in
		own.localScale *= 1 - ZOOM_INCREMENT

	elif eKey and own.localScale.x < MIN_ZOOM:
		# Zoom out
		own.localScale *= 1 + ZOOM_INCREMENT
