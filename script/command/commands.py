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
		 		'Basic sword attack.')
	
	def name():
		return 'Slash'
	
	def icon():
		return 'W_Sword_001.png'

	def tags():
		return ['targets']
class cleave:
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
		return ('Cleave the body of a unit beside you.\n\n'
		 		'Powerful sword attack.\n'
		 		'200% damage')
	
	def name():
		return 'Cleave'
	
	def icon():
		return 'W_Sword_011.png'

	def tags():
		return ['targets']
class gloryStrike:
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
		return 6
	
	def description():
		return ('Strike an adjacent unit and gain strength from the glory of a righteous battle.\n\n'
		 		'Basic sword attack.\n'
		 		'User strength +8')
	
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
		offset = [0, generic.extentInfluence.polynomial(1, 1)]
		commandRange['range'] = shapes.push(shapes.single(), offset)

		# Space to move to
		commandRange['specialSpaces'] = [[0,-1]]
		
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(10, 3, 1)
	
	def description():
		return ('Something poetic and deep about birds and stuff lol.\n\n'
				'Move forward X spaces, strike unit in front.\n'
				'120% Damage')
	
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
		return generic.extentInfluence.polynomial(2, 0, 1)
	
	def description():
		return ('Slash forward as you step backwards (Very zen).\n\n'
				'Strike unit in front, move back X spaces.')
	
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
			
			factors['force'] *= 1.3

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.sword()

		commandRange['aoe'] = shapes.line(3)

		generic.range.rigid(commandRange)
	
	def cost():
		return 32
	
	def description():
		return ('Big like huge.\n\n'
				'Hits all units in 3 spaces in front.\n'
				'130% Damage')
	
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
		return ('Thrust your spear at somebody.\n\n'
				'Basic spear damage against unit 2 spaces away')
	
	def name():
		return 'Thrust'
	
	def icon():
		return 'W_Spear_001.png'

	def tags():
		return ['targets']
class lightningJavelin:
	def perform(actor, target):
		factors = generic.commandFactors.spear(actor, target)

		# Attack N times
		numberTimes = generic.extentInfluence.polynomial(1, 1)
		for i in range(numberTimes):

			# Attack once
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)

		# Grant user an additional act this turn
		generic.command.raiseStat(actor, 'act', 1)
	
	def determineRange():
		commandRange = generic.rangeFactors.spear()
		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(20, 20)
	
	def description():
		return ('Channel the storm into your spear and strike!\n\n'
				'Basic spear attack X times.\n'
				'User can act one more time this turn.')
	
	def name():
		return 'Lightning Javelin'
	
	def icon():
		return 'W_Spear_016.png'

	def tags():
		return ['targets', 'extends']
class beesting:
	def perform(actor, target):
		factors = generic.commandFactors.spear(actor, target)
		
		factors['force'] *= 0.5
		factors['accuracy'] *= 1.5

		if generic.command.hitCheck(target, factors):
			# Attack
			generic.command.standardAttack(target, factors)

			# Lower target's defensive stats
			generic.command.scaleStat(target, 'toughness', 0.8)
			generic.command.scaleStat(target, 'willpower', 0.8)
			generic.command.scaleStat(target, 'agility', 0.8)
	
	def determineRange():
		commandRange = generic.rangeFactors.spear()
		generic.range.free(commandRange)
	
	def cost():
		return 35
	
	def description():
		return ('Venomous spear strike.\n\n'
				'-20% Toughness, willpower, agility on contact.\n'
				'50% Damage\n'
				'150% Accuracy')
	
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
			
			factors['force'] *= 1.4
			factors['accuracy'] *= 1.4

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def determineRange(): 
		commandRange = generic.rangeFactors.spear()

		commandRange['range'] = shapes.single()
		commandRange['aoe'] = shapes.ring(2)

		generic.range.free(commandRange)
	
	def cost():
		return 30
	
	def description():
		return ('Drop the guilltine on all units 2 spaces away.\n\n'
				'Powerful spear attack against all units 2 spaces away.\n'
				'140% Damage\n'
				'140% Accuracy')
	
	def name():
		return 'Guilltine Spiral'
	
	def icon():
		return 'W_Spear_008.png'

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
		 		'Basic axe attack.')
	
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

			factors['force'] *= 1.2
			factors['accuracy'] *= 1.2
			
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.axe()

		commandRange['aoe'] = shapes.line(3)

		generic.range.rigid(commandRange)
	
	def cost():
		return 43
	
	def description():
		return ('Chop down an adjacent unit with your axe.\n\n'
		 		'Hit all units up to 3 spaces away with your axe.\n'
		 		'120% Damage\n'
		 		'120% Accuracy')
	
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
			
			factors['force'] *= 1.8
			factors['accuracy'] *= 1.8

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.axe()

		hollowSquare = shapes.rectangle(1, 1, hollow = True)
		# Push square to be centered space behind (space in front of user)
		commandRange['aoe'] = shapes.push(hollowSquare, [0,-1])

		generic.range.rigid(commandRange)
	
	def cost():
		return 88
	
	def description():
		return ('Break the earth with a powerful swing of your axe.\n\n'
				'Axe damage against all unit surrounding user.\n'
				'180% Damage\n'
				'180% Accuracy')
	
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
			generic.command.scaleStat(target, 'willpower', 0.8)
			generic.command.scaleStat(target, 'intelligence', 0.8)
	
	def determineRange():
		commandRange = generic.rangeFactors.axe()

		generic.range.rigid(commandRange)
	
	def cost():
		return 18
	
	def description():
		return ('Shatter an adjacent unit\'s skull with a mighty swing of your axe.\n\n'
		 		'Axe attack.\n'
		 		'-20% Willpower, intelligence on contact.\n'
		 		'120% Accuracy')
	
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
				generic.command.scaleStat(target, 'toughness', 0.8)
				generic.command.scaleStat(target, 'strength', 0.8)

	def determineRange():
		commandRange = generic.rangeFactors.axe()

		commandRange['aoe'] = shapes.flatLine(1)

		generic.range.rigid(commandRange)
	
	def cost():
		return 27
	
	def description():
		return ('Shatter an adjacent unit\'s skull with a mighty swing of your axe.\n\n'
		 		'Axe attack.\n'
		 		'-20% Toughness, strength on contact.\n'
		 		'120% Accuracy')
	
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

		# Attack N times
		numberTimes = generic.extentInfluence.polynomial(1, 1)
		for i in range(numberTimes):
			# Attack once
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
		
		# Grant user +1 action
		generic.command.raiseStat(actor, 'act', 1)

	def determineRange():
		commandRange = generic.rangeFactors.lightning()

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(25, 25)
	
	def description():
		return ('.')
	
	def name():
		return 'Chain Lightning'
	
	def icon():
		return 'S_Thunder_05.png'

	def tags():
		return ['targets', 'extends']
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
			
			factors['force'] *= 0.8

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
			generic.command.raiseStat(target, 'hp', 100)
	
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
		return ('Sharpen you weapon against a unit beside you.\n\n'
				'+8 Strength for self and target.')
	
	def name():
		return 'Dual-Sharpen'
	
	def icon():
		return 'S_Dagger_01.png'

	def tags():
		return ['targets']
class bloodRitual:
	def perform(actor, target):
		# Lower hp
		dHp = -round( actor['health'] / 6 )
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

