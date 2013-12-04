# Returns dictionary for common factors such as weapons
# Called by commands.py

'Weapons'
def spear(actor, target):
	return {'force' : actor['data']['strength']/2 + actor['data']['focus']/2,
	 		'resist' : target['data']['toughness'],
	 		'accuracy' : actor['data']['focus'],
	 		'evasion' : target['data']['agility']}

def sword(actor, target):
	return {'force' : actor['data']['strength'],
	 		'resist' : target['data']['toughness'],
	 		'accuracy' : actor['data']['focus'],
	 		'evasion' : target['data']['agility']}

def axe(actor, target):
	return {'force' : actor['data']['strength'] * 1.1,
			'resist' : target['data']['toughness'],
			'accuracy' : actor['data']['focus'] * 0.9,
			'evasion' : target['data']['agility']}

def dagger(actor, target):
	return {'force' : actor['data']['agility'] * 0.5 + actor['data']['focus'] * 0.5,
			'resist' : target['data']['toughness'],
			'accuracy' : actor['data']['focus'],
			'evasion' : target['data']['agility']}

'Other'
def magic(actor, target):
	return {'force' : actor['data']['intelligence'],
			'resist' : target['data']['willpower'],
			'accuracy' : actor['data']['focus'],
			'evasion' : target['data']['agility']}
