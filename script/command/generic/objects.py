# TODO(kgeffen) This should be made into a json file,
# many of the other generic pys should as well

# Stats for common objects added to field
def rock():
	return {
		'model' : 'rock',
		'name' : 'Rock',
		'align' : 'neutral',
		'health' : 400,
		'hp' : 400,
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
		'speed' : 25,
		'jump' : 100,
		'regen' : 0,
		'commands' : [[]]
		}

def flame():
	return {
		'model' : 'flame',
		'name' : 'Flame',
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
		'toughness' : 0,
		'willpower' : 0,
		'focus' : 100,
		'agility' : 0,
		'speed' : 25,
		'jump' : 0,
		'regen' : 25,
		'commands' : [['flameBarrage', 'livingFlame']]
		}


def ice():
	return {
		'model' : 'ice',
		'name' : 'Ice',
		'align' : 'neutral',
		'health' : 300,
		'hp' : 300,
		'spirit' : 200,
		'sp' : 50,
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
		'speed' : 25,
		'jump' : 0,
		'regen' : 13,
		'commands' : [['iceShard', 'icePrison', 'crystallineCluster']]
		}

def bubble():
	return {
		'model' : 'bubble',
		'name' : 'Bubble',
		'align' : 'neutral',
		'health' : 1,
		'hp' : 1,
		'spirit' : 0,
		'sp' : 0,
		'move' : 0,
		'mv' : 0,
		'actions' : 1,
		'act' : 1,
		'strength' : 150,
		'intelligence' : 150,
		'toughness' : 0,
		'willpower' : 0,
		'focus' : 100,
		'agility' : 0,
		'speed' : 1,
		'jump' : 0,
		'regen' : 0,
		'commands' : [['burst']]
		}

