# Handle unit upkeep
from bge import logic

# A dict of all traits that trigger at upkeep and what their effect is
TRAIT_EFFECT = {'Poisoned' : 'poisonDamage',
				'Extra Action' : 'addAction'}

# Provide any upkeep needed such as regening sp and restoring move
def do(unit):
	# Regenerate mv
	unit.stats['mv'] = unit.stats['move']
	
	# Regenerate actions
	unit.stats['act'] = unit.stats['actions']
	
	regenerateSp(unit)

	triggerEffectsBasedOnTraits(unit)

# Call any effects that happen because of traits that unit has
def triggerEffectsBasedOnTraits(unit):
	# NOTE(kgeffen) Calling effects after forming list because effects could alter
	# units traits, which would cause list to change during iteration
	calledEffects = []

	for trait in unit.stats['traits']:
		if trait in TRAIT_EFFECT:
			calledEffects.append(TRAIT_EFFECT[trait])

	# TODO(kgeffen) To prevent circular dependancies, should solve underlying problem given the chance
	if calledEffects != []:
		from script.command import effects

	for effect in calledEffects:
		effects.perform(effect, target = unit)

# Increase Sp by percentage (equal to 'regen') of 'Spirit'
# Sp cannot exceed 'spirit'
def regenerateSp(unit):
	dSp = round( unit.stats['regen']/100 * unit.stats['spirit'] )
	
	unit.stats['sp'] += dSp
	
	# If sp exceeds spirit, set sp equal to spirit
	if unit.stats['sp'] > unit.stats['spirit']:
		unit.stats['sp'] = unit.stats['spirit']
