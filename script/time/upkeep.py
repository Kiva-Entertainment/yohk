# Handle unit upkeep
from bge import logic

# Provide any upkeep needed such as regening sp and restoring move
def unit(unitNumber):
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

