# Returns dictionary for common ranges such as weapons
# Called by commands.py
from script.command.generic import shapes

# The overall standard for any command that doesn't fit into any of the below
def standard():
	return {'okDz' : {'max' : 10.0, 'min' : -10.0}, # {'max' : 1.2, 'min' : -1.2},
			'range' : shapes.single(),
			'aoe' : shapes.single(),
			'specialSpaces' : []}

# For commands that center on self
def self():
	return {'okDz' : {'max' : 10.0, 'min' : -10.0}, # {'max' : 1.0, 'min' : -1.0},
			'range' : shapes.single(),
			'aoe' : shapes.single(),
			'specialSpaces' : []}

'Weapons'
def spear():
	return {'okDz' : {'max' : 10.0, 'min' : -10.0}, # {'max' : 1.2, 'min' : -1.2},
			'range' : shapes.ring(2),
			'aoe' : shapes.single(),
			'specialSpaces' : []}

def sword():
	return {'okDz' : {'max' : 10.0, 'min' : -10.0}, # {'max' : 1.2, 'min' : -1.2},
			'range' : shapes.single(),
			'aoe' : shapes.single(),
			'specialSpaces' : []}

def axe():
	return {'okDz' : {'max' : 10.0, 'min' : -10.0}, # {'max' : 1.2, 'min' : -1.2},
			'range' : shapes.single(),
			'aoe' : shapes.single(),
			'specialSpaces' : [[0, -2]]}

def bow():
	return {'okDz' : {'max' : 10.0, 'min' : -10.0}, # {'max' : 1.2, 'min' : -1.2},
			'range' : shapes.diamond(5, 1),
			'aoe' : shapes.single(),
			'specialSpaces' : []}

def dagger():
	return {'okDz' : {'max' : 10.0, 'min' : -10.0}, # {'max' : 1.2, 'min' : -1.2},
			'range' : shapes.single(),
			'aoe' : shapes.single(),
			'specialSpaces' : []}

'Magic Elements'
def lightning():
	return {'okDz' : {'max' : 10.0, 'min' : -10.0}, # {'max' : 10, 'min' : -10},
			'range' : shapes.diamond(2, 1),
			'aoe' : shapes.single(),
			'specialSpaces' : []}


'Other'
