# Returns dictionary for common factors such as weapons
# Called by commands.py

'Weapons'
def spear(actor, target):
	return {'force' : actor.stats['strength']/2 + actor.stats['focus']/2,
	 		'resist' : target.stats['toughness'],
	 		'accuracy' : actor.stats['focus'],
	 		'evasion' : target.stats['agility']}

def sword(actor, target):
	return {'force' : actor.stats['strength'],
	 		'resist' : target.stats['toughness'],
	 		'accuracy' : actor.stats['focus'],
	 		'evasion' : target.stats['agility']}

def axe(actor, target):
	return {'force' : actor.stats['strength'] * 1.2,
			'resist' : target.stats['toughness'],
			'accuracy' : actor.stats['focus'] * 0.8,
			'evasion' : target.stats['agility']}

def dagger(actor, target):
	return {'force' : actor.stats['agility'] * 0.5 + actor.stats['focus'] * 0.5,
			'resist' : target.stats['toughness'],
			'accuracy' : actor.stats['focus'],
			'evasion' : target.stats['agility']}

def bow(actor, target):
	return {'force' : actor.stats['focus'],
			'resist' : target.stats['toughness'],
			'accuracy' : actor.stats['focus'],
			'evasion' : target.stats['agility']}

'Standard'
def physical(actor, target):
	return {'force' : actor.stats['strength'],
	 		'resist' : target.stats['toughness'],
	 		'accuracy' : actor.stats['focus'],
	 		'evasion' : target.stats['agility']}

def magic(actor, target):
	return {'force' : actor.stats['intelligence'],
			'resist' : target.stats['willpower'],
			'accuracy' : actor.stats['focus'],
			'evasion' : target.stats['agility']}

'Other'
# Command should necessarily miss
def miss():
	return {'force' : 0,
			'resist' : 0,
			'accuracy' : 0,
			'evasion' : 1000}

