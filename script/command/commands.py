# Contains all of the damage and range calculations for all commands

# TODO(kgeffen) Remove range descriptions in command descriptions once
# visual display of range exists

# Dynamically called by commandControl.py
# NOTE(kgeffen) Class names start with lowercase for ease of use
from bge import logic
import copy, random

from script.command import generic
from script.command.generic import shapes, extentInfluence

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
		return ('Slash an adjacent unit with your sword')
	
	def name():
		return 'Slash'
	
	def icon():
		return 'W_Sword_001.png'

	def tags():
		return ['targets']
class gloryStrike:
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)
		
		if generic.command.hitCheck(target, factors):
			# Attack (Don't take altered attack into consideration)
			generic.command.standardAttack(target, factors)
			
			# Raise strength
			generic.command.raiseStat(actor, 'strength', 10)
	
	def determineRange():
		commandRange = generic.rangeFactors.sword()
		generic.range.rigid(commandRange)
	
	def cost():
		return 15
	
	def description():
		return ('The battle rages against the unjust and the vile. In such a time, can glory be found anywhere but in battle?\n\n'
				'Basic sword attack\n'
				'+8 Strength')
	
	def name():
		return 'Glory Strike'
	
	def icon():
		return 'S_Sword_06.png'

	def tags():
		return ['targets']

class flameSlash:
	def perform(actor, target):
		multiplier = extentInfluence.polynomial(1, 1/10)

		factors = generic.commandFactors.physical(actor, target)

		factors['force'] *= multiplier
		factors['accuracy'] *= multiplier
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()
		generic.range.rigid(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 9, 1)
	
	def description():
		return ('Slash an adjacent unit with your sword.\n'
				'Wreath your sword in flames by channeling spirit into it.\n'
				'+10X% Damage')
	
	def name():
		return 'Blaze Slash'
	
	def icon():
		return 'W_Sword_016.png'

	def tags():
		return ['targets', 'extends']
class shadeSlash:
	def perform(actor, target):
		factors = generic.commandFactors.physical(actor, target)
		
		if generic.command.hitCheck(target, factors):
			# Deal damage
			generic.command.standardAttack(target, factors)

			# Lower sp
			amount = 0.9 ** extentInfluence.polynomial(0, 1)
			generic.command.scaleStat(target, 'sp', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()
		generic.range.rigid(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 10, 0)
	
	def description():
		return ('Slash an adjacent unit with your sword.\n' 
				'Wreath your sword in ravenous shadows by channeling spirit into it.\n\n'
				'-10% Sp X times\n'
				'(For example, X = 1 lowers target\'s sp by 10%. X = 1 lowers it by 19%)')
	
	def name():
		return 'Shade Slash'
	
	def icon():
		return 'W_Sword_019.png'

	def tags():
		return ['targets', 'extends']
class grandEntrance:
	def perform(actor, *targets):
		multiplier = generic.extentInfluence.polynomial(1.5, 1/2)

		generic.command.move(actor)

		for target in targets:
			# TODO(kgeffen) Move actor before getting targets, the only reason that
			# this is necessary is because actor can hit self before moving
			if target != actor:
				factors = generic.commandFactors.physical(actor, target)
				
				# Raise atack's force and accuracy
				factors['force'] *= multiplier
				factors['accuracy'] *= multiplier
				
				if generic.command.hitCheck(target, factors):
					generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()
		
		# How far from user center of aoe can be
		reach = extentInfluence.polynomial(2, 2)
		commandRange['range'] = shapes.diamond(reach, 1)
		
		# How large the meteor is
		length = generic.extentInfluence.polynomial(1, 1)
		commandRange['aoe'] = shapes.diamond(length, 1)

		# Center of diamond is where user moves to
		commandRange['specialSpaces'] = shapes.single()
		
		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(100, 50, 40, 10)
	
	def description():
		return ('Jump into the fray, damaging all units X + 1 spaces from wherever you land.\n'
				'150% + 50X% Damage\n'
				'150% + 50X% Accuracy')
	
	def name():
		return 'Grand Entrance'
	
	def icon():
		return 'W_Sword_013.png'

	def tags():
		return ['targets', 'extends']
class ribbonDash:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.sword(actor, target)
			
			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
		
		# Move forward
		generic.command.move(actor)

	def determineRange():
		commandRange = generic.rangeFactors.sword()
		
		length = extentInfluence.polynomial(1, 1)
		
		commandRange['aoe'] = generic.shapes.line(length)
		commandRange['specialSpaces'] = [[0, length]]
		
		generic.range.rigid(commandRange)
	
	def cost():
		return extentInfluence.polynomial(20, 5, 5)
	
	def description():
		return ('Move forward X + 2 spaces, damaging anything in your path.\n'
				'Cannot be used if no units stand in your path.')
	
	def name():
		return 'Ribbon Dash'
	
	def icon():
		return 'W_Sword_004.png'

	def tags():
		return ['targets', 'extends']
class greatCross:
	def perform(actor, *targets):
		multiplier = extentInfluence.polynomial(4/3, 1/3)

		for target in targets:
			factors = generic.commandFactors.sword(actor, target)
			
			factors['force'] *= multiplier
			factors['accuracy'] *= multiplier

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.sword()

		length = extentInfluence.polynomial(1, 1)
		commandRange['aoe'] = shapes.cross(length, offset = 1)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(100, 0, 100)
	
	def description():
		return ('Hit all units up to X + 1 spaces from you in any direction\n'
				'133% + 33X% Damage\n'
				'133% + 33X% Accuracy')
	
	def name():
		return 'Great Cross'
	
	def icon():
		return 'W_Sword_010.png'

	def tags():
		return ['targets', 'extends']


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
		return ('With a mighty swing, cleave anything beside you in 2.\n\n'
				'Basic sword attack\n'
				'200% damage')
	
	def name():
		return 'Cleave'
	
	def icon():
		return 'W_Sword_011.png'

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
		offset = [0, generic.extentInfluence.polynomial(0, 1)]
		commandRange['range'] = shapes.push(shapes.single(), offset)

		# Space to move to
		# TODO(kgeffen) Allow 'specialSpace' to be in same space as user
		if logic.globalDict['extent'] > 0:
			commandRange['specialSpaces'] = [[0,-1]]
		
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(10, 2, 1)
	
	def description():
		return ('The world is yours to conquer and control. Descend as a bird would upon its prey.\n\n'
				'Jump forward X spaces, strike the unit in front of you\n'
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
		
		factors['accuracy'] *= 1.2

		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
		
		# Move backwards
		# TODO(kgeffen) Remove conditional once special space can be in same space as actor
		if logic.globalDict['extent'] > 0:
			generic.command.move(actor)
	
	def determineRange():
		commandRange = generic.rangeFactors.sword()
		
		# Space X spaces behind actor
		distance = generic.extentInfluence.polynomial(0, 1)
		# NOTE(kgeffen) distance + 1 since -1 = actor's space,
		# not space behind actor
		# TODO(kgeffen) Allow special space to be on same space as actor
		if distance > 0:
			commandRange['specialSpaces'] = [[0, -( distance + 1 )]]
		
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(1, 1, 1)
	
	def description():
		return ('Even as you enter the fray, you feel the ineffable pull from the horrors of battle.\n\n'
				'Strike unit beside you, move back X spaces\n'
				'120% Accuracy')
	
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
		return 36
	
	def description():
		return ('Bring your huge sword down upon your foes.\n\n'
				'Hit up to 3 units in your sightline\n'
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
		return ('Thrust your spear at a nearby unit.\n\n'
				'Hits any unit 2 spaces away')
	
	def name():
		return 'Thrust'
	
	def icon():
		return 'W_Spear_001.png'

	def tags():
		return ['targets']
class frigidThrust:
	def perform(actor, target):
		factors = generic.commandFactors.spear(actor, target)
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)

			# Lower target's mv
			amount = -extentInfluence.polynomial(0, 1)
			generic.command.raiseStat(target, 'mv', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.spear()
		generic.range.free(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 5, 10)
	
	def description():
		return ('Thrust your spear at any unit 2 spaces from you. Cloak your spear in frigid ice by channeling your spirit into it.\n'
				'-X Mv for one turn')
	
	def name():
		return 'Frigid Thrust'
	
	def icon():
		return 'W_Spear_015.png'

	def tags():
		return ['targets', 'extends']
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
				'Basic spear attack X + 1 times\n'
				'+1 Act')
	
	def name():
		return 'Lightning Javelin'
	
	def icon():
		return 'W_Spear_016.png'

	def tags():
		return ['targets', 'extends']
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
		return 38
	
	def description():
		return ('Judgement is made and the punishment is delivered.\n\n'
				'Powerful spear attack against all units 2 spaces from you\n'
				'140% Damage\n'
				'140% Accuracy')
	
	def name():
		return 'Guilltine Spiral'
	
	def icon():
		return 'W_Spear_008.png'

	def tags():
		return ['targets']

'Axe'
class shatter:
	def perform(actor, target):
		factors = generic.commandFactors.sword(actor, target)

		if generic.command.hitCheck(target, factors):

			# If target is rock, destroy it automatically
			if target['model'] == 'rock':
				generic.command.scaleStat(target, 'hp', 0)
			else:
				# Deal standard damage
				generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.sword()
		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Shatter anything in front of you with a swing of your club.\n'
				'Destroys rocks automatically')
	
	def name():
		return 'Shatter'
	
	def icon():
		return 'W_Mace_012.png'

	def tags():
		return ['targets']

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
		return ('Chop down anything beside you with your axe.\n\n'
				'Basic axe attack')
	
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
		return 38
	
	def description():
		return ('Split the ground to create a gaping maw, hungry for blood.\n\n'
				'Hit up to 3 units in your sightline\n'
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
		return ('Break the earth with an incedibly powerful swing of your axe.\n\n'
				'Hit all units surrounding you\n'
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
				'120% Accuracy\n'
				'-20% Willpower, intelligence for target.')
	
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
		return ('Shatter everything those before you hold as true. Leave them weak and wounded.\n\n'
				'Hit up to 3 units in line in front of you\n'
				'120% Accuracy\n'
				'-20% Toughness, strength for target')
	
	def name():
		return 'Crack Foundation'
	
	def icon():
		return 'W_Mace_012.png'

	def tags():
		return ['targets']

'Dagger'
class assassinate:
	def perform(actor, target):
		factors = generic.commandFactors.dagger(actor, target)

		factors['force'] *= 3
		factors['accuracy'] *= 3

		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.dagger()

		# commandRange['specialSpaces'] = hollowSquare

		generic.range.rigid(commandRange)
	
	def cost():
		return 250
	
	def description():
		return ('Silent.\n'
				'')
	
	def name():
		return 'Assassinate'
	
	def icon():
		return 'W_Dagger_007.png'

	def tags():
		return ['targets']


'Wand'
class psiStrike:
	def perform(actor, target):
		multiplier = extentInfluence.polynomial(1, 1/10)

		factors = generic.commandFactors.magic(actor, target)

		factors['force'] *= multiplier
		factors['accuracy'] *= multiplier
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.sword()
		generic.range.rigid(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 9, 1)
	
	def description():
		return ('Is there ever an escape from the familiarity and guilty comfort of conflict?\n\n'
				'Basic sword attack')
	
	def name():
		return 'Psi-Strike'
	
	def icon():
		return 'W_Wand_06.png'

	def tags():
		return ['targets', 'extends']

'Bow'
class withertipVolley:
	def perform(actor, target):
		factors = generic.commandFactors.physical(actor, target)

		if generic.command.hitCheck(target, factors):
			# Lower target's defensive stats
			amount = 0.8 ** extentInfluence.polynomial(1, 1)

			generic.command.scaleStat(target, 'toughness', amount)
			generic.command.scaleStat(target, 'willpower', amount)
			generic.command.scaleStat(target, 'agility', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.bow()
		generic.range.free(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 20, 10)
	
	def description():
		return ('Shoot any unit up to 5 spaces away with a poisonous arrow that lowers defensive abilities.\n\n'
				'-20% Toughness, willpower, agility X + 1 times\n\n'
				'(Example: X = 1 lowers toughness by 20% of total toughness, X = 2 lowers toughness by 36% of total toughness.')
	
	def name():
		return 'Withertip Volley'
	
	def icon():
		return 'W_Bow_03.png'

	def tags():
		return ['targets', 'extends']
class poisonShot:
	def perform(actor, target):
		# Poison target
		generic.command.addTrait(target, 'Poisoned')
	
	def determineRange():
		commandRange = generic.rangeFactors.bow()
		generic.range.free(commandRange)
	
	def cost():
		return extentInfluence.polynomial(120)
	
	def description():
		return ('Shoot any unit up to 5 spaces away with a poisonous arrow that poisons them.\n\n'
				'')
	
	def name():
		return 'Poison Shot'
	
	def icon():
		return 'W_Bow_13.png'

	def tags():
		return ['targets']
class starshower:
	def perform(actor, _):

		targets = [unit for unit in logic.globalDict['units'] if unit != actor]
		

		for target in targets:

			factors = generic.commandFactors.bow(actor, target)
			factors['force'] *= extentInfluence.polynomial(1, 1/2)
			factors['accuracy'] *= 2

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 100)
	
	def description():
		return ('Hit everyone.\n\n'
				'')
	
	def name():
		return 'Starshower'
	
	def icon():
		return 'W_Bow_15.png'

	def tags():
		return ['extends']


'''Magic'''
'Fire'
class burn:
	def perform(actor, target):
		multiplier = extentInfluence.polynomial(1, 1/10)

		factors = generic.commandFactors.magic(actor, target)

		factors['force'] *= multiplier
		factors['accuracy'] *= multiplier
		
		if generic.command.hitCheck(target, factors):
			generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()
		generic.range.rigid(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 9, 1)
	
	def description():
		return ('Burn an adjacent unit with mystical flames\n'
				'+10X% Damage\n'
				'+10X% Accuracy')
	
	def name():
		return 'Burn'
	
	def icon():
		return 'S_Fire_03.png'

	def tags():
		return ['targets', 'extends']
class meteor:
	def perform(actor, *targets):
		multiplier = generic.extentInfluence.polynomial(1.5, 1/2)

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
		reach = generic.extentInfluence.polynomial(2, 2)
		commandRange['range'] = shapes.diamond(reach)
		
		# How large the meteor is
		length = generic.extentInfluence.polynomial(1, 1)
		commandRange['aoe'] = shapes.diamond(length)
		
		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(100, 50, 40, 10)
	
	def description():
		return ('Summon a giant meteor from outer space\n\n'
				'Meteor has radius X + 1\n'
				'Centered up to X + 2 spaces away\n'
				'150% +50X% Damage\n'
				'150% +50X% Accuracy\n')
	
	def name():
		return 'Meteor'
	
	def icon():
		return 'S_Fire_05.png'

	def tags():
		return ['targets', 'extends']
class livingFlame:
	def perform(actor):
		# Make a copy of target and place it
		spawn = generic.objects.flame()
		spawn['align'] = actor['align']
		
		generic.command.addObjects(spawn)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		reach = generic.extentInfluence.polynomial(1, 1)
		commandRange['range'] = shapes.diamond(reach, 1)

		commandRange['specialSpaces'] = shapes.single()

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(100, 5, 5)
	
	def description():
		return ('A flame bursts to life by your hand, ready to consume and spread.\n\n'
				'Summon a flame up to X + 1 spaces away')
	
	def name():
		return 'Living Flame'
	
	def icon():
		return 'S_Fire_02.png'

	def tags():
		return ['extends']
class blazeCloak:
	def perform(actor, target):
		amount = extentInfluence.polynomial(5, 5)

		generic.command.raiseStat(target, 'intelligence', amount)
		generic.command.raiseStat(target, 'strength', amount)
		generic.command.raiseStat(target, 'focus', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = shapes.diamond(1)

		generic.range.free(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 15, 5)
	
	def description():
		return ('Cloak yourself or a unit beside you in flame to raise its offensive stats\n'
				'+5 +5X Intelligence, strength, focus')
	
	def name():
		return 'Blaze Cloak'
	
	def icon():
		return 'S_Fire_04.png'

	def tags():
		return ['targets', 'extends']

'Light'
class emogen:
	def perform(actor, *targets):
		# Amount of healing
		amount = generic.extentInfluence.polynomial(100, 50)

		for target in targets:
			generic.command.raiseStat(target, 'hp', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()

		commandRange['aoe'] = shapes.diamond(1)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(0, 15, 5)
	
	def description():
		return ('Save us, save us all from death and damnation, from sin and sacrilege.\n\n'
				'Heal yourself and anyone beside you\n'
				'Heal each unit by 100 + 50X hp')
	
	def name():
		return 'Emogen'
	
	def icon():
		return 'S_Magic_01.png'

	def tags():
		return ['targets', 'extends']
class chainLightning:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)

		factors['force'] *= 0.5
		factors['accuracy'] *= 2

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
		return ('The light flashes, the world changes. The speed of it all is so dangerously appealing.\n\n'
				'Strike X + 1 times\n'
				'50% Damage\n'
				'200% Accuracy\n'
				'+1 Act')
	
	def name():
		return 'Chain Lightning'
	
	def icon():
		return 'S_Thunder_05.png'

	def tags():
		return ['targets', 'extends']
class passageBolt:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)

		# Move user
		generic.command.move(actor)

		if generic.command.hitCheck(target, factors):
			# Attack
			generic.command.standardAttack(target, factors)

	def determineRange():
		commandRange = generic.rangeFactors.standard()

		# Single space pushed X spaces away
		offset = [0, generic.extentInfluence.polynomial(0, 1)]
		commandRange['range'] = shapes.push(shapes.single(), offset)

		# Space beyond target
		commandRange['specialSpaces'] = [[0,1]]

		generic.range.rigid(commandRange)
	
	def cost():
		return extentInfluence.polynomial(20, 5, 5)
	
	def description():
		return ('Move quickly through the world, sure of where you\'re headed. In the light, all things become clear.\n\n'
				'Deal standard magic damage to and move past any unit X + 1 spaces away')
	
	def name():
		return 'Passage Bolt'
	
	def icon():
		return 'S_Thunder_04.png'

	def tags():
		return ['targets', 'extends']

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
		return ('Alone, a bird is weak, but don\'t be so foolish as to doubt a flock.\n\n'
				'Summon a swift bird up to 3 spaces away')
	
	def name():
		return 'Birdcall'
	
	def icon():
		return 'I_Feather_01.png'
class gust:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)

		# move target
		if logic.globalDict['extent'] != 0:
			generic.command.move(target)
		
		if generic.command.hitCheck(target, factors):
			# Deal damage
			generic.command.standardAttack(target, factors)				
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()
		
		# Move target back Number of spaces equal to extent
		distance = generic.extentInfluence.polynomial(0, 1)
		if distance != 0:
			commandRange['specialSpaces'] = [[0, distance]]
		
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(0, 3, 5)
	
	def description():
		return ('Hit anything beside you with a burst of air, knocking it backwards\n'
				'Damage and push back any adjacent unit (Push back X spaces)')
	
	def name():
		return 'Gust'
	
	def icon():
		return 'S_Physic_02.png'

	def tags():
		return ['targets', 'extends']
class galeCloak:
	def perform(actor, target):
		amount = extentInfluence.polynomial(1, 1)
		generic.command.raiseStat(target, 'mv', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['range'] = shapes.diamond(1)

		generic.range.free(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 10, 10)
	
	def description():
		return ('Don a cloak of wind to see the world.\n\n'
				'Cloak yourself or a unit beside you.\n'
				'+1 +X Mv for one turn\n'
				'(Protip: Works on bases.)')
	
	def name():
		return 'Gale Cloak'
	
	def icon():
		return 'S_Wind_02.png'

	def tags():
		return ['targets', 'extends']

'Earth'
class mudshot:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.magic(actor, target)

			if generic.command.hitCheck(target, factors):
				
				# Lower mv
				amount = -extentInfluence.polynomial(0, 1)
				generic.command.raiseStat(target, 'mv', amount)

				# Deal damage
				generic.command.standardAttack(target, factors)
				
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()
		
		length = extentInfluence.polynomial(1, 1)
		commandRange['aoe'] = shapes.line(length)
		
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(0, 7, 6)
	
	def description():
		return ('Earth and water forms the mud. A delicate balance of fluidity and stability.\n\n'
				'Damage and lower the movement of any units up to X + 1 spaces from you in one direction\n'
				'-X Mv for one turn')
	
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
		return ('Isolate yourself. Give yourself time to plan and grow.\n\n'
				'Summon a rock on each side of you')
	
	def name():
		return 'Stone Garden'
	
	def icon():
		return 'S_Earth_04.png'

'Water'
class gush:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.magic(actor, target)

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		radius = extentInfluence.polynomial(1, 1)
		commandRange['aoe'] = shapes.diamond(radius, 1)

		generic.range.free(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 15, 5)
	
	def description():
		return ('Unleash a barrage of flame upon a nearby foe.\n\n'
				'Hit anything up to X + 1 spaces away\n'
				'Standard magic attack X + 1 times')
	
	def name():
		return 'Gush'
	
	def icon():
		return 'S_Water_02.png'

	def tags():
		return ['targets', 'extends']
class crashingWave:
	def perform(actor, *targets):
		multiplier = generic.extentInfluence.polynomial(4/3, 1/3)

		for target in targets:
			factors = generic.commandFactors.magic(actor, target)
			
			factors['force'] *= multiplier
			factors['accuracy'] *= multiplier

			if generic.command.hitCheck(target, factors):
				generic.command.standardAttack(target, factors)

	def determineRange():
		commandRange = generic.rangeFactors.standard()

		length = generic.extentInfluence.polynomial(0, 1)
		rectangle = shapes.rectangle(1, length)
		commandRange['aoe'] = shapes.push(rectangle, [0, length])

		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(100, 0, 100)
	
	def description():
		return ('Summon a massive wave to come crashing down in front of you\n'
				'Wave width is 3, moves forward 1 + 2X spaces\n'
				'133% +33X% Damage\n'
				'133% +33X% Accuracy')
	
	def name():
		return 'Crashing Wave'
	
	def icon():
		return 'S_Water_03.png'

	def tags():
		return ['targets', 'extends']

class icePrison:
	def perform(actor, target):
		factors = generic.commandFactors.magic(actor, target)
		
		if generic.command.hitCheck(target, factors):
			amount = -extentInfluence.polynomial(1, 1)
			generic.command.raiseStat(target, 'mv', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		# Max distance to target
		distance = generic.extentInfluence.polynomial(1, 1)
		commandRange['range'] = shapes.diamond(distance, 1)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(0, 6, 4)
	
	def description():
		return ('Imprison any unit up to X + 1 spaces from you, temporarily lowering their movement\n'
				'-1 -X Mv for one turn')
	
	def name():
		return 'Ice Prison'
	
	def icon():
		return 'S_Ice_07.png'

	def tags():
		return ['targets', 'extends']
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
		return ('Cast shards upon the world, they will find their mark and make it too.\n\n'
				'Basic magic attack with range X + 1\n'
				'Perfect for hitting far away units')
	
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

	def determineRange():
		commandRange = generic.rangeFactors.standard()

		reach = generic.extentInfluence.polynomial(1, 1)
		commandRange['range'] = shapes.diamond(reach, 1)

		commandRange['specialSpaces'] = shapes.single()

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(100, 5, 5)
	
	def description():
		return ('Summon a frigid ice crystal up to X + 1 spaces from you')
	
	def name():
		return 'Crystalline Cluster'
	
	def icon():
		return 'S_Ice_01.png'

	def tags():
		return ['extends']

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
		return ('Fluidity of movement, granting a myriad of futures to choose from.\n\n'
				'Affect yourself or a unit beside you\n'
				'+1 +X Mv\n'
				'+1 Act')
	
	def name():
		return 'Typhoon'
	
	def icon():
		return 'S_Water_05.png'

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
		return ('Ascend the ivory tower with no purpose and you will find it empty.\n\n'
				'Regenerate sp')
	
	def name():
		return 'Study'
	
	def icon():
		return 'W_Book_01.png'

	def tags():
		return ['targets']
class tutor:
	def perform(actor, target):
		amount = -generic.command.scaleStat(actor, 'sp', 0)
		generic.command.raiseStat(target, 'sp', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()
		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Ascend the ivory tower with no purpose and you will find it empty.\n\n'
				'Regenerate sp')
	
	def name():
		return 'Tutor'
	
	def icon():
		return 'W_Book_07.png'

	def tags():
		return ['targets']


'Boots'
class dash:
	def perform(actor, target):
		generic.command.raiseStat(target, 'mv', 3)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Concentrate on moving. If you can run, you can survive.\n\n'
				'Move an additional 3 spaces this turn')
	
	def name():
		return 'Dash'
	
	def icon():
		return 'E_Shoes_01.png'

	def tags():
		return ['targets']
class leap:
	def perform(actor):
		# Move self to selected space
		generic.command.move(actor)		
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()
		
		reach = extentInfluence.polynomial(1, 1)
		commandRange['range'] = shapes.diamond(reach, 1)

		commandRange['specialSpaces'] = generic.shapes.single()
		
		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(0, 8, 4)
	
	def description():
		return ('Jump around\n'
				'Jump to space')
	
	def name():
		return 'Leap'
	
	def icon():
		return 'E_Shoes_05.png'

	def tags():
		return ['extends']


'Shields'
class defend:
	def perform(actor, target):
		amount = extentInfluence.polynomial(50, 10)

		generic.command.raiseStat(target, 'toughness', amount)
		generic.command.raiseStat(target, 'willpower', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 10)
	
	def description():
		return ('TODO.\n\n'
				'TODO')
	
	def name():
		return 'Defend'
	
	def icon():
		return 'E_Shield_01.png'

	def tags():
		return ['targets', 'extends']


'Gloves'
class throw:
	def perform(actor, target):
		# move target
		generic.command.move(target)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()
		
		# Move target back Number of spaces equal to extent
		distance = generic.extentInfluence.polynomial(1, 1)
		commandRange['specialSpaces'] = [[0, distance]]
		
		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(0, 2, 4)
	
	def description():
		return ('Throw anything beside you back X + 1 spaces')
	
	def name():
		return 'Throw'
	
	def icon():
		return 'W_Fist_06.png'

	def tags():
		return ['targets', 'extends']

'''Skill'''
'Boosts'
class strengthen:
	def perform(actor, target):
		generic.command.raiseStat(target, 'strength', 10)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('+10 Strength')
	
	def name():
		return 'Strengthen'
	
	def icon():
		return 'S_Buff_01.png'

	def tags():
		return ['targets']
class toughen:
	def perform(actor, target):
		amount = extentInfluence.polynomial(20, 2)

		generic.command.raiseStat(target, 'toughness', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 10)
	
	def description():
		return ('Reject weakness and grow strong.\n\n'
				'+20 +2X Strength')
	
	def name():
		return 'Toughen'
	
	def icon():
		return 'S_Buff_02.png'

	def tags():
		return ['targets', 'extends']
class smarten:
	def perform(actor, target):
		amount = extentInfluence.polynomial(20, 2)

		generic.command.raiseStat(target, 'intelligence', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 10)
	
	def description():
		return ('Reject weakness and grow strong.\n\n'
				'+20 +2X Strength')
	
	def name():
		return 'Smarten'
	
	def icon():
		return 'S_Buff_03.png'

	def tags():
		return ['targets', 'extends']
class resist:
	def perform(actor, target):
		amount = extentInfluence.polynomial(20, 2)

		generic.command.raiseStat(target, 'willpower', amount)
	
	def determineRange():
		commandRange = generic.rangeFactors.self()
		generic.range.free(commandRange)
	
	def cost():
		return extentInfluence.polynomial(0, 10)
	
	def description():
		return ('Reject weakness and grow strong.\n\n'
				'+20 +2X Strength')
	
	def name():
		return 'Resist'
	
	def icon():
		return 'S_Buff_04.png'

	def tags():
		return ['targets', 'extends']

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
				'+10 Focus')
	
	def name():
		return 'Focus'
	
	def icon():
		return 'S_Buff_06.png'

	def tags():
		return ['targets']

'Other'
class wait:
	def perform(actor, target):
		# Grant yourself a pending action
		generic.command.addTrait(actor, 'Extra Action')
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()
		generic.range.free(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Have an extra action next turn.\n\n'
				'')
	
	def name():
		return 'Wait'
	
	def icon():
		return 'O_Clock.png'

	def tags():
		return ['targets']

class enlist:
	def perform(actor):
		spawn = generic.objects.squire()
		spawn['align'] = actor['align']
		
		generic.command.addObjects(spawn)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['specialSpaces'] = shapes.single()

		generic.range.rigid(commandRange)
	
	def cost():
		return 100
	
	def description():
		return ('Summon a squire beside you.\n'
				'Squires can attack, and can raise the strength of their allies.')
	
	def name():
		return 'Enlist'
	
	def icon():
		return 'I_Scroll.png'

	def tags():
		return []
class commision:
	def perform(actor):
		spawn = generic.objects.mason()
		spawn['align'] = actor['align']
		
		generic.command.addObjects(spawn)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['specialSpaces'] = shapes.single()

		generic.range.rigid(commandRange)
	
	def cost():
		return 100
	
	def description():
		return ('Commision a stone mason to build for you.'
				'\nHe can create and destroy rocks with ease.')
	
	def name():
		return 'Commision'
	
	def icon():
		return 'I_Scroll_02.png'

	def tags():
		return []
class stoneWall:
	def perform(actor):
		# Spawn 3 rocks
		spawns = []
		for i in range(0, 3):
			spawns.append(generic.objects.rock())

		generic.command.addObjects(*spawns)

	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['specialSpaces'] = shapes.flatLine(1)

		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Create a wall 3 stones long in front of you\n'
				'Great as a blockade')
	
	def name():
		return 'Stone Wall'
	
	def icon():
		return 'I_Rock_01.png'

	def tags():
		return []
class firstAid:
	def perform(actor, *targets):
		for target in targets:
			generic.command.raiseStat(target, 'hp', 200)
	
	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['aoe'] = shapes.flatLine(1)

		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Heal up to 3 units in a line in front of you\n'
				'Heal each unit by 200 hp')
	
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
		return ('Sharpen your blade against the weapon of any unit beside you.\n'
				'+8 Strength for each unit')
	
	def name():
		return 'Dual-Sharpen'
	
	def icon():
		return 'S_Dagger_01.png'

	def tags():
		return ['targets']
class craft:
	def perform(actor):
		# Spawn a rock
		rock = generic.objects.rock()

		generic.command.addObjects(rock)

	def determineRange():
		commandRange = generic.rangeFactors.standard()

		commandRange['specialSpaces'] = shapes.single()

		generic.range.rigid(commandRange)
	
	def cost():
		return 0
	
	def description():
		return ('Place a stone beside you')
	
	def name():
		return 'Craft'
	
	def icon():
		return 'W_Mace_003.png'

	def tags():
		return []


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
		# Newlines so that choices for which unit to deploy are not covered by description
		text = '\n\n'#'Place a unit of your choice onto the field to fight for you.\n\n'

		# Add a description of the unit at the end
		choices = logic.globalDict['commandChoices']
		choice = choices[0]['value']
		unitDescript = choice['descript']

		text += unitDescript

		return (text)
	
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

