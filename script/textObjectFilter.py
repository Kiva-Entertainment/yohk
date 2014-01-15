# Filter text objects so they are not blurry
# Called by text objects once

def attempt(cont):
	if cont.sensors[0].positive:
		cont.owner.resolution = 20
