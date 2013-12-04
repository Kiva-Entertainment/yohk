# Actions relating to camera
MAX_ZOOM = 170
MIN_ZOOM = 15
ZOOM_INCREMENT = 2

def zoom(cont):
	own = cont.owner

	qKey = cont.sensors["qKey"].positive
	eKey = cont.sensors["eKey"].positive
	
	# Return if trying to zoom in and out at same time
	if qKey and eKey:
		return
	
	if qKey and own.lens < MAX_ZOOM:
		own.lens += ZOOM_INCREMENT

	elif eKey and own.lens > MIN_ZOOM:
		own.lens -= ZOOM_INCREMENT
