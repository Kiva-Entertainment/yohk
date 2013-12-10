# Contains all of the damage and range calculations for all commands

# Dynamically called by commandControl.py
# NOTE(kgeffen) Class names start with lowercase for ease of use
from bge import logic
import copy

from script.command import generic

'''Weapons'''
'Sword'
class slash:
	# The most basic attack
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
	
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
		
		if generic.command.hitCheck(target, factors):
			# Attack (Don't take altered attack into consideration)
			generic.command.standardAttack(target, factors)
			
			# Raise strength
			generic.command.raiseStat(actor, 'strength', 8)
	
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
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
		
		# Move actor forward to space in front of target
		generic.command.move(actor)
	
	def displayRange():
		commandRange = generic.rangeFactors.sword()
		
		# Hit units in sightline from actor that are not adjacent (to actor)
		reach = generic.extentInfluence.polynomial(1, 1)
		offset = 1 # Spaces adjacent to (1 space away from) actor is not valid target
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
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
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
			
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
		
		# Move forward
		generic.command.move(actor)
	
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
			
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
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
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
		
		# Step backwards 1 space
		generic.command.move(actor)
	
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

		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
	
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

class gorgonSlash:
	# Hit adjacent unit, lower target's mv
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		if generic.command.hitCheck(target, factors):
			# Attack (Don't take altered attack into consideration)
			generic.command.standardAttack(target, factors)
			
			# Lower mv
			generic.command.raiseStat(target, 'mv', -1)
	
	def displayRange():
		commandRange = generic.rangeFactors.sword()
		generic.range.rigid(commandRange)
	
	def cost():
		return 10
	
	def description():
		return ('Strike an adjacent unit and lower their mv.' + '\n\n'
		 		'TODO.')
	
	def name():
		return 'Gorgon Slash'
	
	def icon():
		return 'W_Sword_020.png'

'Axe'
class chop:
	# The most basic attack
	def perform(actor, target):
		factors = generic.commandFactors.axe(actor, target)
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
	
	def displayRange():
		commandRange = generic.rangeFactors.axe()
		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Chope down an adjacent unit with your axe.\n\n'
		 		'Basic physical attack.')
	
	def name():
		return 'Chop'
	
	def icon():
		return 'W_Axe_001.png'
class quakeImpact:
	# The most basic attack
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.axe(actor, target)
			
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def displayRange():
		commandRange = generic.rangeFactors.axe()

		commandRange['aoe'] = generic.shapes.diamond(1)

		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Strike the ground at your side, cracking the earth and hurting yourself and others.\n\n'
		 		'TODO.')
	
	def name():
		return 'Quake Impact'
	
	def icon():
		return 'W_Mace_004.png'
class grandSwath:
	# The most basic attack
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.axe(actor, target)
			
			factors['force'] *= 2

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def displayRange():
		commandRange = generic.rangeFactors.axe()

		commandRange['aoe'] = generic.shapes.diamond(2,1)

		generic.range.free(commandRange)
	
	def cost():
		return 10
	
	def description():
		return ('Destroy all nearby units.\n\n'
		 		'Basic physical attack.')
	
	def name():
		return 'Grand Swath'
	
	def icon():
		return 'W_Axe_014.png'

class skullShatter:
	# The most basic attack
	def perform(actor, target):
		factors = generic.commandFactors.axe(actor, target)
		
		factors['force'] *= generic.extentInfluence.polynomial(1, 0.1)

		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)

			# Lower target's intelligence
			amount = generic.extentInfluence.polynomial(12, 4)
			generic.command.raiseStat(target, 'intelligence', -amount)
	
	def displayRange():
		commandRange = generic.rangeFactors.axe()
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(17, 4, 6)
	
	def description():
		return ('Shatter an adjacent unit\'s skull with a mighty swing of your axe.\n\n'
		 		'Basic physical attack plus lowered int.')
	
	def name():
		return 'Skull Shatter'
	
	def icon():
		return 'W_Axe_008.png'
class murderTwist:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.axe(actor, target)
			
			factors['force'] *= generic.extentInfluence.polynomial(1, 0.1)

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)

				# Lower target's agility
				amount = generic.extentInfluence.polynomial(12, 4)
				generic.command.raiseStat(target, 'agility', -amount)
	
	def displayRange():
		commandRange = generic.rangeFactors.axe()

		commandRange['aoe'] = generic.shapes.ring(1)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(24, 5, 6)
	
	def description():
		return ('Spin around and kill them all. Lowers accuracy.\n\n'
		 		'TODO.')
	
	def name():
		return 'Murder Twist'
	
	def icon():
		return 'W_Axe_010.png'
class concentratedChaos:
	def perform(actor, target):
		factors = generic.commandFactors.axe(actor, target)
		
		factors['force'] *= generic.extentInfluence.polynomial(1, 1)

		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)

			# Lower target's focus
			amount = generic.extentInfluence.polynomial(9, 5)
			generic.command.raiseStat(target, 'focus', -amount)
	
	def displayRange():
		commandRange = generic.rangeFactors.axe()

		radius = generic.extentInfluence.polynomial(0,1)
		commandRange['specialSpaces'] = generic.shapes.diamond(radius, 1)
		commandRange['range'] = generic.shapes.ring(radius + 1)

		generic.range.free(commandRange)
	
	def cost():
		return 0#generic.extentInfluence.polynomial(13, 7, 18)
	
	def description():
		return ('The entire universe focuses its pain and confusion of the enemy.\n\n'
		 		'TODO.')
	
	def name():
		return 'Concentrated Chaos'
	
	def icon():
		return 'W_Axe_013.png'


'Wand'
class psiStrike:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		factors['accuracy'] *= 0.5

		# Lower target's hp and lower sp by tenth of hp loss
		if generic.command.hitCheck(target, factors):
			amount = generic.command.standardAttack(target, factors)
			amount /= 10

			generic.command.raiseStat(target, 'sp', -amount)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()
		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Hit an adjacent unit with magical waves of energy.' + '\n\n'
				'Basic magic attack. Lowers target\'s sp')
	
	def name():
		return 'Psi-Strike'
	
	def icon():
		return 'W_Wand_06.png'

'''Magic'''
'Offensive'
class mudshot:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.magic(actor, target)
			
			if generic.command.hitCheck(target, factors):
				
				# Lower mv
				amount = generic.extentInfluence.polynomial(1, 1)
				generic.command.raiseStat(target, 'mv', -amount)

				# Deal damage
				generic.command.standardAttack(target, factors)
				
	
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
		generic.command.move(target)
		
		if generic.command.hitCheck(target, factors):
			# Deal damage
			generic.command.standardAttack(target, factors)				
	
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
		generic.command.raiseStat(target, 'toughness', 10)
		generic.command.raiseStat(target, 'willpower', 10)
		generic.command.raiseStat(target, 'agility', 10)
		generic.command.raiseStat(target, 'mv', 3)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		# A diamond centered on user, but center ([0,0]) is omitted (1 = # of rings omitted)
		commandRange['range'] = generic.shapes.diamond(2, 1)

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
class earthGrip:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		if generic.command.hitCheck(target, factors):
			generic.command.scaleStat(target, 'mv', 0)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		# Max distance to target
		distance = generic.extentInfluence.polynomial(1, 1)
		commandRange['range'] = generic.shapes.line(distance)

		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(40, 12, 8)
	
	def description():
		return ('Drag a nearby unit to the ground.' + '\n\n'
				'TODO.')
	
	def name():
		return 'Earth Grip'
	
	def icon():
		return 'S_Earth_02.png'
class icePrison:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		if generic.command.hitCheck(target, factors):
			generic.command.raiseStat(target, 'movement', -1)
			generic.command.raiseStat(target, 'mv', -1)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		# Max distance to target
		distance = generic.extentInfluence.polynomial(2, 1)
		commandRange['range'] = generic.shapes.diamond(distance, 1)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(40, 6, 17)
	
	def description():
		return ('Enclose nearby unit in ice, lowering their movement.' + '\n\n'
				'TODO.')
	
	def name():
		return 'Ice Prison'
	
	def icon():
		return 'S_Ice_07.png'
class degenerate:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		numberTimes = generic.extentInfluence.polynomial(1,1)
		for i in range(0, numberTimes):

			# Attack target
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		# A diamond centered on user, but center ([0,0]) is omitted (1 = # of rings omitted)
		commandRange['range'] = generic.shapes.diamond(2, 1)

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


class flameBarrage:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		numberTimes = generic.extentInfluence.polynomial(1,1)
		for i in range(0, numberTimes):

			# Attack target
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		# A diamond centered on user, but center ([0,0]) is omitted (1 = # of rings omitted)
		commandRange['range'] = generic.shapes.diamond(2, 1)

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
class meteor:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.magic(actor, target)
			
			# Raise atack's force and accuracy
			factors['force'] *= generic.extentInfluence.polynomial(1, 1/2)
			factors['accuracy'] *= generic.extentInfluence.polynomial(1, 1/2)
			
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
		
	
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
class divineReflection:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)

		if generic.command.hitCheck(target, factors):
			# Make a copy of target and place it
			unit = copy.deepcopy(target)
			unit['hp'] = 1
			unit['sp'] = 0
			unit['align'] = actor['align']
			unit['name'] = 'Reflection'
			
			generic.command.addObjects(unit)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['specialSpaces'] = [[0,1]]

		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('To reflect is divine.\n\n'
			'TODO.')
	
	def name():
		return 'Divine Reflection'
	
	def icon():
		return 'I_Mirror.png'
class birdcall:
	def perform(actor):
		# Make a copy of target and place it
		unit = generic.objects.bird()
		unit['align'] = actor['align']
		
		generic.command.addObjects(unit)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = generic.shapes.diamond(3, 1)
		commandRange['specialSpaces'] = generic.shapes.single()

		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('TWeet tweet.\n\n'
			'TODO.')
	
	def name():
		return 'Birdcall'
	
	def icon():
		return 'I_Feather_01.png'
class stoneGarden:
	def perform(actor, target):
		# Add a barrel on each side
		# 4 barrels in total
		units = []
		for i in range(0,4):
			units.append(generic.objects.barrel())

		generic.command.addObjects(*units)
	
	def displayRange():
		commandRange = generic.rangeFactors.self()

		commandRange['specialSpaces'] = generic.shapes.ring(1)

		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Get some alone time.\n\n'
			'TODO.')
	
	def name():
		return 'Stone Garden'
	
	def icon():
		return 'S_Earth_04.png'
class stoneArmor:
	def perform(actor, target):
		amount = generic.extentInfluence.polynomial(10, 4)
		generic.command.raiseStat(target, 'toughness', 10)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = generic.shapes.diamond(2)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(20, 5, 4)
	
	def description():
		return ('Cloak a nearby unit in tough stone.\n\n'
			'TODO.')
	
	def name():
		return 'Stone Armor'
	
	def icon():
		return 'S_Earth_06.png'
class emogen:
	def perform(actor, *targets):
		# Amount of healing
		amount = generic.extentInfluence.polynomial(100, 50)

		for target in targets:
			generic.command.raiseStat(target, 'hp', amount)
	
	def displayRange():
		commandRange = generic.rangeFactors.self()

		commandRange['aoe'] = generic.shapes.diamond(1)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(30, 10, 10)
	
	def description():
		return ('The healing is good.\n\n'
			'TODO.')
	
	def name():
		return 'Emogen'
	
	def icon():
		return 'S_Magic_01.png'



'''Items'''
'Books'
# TODO(kgeffen) Sp regen should happen in a generic method
class study:
	def perform(actor, target):
		# Increase sp by same amount as at upkeep
		dSp = actor['regen']/100 * actor['spirit']
		dSp = round(dSp)
		generic.command.raiseStat(actor, 'sp', dSp)
	
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
		amount = actor['regen']/100 * actor['spirit']
		amount = round(amount)
		
		generic.command.raiseStat(actor, 'sp', amount)
		generic.command.raiseStat(target, 'sp', amount)
	
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
		generic.command.raiseStat(actor, 'mv', 2)
	
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

class rush:
	def perform(actor, target):
		generic.command.raiseStat(actor, 'speed', 5)
	
	def displayRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Raise your speed.\n\n'
			'TODO')
	
	def name():
		return 'Rush'
	
	def icon():
		return 'E_Shoes_06.png'
class kick:
	# The most basic attack
	def perform(actor, target):
		factors = generic.commandFactors.physical(actor, target)
		
		factors['force'] *= 0.9

		# Attack
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)

		# Raise movement
		generic.command.raiseStat(actor, 'mv', 1)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()
		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Kick an adjacent unit, then run away.' + '\n\n'
		 		'TODO.')
	
	def name():
		return 'Kick'
	
	def icon():
		return 'E_Shoes_03.png'
class sneak:
	def perform(actor, target):
		generic.command.raiseStat(actor, 'mv', 1)
		generic.command.raiseStat(actor, 'agility', 8)
	
	def displayRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Skulk around.\n\n'
			'TODO.')
	
	def name():
		return 'Sneak'
	
	def icon():
		return 'E_Shoes_07.png'


'''Skill'''
class strengthen:
	def perform(actor, target):
		generic.command.raiseStat(actor, 'strength', 10)
	
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
		generic.command.raiseStat(actor, 'intelligence', 10)
	
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
		generic.command.raiseStat(actor, 'focus', 10)
	
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
		generic.command.raiseStat(actor, 'strength', 8)
		generic.command.raiseStat(target, 'strength', 8)
	
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

class craft:
	def perform(actor):
		unit = generic.objects.barrel()

		generic.command.addObjects(unit)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['specialSpaces'] = generic.shapes.single()

		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Make a barrel like pow!\n\n'
			'TODO.')
	
	def name():
		return 'Craft'
	
	def icon():
		return 'I_Rock_01.png'

class bloodRitual:
	def perform(actor, target):
		# Lower hp
		generic.command.raiseStat(actor, 'hp', -100)

		generic.command.raiseStat(actor, 'strength', 20)
		generic.command.raiseStat(actor, 'intelligence', 20)
		generic.command.raiseStat(actor, 'sp', 20)
	
	def displayRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Pay for power in blood.\n\n'
			'TOODO.')
	
	def name():
		return 'Blood Ritual'
	
	def icon():
		return 'I_Ruby.png'
class bloodlust:
	def perform(actor, target):
		# Empty target's sp
		amount = generic.command.scaleStat(target, 'sp', 0)

		# Raise target's sp by same amount
		generic.command.raiseStat(target, 'strength', -amount)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = generic.shapes.diamond(1)

		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Make them see blood.\n\n'
			'TOODO.')
	
	def name():
		return 'Bloodlust'
	
	def icon():
		return 'S_Death_01.png'
class riteOfImmortality:
	def perform(actor):
		# Hurt self
		generic.command.raiseStat(actor, 'hp', -100)

		unit = copy.deepcopy(actor)

		unit['hp'] = 1
		unit['sp'] = 0
		unit['name'] = 'Husk'

		generic.command.addObjects(unit)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		reach = generic.extentInfluence.polynomial(1,1)
		commandRange['range'] = generic.shapes.diamond(reach, 1)

		commandRange['specialSpaces'] = generic.shapes.single()

		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Split your body and soul!\n\n'
			'TODO.')
	
	def name():
		return 'Rite of Immortality'
	
	def icon():
		return 'I_Bone.png'


'''Special'''
class deploy:
	def perform(actor):
		choice = logic.globalDict['commandChoices'][0]['value']
		unit = choice

		generic.command.addObjects(unit)
	
	def displayRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['specialSpaces'] = generic.shapes.single()

		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Deploy a unit.\n\n'
			'TODO.')
	
	def name():
		return 'Deploy'
	
	def icon():
		return 'S_Buff_06.png'

	def determineChoices():
		ownAlign = logic.globalDict['actor']['align']

		choices = logic.globalDict['commandChoices']
		for unit in logic.globalDict['inactiveUnits']:
			if unit['align'] == ownAlign:
				
				pair = {'value' : unit,
						'display' : unit['name']}
				choices.append(pair)


