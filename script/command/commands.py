# Contains all of the damage and range calculations for all commands

# Dynamically called by commandControl.py
# NOTE(kgeffen) Class names start with lowercase for ease of use
from bge import logic

from script.command import generic

'''Weapons'''
'Sword'
class slash:
	# The most basic attack
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		if generic.command.hitCheck(target['number'], factors):
			generic.command.standardAttack(target['number'], factors)
	
	def displayRange():
		commandRange = generic.rangeFactors.sword()
		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Slash an adjacent unit with your sword.' + '\n\n'
		 		'Basic physical attack.')
	
	def name():
		return 'Slash'
	
	def icon():
		return 'W_Sword_001.png'
class gloryStrike:
	# Hit adjacent unit, raise user's strength
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		if generic.command.hitCheck(target['number'], factors):
			# Attack (Don't take altered attack into consideration)
			generic.command.standardAttack(target['number'], factors)
			
			# Raise strength
			generic.command.raiseStat(actor['number'], 'strength', 8)
	
	def displayRange():
		commandRange = generic.rangeFactors.sword()
		generic.range.rigid(commandRange)
	
	def cost():
		return 18
	
	def description():
		return ('Strike an adjacent unit and gain strength from the glory of a righteous battle.' + '\n\n'
		 		'Basic physical attack.' + '\n'
				'Raises user\'s strength by 8 after it hits.')
	
	def name():
		return 'Glory Strike'
	
	def icon():
		return 'S_Sword_06.png'
class predatorsDescent:
	# Move actor forward to space in front of unit in sightline, attack that unit
	# Important counter to mudshot/aeroblast
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		if generic.command.hitCheck(target['number'], factors):
			generic.command.standardAttack(target['number'], factors)
		
		# Move actor forward to space in front of target
		generic.command.move(actor['number'])
	
	def displayRange():
		commandRange = generic.rangeFactors.sword()
		
		# Hit units in sightline from actor that are not adjacent (to actor)
		reach = generic.extentInfluence.polynomial(1, 1)
		offset = 1 # Spaces adjacent to user (1 space from actor) should not be selectable
		commandRange['range'] = generic.shapes.line(reach, offset)

		# Space to move to
		commandRange['specialSpaces'] = [[0,-1]]
		
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(12, 4, 2)
	
	def description():
		return ('Jump forward and slash a unit in your sightline.\n\n'
				'Standard physical damage to a unit, move in front of that unit.' + '\n'
				'Move farther if you spend more.')
	
	def name():
		return "Predator's Descent"
	
	def icon():
		return 'W_Sword_009.png'
class doubleSlash:
	# Powerful sword skill that relies on open space around target
	# Most classes can't use it every turn
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		for i in range(0,2):
			if generic.command.hitCheck(target['number'], factors):
				generic.command.standardAttack(target['number'], factors)
	
	def displayRange():
		commandRange = generic.rangeFactors.sword()
		
		# Empty spaces
		# TODO(kgeffen) Make generic for this
		commandRange['specialSpaces'] = [[1,1],[-1,1],[-1,-1],[1,-1]]
		
		generic.range.rigid(commandRange)
	
	def cost():
		return 32
	
	def description():
		return ('Slash an adjacent unit twice, because slashing once just isn\'t enough.\n\n'
			'Standard physical damage to an adjacent unit with empty spaces on its diagonals.')
	
	def name():
		return "Double Slash"
	
	def icon():
		return 'W_Sword_013.png'
class ribbonDash:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.sword(actor, target)
			
			factors['force'] *= generic.extentInfluence.polynomial(1, 1/12)
			
			if generic.command.hitCheck(target['number'], factors):
				generic.command.standardAttack(target['number'], factors)
		
		# Move forward
		generic.command.move(actor['number'])
	
	def displayRange():
		commandRange = generic.rangeFactors.sword()
		
		length = logic.globalDict['extent'] + 1
		
		commandRange['aoe'] = generic.shapes.line(length)
		commandRange['specialSpaces'] = [[0,length]]
		
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(9, 2, 2)
	
	def description():
		return ('Dash forward, slashing all units in your path to ribbons.\n\n'
			'Standard physical damage to all units between user and ending space.\n'
			'Deal more and move further by spending more.')
	
	def name():
		return 'Ribbon Dash'
	
	def icon():
		return 'W_Sword_004.png'
class frontlineSlash:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.sword(actor, target)
			
			if generic.command.hitCheck(target['number'], factors):
				generic.command.standardAttack(target['number'], factors)
	
	def displayRange():
		commandRange = generic.rangeFactors.sword()
		
		commandRange['aoe'] = generic.shapes.flatLine(1)
		
		generic.range.rigid(commandRange)
	
	def cost():
		return 18
	
	def description():
		return ('A massive sword swipe that hits up to 3 units in line in front of user.\n\n'
			'Standard physical damage to each unit.')
	
	def name():
		return 'Frontline Slash'
	
	def icon():
		return 'W_Sword_007.png'
class ebber:
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		if generic.command.hitCheck(target['number'], factors):
			generic.command.standardAttack(target['number'], factors)
		
		# Step backwards 1 space
		generic.command.move(actor['number'])
	
	def displayRange():
		commandRange = generic.rangeFactors.sword()
		
		# Space X spaces behind actor
		distance = generic.extentInfluence.polynomial(1, 1)
		# NOTE(kgeffen) distance + 1 since -1 = actor's space,
		# not space behind actor
		commandRange['specialSpaces'] = [[0, -( distance + 1 )]]
		
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(2, 1, 1)
	
	def description():
		return ('Slash forward as you step backwards (Very zen).\n\n'
			'Standard physical attack, move back X spaces.')
	
	def name():
		return 'Ebber'
	
	def icon():
		return 'S_Sword_09.png'
class cleave:
	# Basic powerful attack
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		factors['accuracy'] *= 1.5
		factors['force'] *= 2

		if generic.command.hitCheck(target['number'], factors):
			generic.command.standardAttack(target['number'], factors)
	
	def displayRange():
		commandRange = generic.rangeFactors.sword()
		generic.range.rigid(commandRange)
	
	def cost():
		return 60
	
	def description():
		return ('Strike an adjacent unit with a powerful sword technique.' + '\n\n'
		 		'Powerful physical attack, more accurate than normal.')
	
	def name():
		return 'Cleave'
	
	def icon():
		return 'W_Sword_011.png'

'Wand'
class psiStrike:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		if generic.command.hitCheck(target['number'], factors):
			generic.command.standardAttack(target['number'], factors)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()
		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Hit an adjacent unit with magical waves of energy.' + '\n\n'
				'Basic magic attack.')
	
	def name():
		return 'Psi-Strike'
	
	def icon():
		return 'W_Wand_06.png'

'''Magic'''
'Offensive'
class flameBarrage:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		numberTimes = generic.extentInfluence.polynomial(1,1)
		for i in range(0, numberTimes):

			# Attack target
			if generic.command.hitCheck(target['number'], factors):
				generic.command.standardAttack(target['number'], factors)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = generic.shapes.emptyDiamond(2)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(12, 36, 27)
	
	def description():
		return ('Send a barrage of flame at a nearby unit.\n\n'
			'Standard magic damage X times.')
	
	def name():
		return 'Flame Barrage'
	
	def icon():
		return 'S_Fire_03.png'
class mudshot:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.magic(actor, target)
			
			if generic.command.hitCheck(target['number'], factors):
				
				# Lower mv
				amount = generic.extentInfluence.polynomial(1, 1)
				generic.command.raiseStat(target['number'], 'mv', -amount)

				# Deal damage
				generic.command.standardAttack(target['number'], factors)
				
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()
		
		# Hit all units in actors sightline of length = _extent_
		length = 1 + logic.globalDict['extent']
		commandRange['aoe'] = generic.shapes.line(length)
		
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(17, 16, 9)
	
	def description():
		return ('Send mud cardinally. Hit all units in its path.\n\n'
			'Standard magic damage to all units in mud\'s path.\n'
			'All units that are hit have their movement lowered for the next turn.\n'
			'Spend more to send mud farther and lower movement by more.')
	
	def name():
		return 'Mudshot'
	
	def icon():
		return 'S_Earth_05.png'
class aeroImpact:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		# move target
		generic.command.move(target['number'])
		
		if generic.command.hitCheck(target['number'], factors):
			# Deal damage
			generic.command.standardAttack(target['number'], factors)				
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()
		
		# Can hit very low targets so they can land lower
		# TODO(kgeffen) Make landing space ok to be low,
		# but not the target hit
		commandRange['okDz'] = {'max' : 1.0, 'min' : -10.0}
		
		# Move target back Number of spaces equal to extent
		distance = generic.extentInfluence.polynomial(1, 1)
		commandRange['specialSpaces'] = [[0, distance]]
		
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(16, 5, 11)
	
	def description():
		return ('Send a burst of air at an adjacent unit.\n\n'
			'Standard magic damage and move target backwards.\n'
			'Push target further by spending more.')
	
	def name():
		return 'Aero Impact'
	
	def icon():
		return 'S_Physic_02.png'
class galeCloak:
	def perform(actor, target):
		generic.command.raiseStat(target['number'], 'toughness', 10)
		generic.command.raiseStat(target['number'], 'willpower', 10)
		generic.command.raiseStat(target['number'], 'agility', 10)
		generic.command.raiseStat(target['number'], 'mv', 3)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = generic.shapes.emptyDiamond(2)

		generic.range.free(commandRange)
	
	def cost():
		return 60
	
	def description():
		return ('Cloak a nearby unit in powerful wind.\n\n'
			'Raise target\'s defensive abilities and mv.')
	
	def name():
		return 'Gale Cloak'
	
	def icon():
		return 'S_Wind_02.png'
class meteor:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.magic(actor, target)
			
			# Raise atack's force and accuracy
			factors['force'] *= generic.extentInfluence.polynomial(1, 1/2)
			factors['accuracy'] *= generic.extentInfluence.polynomial(1, 1/2)
			
			if generic.command.hitCheck(target['number'], factors):
				generic.command.standardAttack(target['number'], factors)
		
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()
		
		# How far from caster spell command can be target meteor's center
		reach = generic.extentInfluence.polynomial(2, 1)
		commandRange['range'] = generic.shapes.diamond(reach)
		
		# How large the meteor is
		length = generic.extentInfluence.polynomial(0, 1)
		commandRange['aoe'] = generic.shapes.diamond(length)
		
		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(12, 45, 34, 15)
	
	def description():
		return ('Call down a huge meteor from outer space.\n\n'
			'Call down larger meteors by spending more')
	
	def name():
		return 'Meteor'
	
	def icon():
		return 'S_Fire_05.png'

'''Items'''
'Books'
# TODO(kgeffen) Sp regen should happen in a generic method
class study:
	def perform(actor, target):
		# Increase sp by same amount as at upkeep
		dSp = actor['data']['regen']/100 * actor['data']['spirit']
		dSp = round(dSp)
		generic.command.raiseStat(actor['number'], 'sp', dSp)
	
	def displayRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Spend the turn reading.' + '\n\n'
				'Regenerate sp.')
	
	def name():
		return 'Study'
	
	def icon():
		return 'W_Book_01.png'
class tutor:
	def perform(actor, target):
		# Increase sp by same amount as at upkeep
		amount = actor['data']['regen']/100 * actor['data']['spirit']
		amount = round(amount)
		
		generic.command.raiseStat(actor['number'], 'sp', amount)
		generic.command.raiseStat(target['number'], 'sp', amount)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()
		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Teach an adjacent unit about life.\n\n'
			'Regenerate the sp of user and an adjacent unit.')
	
	def name():
		return 'Tutor'
	
	def icon():
		return 'W_Book_06.png'

'Boots'
class dash:
	def perform(actor, target):
		generic.command.raiseStat(actor['number'], 'mv', 2)
	
	def displayRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Hightail it out of there.\n\n'
			'Move an additional 2 spaces this turn.')
	
	def name():
		return 'Dash'
	
	def icon():
		return 'E_Shoes_01.png'

'''Skill'''
class strengthen:
	def perform(actor, target):
		generic.command.raiseStat(actor['number'], 'strength', 10)
	
	def displayRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Got strong, son.\n\n'
			'Raise user\'s strength by 10.')
	
	def name():
		return 'Strengthen'
	
	def icon():
		return 'S_Buff_01.png'
class smarten:
	def perform(actor, target):
		generic.command.raiseStat(actor['number'], 'intelligence', 10)
	
	def displayRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('The best way to learn is to listen.\n\n'
			'Raise user\'s intelligence by 10.')
	
	def name():
		return 'Smarten'
	
	def icon():
		return 'S_Buff_03.png'
class focus:
	def perform(actor, target):
		generic.command.raiseStat(actor['number'], 'focus', 10)
	
	def displayRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Just breath, you can do this.\n\n'
			'Raise user\'s focus by 10.')
	
	def name():
		return 'Focus'
	
	def icon():
		return 'S_Buff_06.png'
class dualSharpen:
	def perform(actor, target):
		generic.command.raiseStat(actor['number'], 'strength', 8)
		generic.command.raiseStat(target['number'], 'strength', 8)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()
		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Sharpen you weapon against an adjacent unit\'s.\n\n'
			'Raise the strength of user and adjacent unit')
	
	def name():
		return 'Dual-Sharpen'
	
	def icon():
		return 'S_Dagger_01.png'
