# TODO(kgeffen) This should be made into a json file,
# many of the other generic pys should as well

# Stats for common objects added to field
def rock():
	return {
		'model' : 'rock',
		'name' : 'Rock',
		'descript' : 'A rock. Immobile and passive, it acts as makeshift a barrier.',
		'align' : 'neutral',
		'health' : 200,
		'hp' : 200,
		'spirit' : 0,
		'sp' : 0,
		'move' : 0,
		'mv' : 0,
		'actions' : 0,
		'act' : 0,
		'strength' : 0,
		'intelligence' : 0,
		'toughness' : 100,
		'willpower' : 0,
		'focus' : 0,
		'agility' : 0,
		'speed' : 0,
		'jump' : 0,
		'regen' : 0,
		'commands' : [[]]
		}

def bird():
	return {
		'model' : 'bird',
		'name' : 'Bird',
		'descript' : 'A small bird. Although it cannot attack, it is great for blocking bases or slowing down any assailants. It can also be used in combination with Ribbon-Dash or Passage Bolt to move across the field quickly.',
		'align' : 'neutral',
		'health' : 100,
		'hp' : 100,
		'spirit' : 0,
		'sp' : 0,
		'move' : 5,
		'mv' : 5,
		'actions' : 0,
		'act' : 0,
		'strength' : 0,
		'intelligence' : 0,
		'toughness' : 20,
		'willpower' : 20,
		'focus' : 100,
		'agility' : 100,
		'speed' : 50,
		'jump' : 100,
		'regen' : 0,
		'commands' : [[]]
		}

def flame():
	return {
		'model' : 'flame',
		'name' : 'Flame',
		'descript' : 'A raging fire. It can burn any adjacent units and eventually can spread. It can only spread once.',
		'align' : 'neutral',
		'health' : 200,
		'hp' : 200,
		'spirit' : 200,
		'sp' : 50,
		'move' : 0,
		'mv' : 0,
		'actions' : 1,
		'act' : 1,
		'strength' : 100,
		'intelligence' : 100,
		'toughness' : 0,
		'willpower' : 0,
		'focus' : 100,
		'agility' : 0,
		'speed' : 50,
		'jump' : 0,
		'regen' : 25,
		'commands' : [['burn', 'livingFlame']]
		}
def ice():
	return {
		'model' : 'ice',
		'name' : 'Ice',
		'descript' : 'A frigid ice crystal. On the offense, it can shoot a shard of ice to hit far away enemies, or can slow them down with Ice Prison. It can spread, but only once.',
		'align' : 'neutral',
		'health' : 300,
		'hp' : 300,
		'spirit' : 200,
		'sp' : 0,
		'move' : 0,
		'mv' : 0,
		'actions' : 1,
		'act' : 1,
		'strength' : 100,
		'intelligence' : 100,
		'toughness' : 100,
		'willpower' : 100,
		'focus' : 100,
		'agility' : 0,
		'speed' : 50,
		'jump' : 0,
		'regen' : 25,
		'commands' : [['iceShard', 'icePrison', 'crystallineCluster']]
		}

def squire():
	return {
		'model' : 'squire',
		'name' : 'Squire',
		'descript' : 'A weak squire. Can raise the strength of nearby units, and slash to take out weaker enemies.',
		'align' : 'neutral',
		'health' : 500,
		'hp' : 500,
		'spirit' : 0,
		'sp' : 0,
		'move' : 3,
		'mv' : 3,
		'actions' : 1,
		'act' : 1,
		'strength' : 60,
		'intelligence' : 40,
		'toughness' : 60,
		'willpower' : 40,
		'focus' : 50,
		'agility' : 50,
		'speed' : 50,
		'jump' : 10,
		'regen' : 0,
		'commands' : [['slash', 'dualSharpen']]
		}
