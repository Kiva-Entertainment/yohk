# Contains all of the damage and range calculations for all commands

# TODO(kgeffen) Remove range descriptions in command descriptions once
# visual display of range exists

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
		return ('Is there ever an escape from the familiarity and guilty comfort of conflict?\n\n'
		 		'Basic sword attack')
	
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
		return ('With a mighty swing, cleave anything beside you in 2.\n\n'
				'Basic sword attack\n'
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
		return 8
	
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
		return 32
	
	def description():
		return ('Venomous spear strike. Sting like a bee.\n\n'
				'50% Damage\n'
				'150% Accuracy\n'
				'-20% Toughness, willpower, agility for target')
	
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
		return ('Unleash a barrage of flame upon a nearby foe.\n\n'
				'Hit anything up to X + 1 spaces away\n'
				'Standard magic attack X + 1 times')
	
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
		return ('Summon a huge meteor from outer space.\n\n'
				'Meteor has radius X + 1\n'
				'Centered up to X + 2 spaces away\n'
				'+50X% Damage\n'
				'+50X% Accuracy\n')
	
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
		return ('A flame bursts to life by your hand, ready to consume and spread.\n\n'
				'Summon a flame up to 2 spaces away')
	
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
		return ('Don a cloak of flame to ignite the world.\n\n'
				'Cloak yourself or a unit beside you\n'
				'+20 Intelligence, strength, focus')
	
	def name():
		return 'Blaze Cloak'
	
	def icon():
		return 'S_Fire_04.png'

	def tags():
		return ['targets']

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

		factors['force'] *= 0.5
		factors['accuracy'] *= 2

		# Move user
		generic.command.move(actor)

		if generic.command.hitCheck(target, factors):
			# Attack
			generic.command.standardAttack(target, factors)
			
			# Grant user +1 action
			generic.command.raiseStat(actor, 'act', 1)

	def determineRange():
		commandRange = generic.rangeFactors.standard()

		# Single space pushed X spaces away
		offset = [0, generic.extentInfluence.polynomial(0, 1)]
		commandRange['range'] = shapes.push(shapes.single(), offset)

		# Space beyond target
		commandRange['specialSpaces'] = [[0,1]]

		generic.range.rigid(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(26, 8, 4)
	
	def description():
		return ('Move quickly through the world, sure of where you\'re headed. In the light, all things become clear.\n\n'
				'Move past any unit X + 1 spaces away\n'
				'50% Damage\n'
				'200% Accuracy\n'
				'+1 Act')
	
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
				'Summon a bird up to 3 spaces away')
	
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
		return ('It\'s scary when the air itself turns violent.\n\n'
				'Push a unit beside you back X + 1 spaces\n'
				'80% Damage')
	
	def name():
		return 'Aero Impact'
	
	def icon():
		return 'S_Physic_02.png'

	def tags():
		return ['targets', 'extends']

'Earth'
class mudshot:
	def perform(actor, *targets):
		for target in targets:
			factors = generic.commandFactors.magic(actor, target)
			
			factors['force'] *= 0.8
			factors['accuracy'] *= 1.2

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
		return ('Earth and water forms the mud. A delicate balance of fluidity and stability.\n\n'
				'Hit all units up to X + 1 spaces in front of you in one direction\n'
				'80% Damage\n'
				'120% Accuracy\n'
				'-X mv')
	
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
				'Summon a tough stone on each side of you')
	
	def name():
		return 'Stone Garden'
	
	def icon():
		return 'S_Earth_04.png'

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
		return ('Cast shards upon the world, they will find their mark and make it too.\n\n'
				'Basic magic attack with range X + 1')
	
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
		return ('Force the world to form precisely. But be warned, a world forced to form will inevitably shatter.\n\n'
				'Summon a frigid ice crystal up to X + 1 spaces from you')
	
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
		return ('To conquer any foe, show them a world both cold and confining and they will forfeit.\n\n'
				'Hit a unit up to X + 1 spaces away\n'
				'-1 Mv permanently')
	
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
class blessedWave:
	def perform(actor, *targets):
		multiplier = generic.extentInfluence.polynomial(1, 1/2)

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
					amount = 200 * multiplier
					generic.command.raiseStat(target, 'hp', amount)


	def determineRange():
		commandRange = generic.rangeFactors.standard()

		reach = generic.extentInfluence.polynomial(0, 1)
		commandRange['aoe'] = shapes.diamond(reach)

		generic.range.free(commandRange)
	
	def cost():
		return generic.extentInfluence.polynomial(10, 83, 20, 9)
	
	def description():
		return ('Gush water both soothing to the righteous and agonizing to the wicked.\n\n'
				'Hit all units up to X spaces away, including yourself\n'
				'Damage enemies and heal allies\n'
				'Heal each ally by 200 + 100X\n'
				'+50X% Damage\n'
				'+50X% Accuracy')
	
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
		return ('Ascend the ivory tower with no purpose and you will find it empty.\n\n'
				'Regenrate sp')
	
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
		return ('Concentrate on moving. If you can run, you can survive.\n\n'
				'+2 Mv')
	
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
		return ('Reject weakness and grow strong.\n\n'
				'+10 Strength')
	
	def name():
		return 'Strengthen'
	
	def icon():
		return 'S_Buff_01.png'

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
				'+10 Focus')
	
	def name():
		return 'Focus'
	
	def icon():
		return 'S_Buff_06.png'

	def tags():
		return ['targets']

'Other'
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
		return ('Treat the wounded.\n\n'
				'Heal up to 3 units in line in front of you\n'
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
		return ('Sharpen your blade against the weapon of a unit beside you.\n\n'
				'+8 Strength for both units')
	
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
		return ('To be powerful, to be great, you must suffer.\n\n'
				'Pay 1/6th of your hp\n'
				'Regenerate you sp\n'
				'+20 Strength\n'
				'+20 Intelligence')
	
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
		return ('Place a unit of your choice onto the field to fight for you.')
	
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

