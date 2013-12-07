# Returns dictionary for common factors such as weapons
# Called by commands.py

'Weapons'
def spear(actor, target):
	return {'force' : actor['strength']/2 + actor['focus']/2,
	 		'resist' : target['toughness'],
	 		'accuracy' : actor['focus'],
	 		'evasion' : target['agility']}

def sword(actor, target):
	return {'force' : actor['strength'],
	 		'resist' : target['toughness'],
	 		'accuracy' : actor['focus'],
	 		'evasion' : target['agility']}

def axe(actor, target):
	return {'force' : actor['strength'] * 1.1,
			'resist' : target['toughness'],
			'accuracy' : actor['focus'] * 0.9,
			'evasion' : target['agility']}

def dagger(actor, target):
	return {'force' : actor['agility'] * 0.5 + actor['focus'] * 0.5,
			'resist' : target['toughness'],
			'accuracy' : actor['focus'],
			'evasion' : target['agility']}

'Other'
def magic(actor, target):
	return {'force' : actor['intelligence'],
			'resist' : target['willpower'],
			'accuracy' : actor['focus'],
			'evasion' : target['agility']}
