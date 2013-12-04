# Returns dictionary for common ranges such as weapons
# Called by commands.py
from script.command.generic import areaOfEffect

# The overall standard for any command that doesn't fit into any of the below
def standard():
	return {'okDz' : {'max' : 1.2, 'min' : -1.2},
			'reach' : 1,
			'aoe' : areaOfEffect.single(),
			'specialSpaces' : []}

# For commands that center on self
def self():
	return {'okDz' : {'max' : 1.0, 'min' : -1.0},
			'reach' : 0,
			'aoe' : areaOfEffect.single(),
			'specialSpaces' : []}

'Weapons'
def spear():
	return {'okDz' : {'max' : 1.2, 'min' : -1.2},
			'reach' : 2,
			'aoe' : areaOfEffect.single(),
			'specialSpaces' : []}

def sword():
	return {'okDz' : {'max' : 1.2, 'min' : -1.2},
			'reach' : 1,
			'aoe' : areaOfEffect.single(),
			'specialSpaces' : []}

def axe():
	return {'okDz' : {'max' : 1.2, 'min' : -1.2},
			'reach' : 1,
			'aoe' : areaOfEffect.single(),
			'specialSpaces' : []}

def dagger():
	return {'okDz' : {'max' : 1.2, 'min' : -1.2},
			'reach' : 1,
			'aoe' : areaOfEffect.single(),
			'specialSpaces' : []}

'Other'
