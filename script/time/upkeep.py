# Handle unit upkeep
from bge import logic

# Provide any upkeep needed such as regening sp and restoring move
def unit(unit):
	# TODO(kgeffen) As more traits are added, determining what happens, as well as how it stacks,
	# should be made into a more concrete process
	# For example, instead of elifs, have a dictionary with methods called based on the unit's traits
	if 'Poisoned' in unit['traits']:
		dealPoisonDamage(unit)

	# Regenerate mv
	unit['mv'] = unit['move']
	
	# Regenerate actions
	unit['act'] = unit['actions']
	
	regenerateSp(unit)


# Increase Sp by percentage (equal to 'regen') of 'Spirit'
# Sp cannot exceed 'spirit'
def regenerateSp(unit):
	dSp = round( unit['regen']/100 * unit['spirit'] )
	
	unit['sp'] += dSp
	
	# If sp exceeds spirit, set sp equal to spirit
	if unit['sp'] > unit['spirit']:
		unit['sp'] = unit['spirit']

# TODO(kgeffen) Make a setup for effects to deal damage while taking advantage of functionality of command package
def dealPoisonDamage(unit):
	dHp = round(unit['health'] / 10)
	
	if unit['hp'] >= dHp:
		unit['hp'] -= dHp
	else:
		unit['hp'] = 0


