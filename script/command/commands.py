# Contains all of the damage and range calculations for all commands

# Dynamically called by commandControl.py
# NOTE(kgeffen) Class names start with lowercase for ease of use
from bge import logic
import copy, random

from script.command import generic
from script.command.generic import shapes

'''Weapons'''
'Sword'
class slash:
	# The most basic attack
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.sword()
		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Slash an adjacent unit with your sword.' + '\n\n'
		 		'Basic physical attack against adjacent unit.')
	
	def name():
		return 'Slash'
	
	def icon():
		return 'W_Sword_001.png'

	def tags():
		return ['targets']
class cleave:
	# Basic powerful attack
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		factors['force'] *= 2

		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.sword()
		generic.range.rigid(commandRange)
	
	def cost():
		return 52
	
	def description():
		return ('Strike an adjacent unit with a powerful sword technique.' + '\n\n'
		 		'Powerful physical attack which deals twice as much damage as normal.')
	
	def name():
		return 'Cleave'
	
	def icon():
		return 'W_Sword_011.png'

	def tags():
		return ['targets']
class gloryStrike:
	# Hit adjacent unit, raise user's strength
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		if generic.command.hitCheck(target, factors):
			# Attack (Don't take altered attack into consideration)
			generic.command.standardAttack(target, factors)
			
			# Raise strength
			generic.command.raiseStat(actor, 'strength', 8)
	
	def determineRange():
		commandRange = generic.rangeFactors.sword()
		generic.range.rigid(commandRange)
	
	def cost():
		return 14
	
	def description():
		return ('Strike an adjacent unit and gain strength from the glory of a righteous battle.' + '\n\n'
		 		'Basic physical attack.' + '\n'
				'Raises user\'s strength by 8 after it hits.')
	
	def name():
		return 'Glory Strike'
	
	def icon():
		return 'S_Sword_06.png'

	def tags():
		return ['targets']
class predatorsDescent:
	# Move actor forward to space in front of unit in sightline, attack that unit
	# Important counter to mudshot/aeroblast
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		factors['force'] *= 1.2

		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
		
		# Move actor forward to space in front of target
		generic.command.move(actor)
	
	def determineRange():
		commandRange = generic.rangeFactors.sword()
		
		# Hit units in sightline from actor that are not adjacent (to actor)
		reach = generic.extentInfluence.polynomial(1, 1)
		offset = 1 # Spaces adjacent to (1 space away from) actor is not valid target
		commandRange['range'] = shapes.line(reach, offset)

		# Space to move to
		commandRange['specialSpaces'] = [[0,-1]]
		
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(15, 3, 1)
	
	def description():
		return ('Jump forward and slash a unit in your sightline.\n\n'
				'Standard physical damage to a unit, move in front of that unit.' + '\n'
				'Move farther if you spend more.')
	
	def name():
		return "Predator's Descent"
	
	def icon():
		return 'W_Sword_009.png'

	def tags():
		return ['targets', 'extends']
class ebber:
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		factors['force'] *= generic.extentInfluence.polynomial(1, 1/10)

		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
		
		# Step backwards 1 space
		generic.command.move(actor)
	
	def determineRange():
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

	def tags():
		return ['targets', 'extends']
class hugeSlash:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.sword(actor, target)
			
			factors['force'] *= 1.5

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.sword()

		commandRange['aoe'] = shapes.line(3)

		generic.range.rigid(commandRange)
	
	def cost():
		return 32
	
	def description():
		return ('.')
	
	def name():
		return 'Huge Slash'
	
	def icon():
		return 'W_Sword_006.png'

	def tags():
		return ['targets']


'Spear'
class thrust:
	def perform(actor, target):
		factors = generic.commandFactors.spear(actor, target)
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.spear()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Basic spear attack.')
	
	def name():
		return 'Thrust'
	
	def icon():
		return 'W_Spear_001.png'

	def tags():
		return ['targets']
class frostSkewer:
	def perform(actor, target):
		factors = generic.commandFactors.spear(actor, target)
		
		if generic.command.hitCheck(target, factors):
			# Attack
			generic.command.standardAttack(target, factors)

			# Lower target's mv by 1
			generic.command.raiseStat(target, 'mv', -1)
	
	def determineRange():
		commandRange = generic.rangeFactors.spear()
		generic.range.free(commandRange)
	
	def cost():
		return 10
	
	def description():
		return ('Basic spear attack.')
	
	def name():
		return 'Frost Skewer'
	
	def icon():
		return 'W_Spear_015.png'

	def tags():
		return ['targets']
class lightningJavelin:
	def perform(actor, target):
		factors = generic.commandFactors.spear(actor, target)
		
		if generic.command.hitCheck(target, factors):
			# Attack
			generic.command.standardAttack(target, factors)

			# Raise user's act by 1
			generic.command.raiseStat(actor, 'act', 1)
	
	def determineRange():
		commandRange = generic.rangeFactors.spear()
		generic.range.free(commandRange)
	
	def cost():
		return 28
	
	def description():
		return ('Basic spear attack.')
	
	def name():
		return 'Lightning Javelin'
	
	def icon():
		return 'W_Spear_016.png'

	def tags():
		return ['targets']
class beesting:
	def perform(actor, target):
		factors = generic.commandFactors.spear(actor, target)
		
		factors['force'] *= 0.6
		factors['force'] *= 1.5

		if generic.command.hitCheck(target, factors):
			# Attack
			generic.command.standardAttack(target, factors)

			# Lower target's defensive stats
			generic.command.raiseStat(target, 'toughness', -10)
			generic.command.raiseStat(target, 'willpower', -10)
			generic.command.raiseStat(target, 'agility', -10)
	
	def determineRange():
		commandRange = generic.rangeFactors.spear()
		generic.range.free(commandRange)
	
	def cost():
		return 45
	
	def description():
		return ('Lower attack than normal, but lowers defensive stats.')
	
	def name():
		return 'Beesting'
	
	def icon():
		return 'W_Spear_017.png'

	def tags():
		return ['targets']
class guilltineSpiral:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.spear(actor, target)
			
			factors['force'] *= 1.3
			factors['accuracy'] *= 1.3

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def determineRange(): 
		commandRange = generic.rangeFactors.spear()

		commandRange['range'] = shapes.single()
		commandRange['aoe'] = shapes.ring(2)

		generic.range.free(commandRange)
	
	def cost():
		return 29
	
	def description():
		return ('Basic spear attack.')
	
	def name():
		return 'Guilltine Spiral'
	
	def icon():
		return 'W_Spear_008.png'

	def tags():
		return ['targets']
class fallingComet:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.spear(actor, target)
			
			factors['force'] = 1.6
			factors['accuracy'] = 1.6

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.spear()

		commandRange['range'] = [[0, 1]]

		length = 3
		commandRange['aoe'] = shapes.line(length)

		commandRange['specialSpaces'] = [[0, length]]

		generic.range.rigid(commandRange)
	
	def cost():
		return 83
	
	def description():
		return ('Basic spear attack.')
	
	def name():
		return 'Falling Comet'
	
	def icon():
		return 'W_Spear_014.png'

	def tags():
		return ['targets']
class momentousDescent:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.spear(actor, target)
			
			factors['force'] *= 1.4
			factors['accuracy'] *= 1.4

			if target != actor:
				if generic.command.hitCheck(target, factors):
					generic.command.standardAttack(target, factors)
	
	def determineRange(): 
		commandRange = generic.rangeFactors.spear()

		commandRange['range'] = shapes.ring(2)
		commandRange['aoe'] = shapes.x(1)

		generic.range.free(commandRange)
	
	def cost():
		return 33
	
	def description():
		return ('Basic spear attack.')
	
	def name():
		return 'Momentous Descent'
	
	def icon():
		return 'W_Spear_003.png'

	def tags():
		return ['targets']


'Axe'
class chop:
	def perform(actor, target):
		factors = generic.commandFactors.axe(actor, target)
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.axe()
		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Chop down an adjacent unit with your axe.\n\n'
		 		'Basic physical attack.')
	
	def name():
		return 'Chop'
	
	def icon():
		return 'W_Axe_001.png'

	def tags():
		return ['targets']
class chasmMaw:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.axe(actor, target)

			factors['force'] *= 1.3
			factors['accuracy'] *= 1.3
			
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.axe()

		commandRange['aoe'] = shapes.line(3)

		generic.range.rigid(commandRange)
	
	def cost():
		return 36
	
	def description():
		return ('Chop down an adjacent unit with your axe.\n\n'
		 		'Basic physical attack.')
	
	def name():
		return 'Chasm Maw'
	
	def icon():
		return 'W_Mace_009.png'

	def tags():
		return ['targets']
class viciousQuake:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.axe(actor, target)
			
			factors['force'] *= 1.7
			factors['accuracy'] *= 1.8

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.axe()

		hollowSquare = shapes.rectangle(1, 1, True)
		# Push square to be centered space behind (space in front of user)
		commandRange['aoe'] = shapes.push(hollowSquare, [0,-1])

		generic.range.rigid(commandRange)
	
	def cost():
		return 77
	
	def description():
		return ('TODO.')
	
	def name():
		return 'Vicious Quake'
	
	def icon():
		return 'W_Mace_004.png'

	def tags():
		return ['targets']
class brainTrauma:
	def perform(actor, target):
		factors = generic.commandFactors.axe(actor, target)

		factors['accuracy'] *= 1.2
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)

			# Lower target's intelligence
			generic.command.raiseStat(target, 'willpower', -20)
			generic.command.raiseStat(target, 'intelligence', -20)
	
	def determineRange():
		commandRange = generic.rangeFactors.axe()

		generic.range.rigid(commandRange)
	
	def cost():
		return 21
	
	def description():
		return ('Shatter an adjacent unit\'s skull with a mighty swing of your axe.\n\n'
		 		'Basic physical attack plus lowered int.')
	
	def name():
		return 'Brain Trauma'
	
	def icon():
		return 'W_Axe_008.png'

	def tags():
		return ['targets']
class crackFoundation:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.axe(actor, target)
			
			factors['accuracy'] *= 1.2

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)

				# Lower target's physical stats
				generic.command.raiseStat(target, 'toughness', -20)
				generic.command.raiseStat(target, 'strength', -20)

	def determineRange():
		commandRange = generic.rangeFactors.axe()

		commandRange['aoe'] = shapes.flatLine(1)

		generic.range.rigid(commandRange)
	
	def cost():
		return 28
	
	def description():
		return ('Shatter an adjacent unit\'s skull with a mighty swing of your axe.\n\n'
		 		'Basic physical attack plus lowered int.')
	
	def name():
		return 'Crack Foundation'
	
	def icon():
		return 'W_Mace_012.png'

	def tags():
		return ['targets']

'Wand'

'''Magic'''
'Fire'
class flameBarrage:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		numberTimes = generic.extentInfluence.polynomial(1,1)
		for i in range(0, numberTimes):

			# Attack target
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		reach = generic.extentInfluence.polynomial(1, 1)
		commandRange['range'] = shapes.diamond(reach, 1)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(0, 40, 25)
	
	def description():
		return ('Send a barrage of flame at a nearby unit.\n\n'
			'Standard magic damage X times.')
	
	def name():
		return 'Flame Barrage'
	
	def icon():
		return 'S_Fire_03.png'

	def tags():
		return ['targets', 'extends']
class meteor:
	def perform(actor, *targets):
		multiplier = generic.extentInfluence.polynomial(1, 1/2)

		for target in targets:
			factors = generic.commandFactors.magic(actor, target)
			
			# Raise atack's force and accuracy
			factors['force'] *= multiplier
			factors['accuracy'] *= multiplier
			
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
		
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()
		
		# How far from caster spell command can be target meteor's center
		reach = generic.extentInfluence.polynomial(2, 1)
		commandRange['range'] = shapes.diamond(reach)
		
		# How large the meteor is
		length = generic.extentInfluence.polynomial(0, 1)
		commandRange['aoe'] = shapes.diamond(length)
		
		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(10, 49, 20, 8)
	
	def description():
		return ('Call down a huge meteor from outer space.\n\n'
			'Call down larger meteors by spending more')
	
	def name():
		return 'Meteor'
	
	def icon():
		return 'S_Fire_05.png'

	def tags():
		return ['targets', 'extends']
class livingFlame:
	def perform(actor):
		# Make a copy of target and place it
		unit = generic.objects.flame()
		unit['align'] = actor['align']
		unit['intelligence'] = actor['intelligence']
		
		generic.command.addObjects(unit)

		# If user is a flame, lose the skill to make more flame
		if actor['model'] == 'flame':
			generic.command.loseCommand(actor, 'livingFlame')
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = shapes.diamond(2, 1)
		commandRange['specialSpaces'] = shapes.single()

		generic.range.free(commandRange)
	
	def cost():
		return 100
	
	def description():
		return ('.')
	
	def name():
		return 'Living Flame'
	
	def icon():
		return 'S_Fire_02.png'
class blazeCloak:
	def perform(actor, target):
		generic.command.raiseStat(target, 'intelligence', 20)
		generic.command.raiseStat(target, 'strength', 20)
		generic.command.raiseStat(target, 'focus', 20)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = shapes.diamond(1)

		generic.range.free(commandRange)
	
	def cost():
		return 110
	
	def description():
		return ('Raise you offensive power substantially.')
	
	def name():
		return 'Blaze Cloak'
	
	def icon():
		return 'S_Fire_04.png'

	def tags():
		return ['targets']

'Light'
class pacify:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		# If target is a base, command should miss
		if target['model'] == 'base':
			factors = generic.commandFactors.miss()

		if generic.command.hitCheck(target, factors):
			# Lower target's actions by 1
			generic.command.raiseStat(target, 'act', -1)

	def determineRange():
		commandRange = generic.rangeFactors.standard()
		generic.range.rigid(commandRange)
	
	def cost():
		return 100
	
	def description():
		return ('Lower targets actions by 1 for next turn.')
	
	def name():
		return 'Pacify'
	
	def icon():
		return 'S_Holy_01.png'

	def tags():
		return ['targets']
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
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['specialSpaces'] = [[0,1]]

		generic.range.rigid(commandRange)
	
	def cost():
		return 150
	
	def description():
		return ('To reflect is divine.\n\n'
			'TODO.')
	
	def name():
		return 'Divine Reflection'
	
	def icon():
		return 'I_Mirror.png'

	def tags():
		return ['targets']
class emogen:
	def perform(actor, *targets):
		# Amount of healing
		amount = generic.extentInfluence.polynomial(50, 50)

		for target in targets:
			generic.command.raiseStat(target, 'hp', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()

		commandRange['aoe'] = shapes.diamond(1)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(0, 20, 10)
	
	def description():
		return ('The healing is good.\n\n'
			'TODO.')
	
	def name():
		return 'Emogen'
	
	def icon():
		return 'S_Magic_01.png'

	def tags():
		return ['targets', 'extends']

class lightningBolt:
	def perform(actor, target):
		factors = generic.commandFactors.lightning(actor, target)
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)

	def determineRange():
		commandRange = generic.rangeFactors.lightning()

		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Weaker than most magic, but has good range and accuracy.')
	
	def name():
		return 'Lightning Bolt'
	
	def icon():
		return 'S_Thunder_01.png'

	def tags():
		return ['targets']
class chainLightning:
	def perform(actor, target):
		factors = generic.commandFactors.lightning(actor, target)

		if generic.command.hitCheck(target, factors):
			# Attack
			generic.command.standardAttack(target, factors)
			
			# Grant user +1 action
			generic.command.raiseStat(actor, 'act', 1)

	def determineRange():
		commandRange = generic.rangeFactors.lightning()

		generic.range.free(commandRange)
	
	def cost():
		return 23
	
	def description():
		return ('.')
	
	def name():
		return 'Chain Lightning'
	
	def icon():
		return 'S_Thunder_05.png'

	def tags():
		return ['targets']
class passageBolt:
	def perform(actor, target):
		factors = generic.commandFactors.lightning(actor, target)

		factors['force'] *= generic.extentInfluence.polynomial(1, 1/8)

		# Move user
		generic.command.move(actor)

		if generic.command.hitCheck(target, factors):
			# Attack
			generic.command.standardAttack(target, factors)
			
			# Grant user +1 action
			generic.command.raiseStat(actor, 'act', 1)

	def determineRange():
		commandRange = generic.rangeFactors.lightning()

		length = generic.extentInfluence.polynomial(1,1)
		commandRange['range'] = shapes.line(length)

		commandRange['specialSpaces'] = [[0,1]]

		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(26, 8, 4)
	
	def description():
		return ('.')
	
	def name():
		return 'Passage Bolt'
	
	def icon():
		return 'S_Thunder_04.png'

	def tags():
		return ['targets', 'extends']
class stunBeam:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		if generic.command.hitCheck(target, factors):
			generic.command.raiseStat(target, 'mv', -2)

	def determineRange():
		commandRange = generic.rangeFactors.lightning()

		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Lower targets spedd by 2.')
	
	def name():
		return 'Stun Beam'
	
	def icon():
		return 'S_Light_01.png'

	def tags():
		return ['targets']

'Wind'
class birdcall:
	def perform(actor):
		# Make a copy of target and place it
		unit = generic.objects.bird()
		unit['align'] = actor['align']
		
		generic.command.addObjects(unit)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = shapes.diamond(3, 1)
		commandRange['specialSpaces'] = shapes.single()

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
class aeroImpact:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		factors['force'] *= 0.8

		# move target
		generic.command.move(target)
		
		if generic.command.hitCheck(target, factors):
			# Deal damage
			generic.command.standardAttack(target, factors)				
	
	def determineRange():
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
		return generic.extentInfluence.polynomial(0, 3, 9)
	
	def description():
		return ('Send a burst of air at an adjacent unit.\n\n'
			'Standard magic damage and move target backwards.\n'
			'Push target further by spending more.')
	
	def name():
		return 'Aero Impact'
	
	def icon():
		return 'S_Physic_02.png'

	def tags():
		return ['targets', 'extends']
class galeCloak:
	def perform(actor, target):
		generic.command.raiseStat(target, 'toughness', 50)
		generic.command.raiseStat(target, 'willpower', 50)
		generic.command.raiseStat(target, 'agility', 50)
		generic.command.raiseStat(target, 'mv', 3)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = shapes.diamond(2)

		generic.range.free(commandRange)
	
	def cost():
		return 70
	
	def description():
		return ('Cloak a nearby unit in powerful wind.\n\n'
			'Raise target\'s defensive abilities and mv.')
	
	def name():
		return 'Gale Cloak'
	
	def icon():
		return 'S_Wind_02.png'

	def tags():
		return ['targets']
class fly:
	def perform(actor):
		generic.command.move(actor)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['okDz'] = {'max' : 10, 'min' : -10}

		length = generic.extentInfluence.polynomial(1, 1)
		commandRange['range'] = shapes.diamond(length, 1)
		commandRange['specialSpaces'] = shapes.single()

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(20, 17, 5)
	
	def description():
		return ('Beats taking the bus.')
	
	def name():
		return 'Fly'
	
	def icon():
		return 'S_Wind_06.png'

	def tags():
		return ['extends']

'Earth'
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
				
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()
		
		# Hit all units in actors sightline of length = _extent_
		length = 1 + logic.globalDict['extent']
		commandRange['aoe'] = shapes.line(length)
		
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(0, 16, 9)
	
	def description():
		return ('Send mud cardinally. Hit all units in its path.\n\n'
			'Standard magic damage to all units in mud\'s path.\n'
			'All units that are hit have their movement lowered for the next turn.\n'
			'Spend more to send mud farther and lower movement by more.')
	
	def name():
		return 'Mudshot'
	
	def icon():
		return 'S_Earth_05.png'

	def tags():
		return ['targets', 'extends']
class stoneGarden:
	def perform(actor, target):
		# Add a rock on each side
		# 4 rocks in total
		units = []
		for i in range(0,4):
			units.append(generic.objects.rock())

		generic.command.addObjects(*units)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()

		commandRange['specialSpaces'] = shapes.ring(1)

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
		amount = generic.extentInfluence.polynomial(8, 5)

		# Raise toughness by amount
		generic.command.raiseStat(target, 'toughness', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = shapes.diamond(2)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(0, 14, 7)
	
	def description():
		return ('Cloak a nearby unit in tough stone.\n\n'
			'TODO.')
	
	def name():
		return 'Stone Armor'
	
	def icon():
		return 'S_Earth_06.png'

	def tags():
		return ['targets', 'extends']
class earthGrip:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		if generic.command.hitCheck(target, factors):
			# Lower mc to zero, but don't raise it
			if target['mv'] > 0:
				generic.command.scaleStat(target, 'mv', 0)

			# Deal damage
			generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		# Max distance to target
		distance = generic.extentInfluence.polynomial(1, 1)
		commandRange['range'] = shapes.line(distance)

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

	def tags():
		return ['targets', 'extends']

'Water'
class iceShard:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)

	def determineRange():
		commandRange = generic.rangeFactors.standard()

		reach = generic.extentInfluence.polynomial(1, 1)
		commandRange['range'] = shapes.diamond(reach, 1)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(0, 5, 5)
	
	def description():
		return ('Pretty basic.')
	
	def name():
		return 'Ice Shard'
	
	def icon():
		return 'S_Ice_03.png'

	def tags():
		return ['targets', 'extends']
class crystallineCluster:
	def perform(actor):
		# Basic ice object
		unit = generic.objects.ice()
		unit['align'] = actor['align']
		
		generic.command.addObjects(unit)

		# Once an ice makes an ice, it can't loses the ability to make more
		if actor['model'] == 'ice':
			generic.command.loseCommand(actor, 'crystallineCluster')

	def determineRange():
		commandRange = generic.rangeFactors.standard()

		reach = generic.extentInfluence.polynomial(1, 1)
		commandRange['range'] = shapes.diamond(reach, 1)

		commandRange['specialSpaces'] = shapes.single()

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(100, 5, 5)
	
	def description():
		return ('Make an ice crystal.')
	
	def name():
		return 'Crystalline Cluster'
	
	def icon():
		return 'S_Ice_01.png'
class icePrison:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		if generic.command.hitCheck(target, factors):
			generic.command.raiseStat(target, 'move', -1)
			generic.command.raiseStat(target, 'mv', -1)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		# Max distance to target
		distance = generic.extentInfluence.polynomial(1, 1)
		commandRange['range'] = shapes.diamond(distance, 1)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(14, 6, 6)
	
	def description():
		return ('Enclose nearby unit in ice, lowering their movement.' + '\n\n'
				'TODO.')
	
	def name():
		return 'Ice Prison'
	
	def icon():
		return 'S_Ice_07.png'

	def tags():
		return ['targets', 'extends']
class typhoon:
	def perform(actor, target):
		# Raise mv
		amount = generic.extentInfluence.polynomial(1, 1)
		generic.command.raiseStat(target, 'mv', amount)

		# Raise act
		generic.command.raiseStat(target, 'act', 1)		

	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = shapes.diamond(1)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(20, 20)
	
	def description():
		return ('Required to move quickly.')
	
	def name():
		return 'Typhoon'
	
	def icon():
		return 'S_Water_05.png'

	def tags():
		return ['targets', 'extends']
class blessedWave:
	def perform(actor, *targets):
		multiplier = generic.extentInfluence.polynomial(1, 1/3)

		for target in targets:
			factors = generic.commandFactors.magic(actor, target)
			
			factors['force'] *= multiplier
			factors['accuracy'] *= multiplier

			if generic.command.hitCheck(target, factors):
				# If target is an enemy, damage it
				# If target is an ally, heal it
				if target['align'] != actor['align']:
					generic.command.standardAttack(target, factors)
				
				else:
					amount = 100 * multiplier
					generic.command.raiseStat(target, 'hp', amount)


	def determineRange():
		commandRange = generic.rangeFactors.standard()

		reach = generic.extentInfluence.polynomial(0, 1)
		commandRange['aoe'] = shapes.diamond(reach)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(0, 24, 17, 7)
	
	def description():
		return ('Pretty basic.')
	
	def name():
		return 'Blessed Wave'
	
	def icon():
		return 'S_Water_03.png'

	def tags():
		return ['targets', 'extends']


'Shadow'
class toxins:
	def perform(actor, *targets):
		choice = logic.globalDict['commandChoices'][0]['value']
		loweredStat = choice

		for target in targets:
			factors = generic.commandFactors.magic(actor, target)
			
			if generic.command.hitCheck(target, factors):
				# Lower unit's given stat
				generic.command.raiseStat(target, loweredStat, -10)

	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['aoe'] = shapes.diamond(2, 1)

		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Lower one of several stats.')
	
	def name():
		return 'Toxins'
	
	def icon():
		return 'S_Poison_01.png'

	def determineChoices():
		choices = logic.globalDict['commandChoices']

		for stat in ['strength', 'intelligence', 'toughness', 'willpower', 'accuracy', 'agility']:
				
			pair = {'value' : stat,
					'display' : stat.capitalize()}

			choices.append(pair)

	def tags():
		return ['targets']


# TODO(kgeffen) Add dying triggers and make bubbles burst when killed
class bubble:
	def perform(actor):
		# Basic ice object
		unit = generic.objects.bubble()
		unit['align'] = actor['align']
		
		generic.command.addObjects(unit)

	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['specialSpaces'] = shapes.single()

		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Make an exploding bubble.')
	
	def name():
		return 'Bubble'
	
	def icon():
		return 'S_Water_07.png'




'''Items'''
'Books'
class study:
	def perform(actor, target):
		generic.command.regen(actor)
	
	def determineRange():
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

	def tags():
		return ['targets']
class tutor:
	def perform(actor, target):
		generic.command.regen(target)
	
	def determineRange():
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

	def tags():
		return ['targets']

'Boots'
class dash:
	def perform(actor, target):
		generic.command.raiseStat(actor, 'mv', 2)
	
	def determineRange():
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

	def tags():
		return ['targets']


'''Skill'''
'Boosts'
class strengthen:
	def perform(actor, target):
		generic.command.raiseStat(actor, 'strength', 10)
	
	def determineRange():
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

	def tags():
		return ['targets']
class smarten:
	def perform(actor, target):
		generic.command.raiseStat(actor, 'intelligence', 10)
	
	def determineRange():
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

	def tags():
		return ['targets']
class focus:
	def perform(actor, target):
		generic.command.raiseStat(actor, 'focus', 10)
	
	def determineRange():
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

	def tags():
		return ['targets']

'Food'
class eatMeat:
	def perform(actor, target):
		generic.command.raiseStat(actor, 'hp', 100)
		generic.command.raiseStat(actor, 'strength', 5)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Contains protein.')
	
	def name():
		return 'Eat Meat'
	
	def icon():
		return 'I_C_Meat.png'

	def tags():
		return ['targets']
class eatPie:
	def perform(actor, target):
		generic.command.raiseStat(actor, 'hp', 100)
		generic.command.raiseStat(actor, 'mv', 1)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Sugary, will make you run around.')
	
	def name():
		return 'Eat Pie'
	
	def icon():
		return 'I_C_Pie.png'

	def tags():
		return ['targets']
class eatCarrot:
	def perform(actor, target):
		generic.command.raiseStat(actor, 'hp', 100)
		generic.command.raiseStat(actor, 'focus', 5)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Sharpens eyesight.')
	
	def name():
		return 'Eat Carrot'
	
	def icon():
		return 'I_C_Carrot.png'

	def tags():
		return ['targets']
class eatFish:
	def perform(actor, target):
		generic.command.raiseStat(actor, 'hp', 100)
		generic.command.raiseStat(actor, 'intelligence', 5)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Makes you brainy.')
	
	def name():
		return 'Eat Fish'
	
	def icon():
		return 'I_C_RawFish.png'

	def tags():
		return ['targets']

'Other'
class firstAid:
	def perform(actor, *targets):
		for target in targets:
			generic.command.raiseStat(target, 'hp', 50)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['aoe'] = shapes.flatLine(1)

		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('IDK bandages and kisses.')
	
	def name():
		return 'First Aid'
	
	def icon():
		return 'I_Antidote.png'

	def tags():
		return ['targets']
class dualSharpen:
	def perform(actor, target):
		generic.command.raiseStat(actor, 'strength', 8)
		generic.command.raiseStat(target, 'strength', 8)
	
	def determineRange():
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

	def tags():
		return ['targets']
class bloodRitual:
	def perform(actor, target):
		# Lower hp
		dHp = -round( actor['health'] / 8 )
		generic.command.raiseStat(actor, 'hp', dHp)

		generic.command.raiseStat(actor, 'strength', 20)
		generic.command.raiseStat(actor, 'intelligence', 20)
		generic.command.regen(actor)
	
	def determineRange():
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

	def tags():
		return ['targets']
class vileRitual:
	def perform(actor):
		# Hurt self
		generic.command.raiseStat(actor, 'hp', -100)

		# Make a Husk
		unit = copy.deepcopy(actor)

		unit['hp'] = 1
		unit['health'] = 1
		unit['sp'] = 0
		unit['mv'] = unit['move']
		unit['act'] = unit['actions']
		unit['name'] = 'Husk'

		generic.command.addObjects(unit)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = shapes.line(3)

		commandRange['specialSpaces'] = shapes.single()

		generic.range.rigid(commandRange)
	
	def cost():
		return 100
	
	def description():
		return ('Split your body and soul!\n\n'
			'TODO.')
	
	def name():
		return 'Vile Ritual'
	
	def icon():
		return 'I_Bone.png'


class craft:
	def perform(actor):
		unit = generic.objects.barrel()

		generic.command.addObjects(unit)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['specialSpaces'] = shapes.single()

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



'''Special'''
class deploy:
	def perform(actor):
		choice = logic.globalDict['commandChoices'][0]['value']
		unit = choice
		# TODO(kgeffen) This is included because, as scaffolding, generic units are deployed, and aren't removed
		# from list of undeployed units. Once units can only be added once, remove the followind line
		unit = copy.deepcopy(choice)

		generic.command.addObjects(unit)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['specialSpaces'] = shapes.single()

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
class burst:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.magic(actor, target)

			# Deal damage - Attack always hits
			generic.command.standardAttack(target, factors)

	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['aoe'] = shapes.diamond(1)

		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('POP!')
	
	def name():
		return 'Burst'
	
	def icon():
		return 'S_Water_07.png'


