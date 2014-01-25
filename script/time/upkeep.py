# Handle unit upkeep
from bge import logic

# A dict of all traits that trigger at upkeep and what their effect is
TRAIT_EFFECT = {'Poisoned' : 'poisonDamage'}

# Provide any upkeep needed such as regening sp and restoring move
def unit(unit):
	triggerEffectsBasedOnTraits(unit)

	# Regenerate mv
	unit['mv'] = unit['move']
	
	# Regenerate actions
	unit['act'] = unit['actions']
	
	regenerateSp(unit)

# Call any effects that happen because of traits that unit has
def triggerEffectsBasedOnTraits(unit):
	# NOTE(kgeffen) Calling effects after forming list because effects could alter
	# units traits, which would cause list to change during iteration
	calledEffects = []

	for trait in unit['traits']:
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
	dSp = round( unit['regen']/100 * unit['spirit'] )
	
	unit['sp'] += dSp
	
	# If sp exceeds spirit, set sp equal to spirit
	if unit['sp'] > unit['spirit']:
		unit['sp'] = unit['spirit']
