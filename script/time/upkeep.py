# Handle unit upkeep
from bge import logic

# Provide any upkeep needed such as regening sp and restoring move
def unit(unitNumber):
	unitData = logic.globalDict['units'][unitNumber]
	
	# Regenerate mv
	logic.globalDict['units'][unitNumber]['mv'] = unitData['move']
	
	# Regenerate actions
	logic.globalDict['units'][unitNumber]['act'] = unitData['actions']
	
	regenerateSp(unitNumber, unitData)


# Increase Sp by percentage (equal to 'regen') of 'Spirit'
# Sp cannot exceed 'spirit'
def regenerateSp(unitNumber, unitData):
	dSp = round( unitData['regen']/100 * unitData['spirit'] )
	
	logic.globalDict['units'][unitNumber]['sp'] += dSp
	
	# If sp exceeds spirit, set sp equal to spirit
	if logic.globalDict['units'][unitNumber]['sp'] > unitData['spirit']:
		logic.globalDict['units'][unitNumber]['sp'] = unitData['spirit']

