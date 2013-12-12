# Basic command building-blocks
# Simple commands need no code beyond calling these methods
# All methods in this module callable

# NOTE(kgeffen) Only the basic results of commands + hitCheck store results,
# basic commands are composed of results of commands
# Ex: standardAttack causes hp stat to raise by -(amount)

# Called by commands.py
from bge import logic
import math
import random

from script import unitControl
from script.command import storeResult

# How random calculations are
RANDOMNESS = 0.1

'Basic commands'
def standardAttack(target, factors):
	force = 2 * random.gauss(factors['force'], factors['force'] * RANDOMNESS)
	resist = random.gauss(factors['resist'], factors['resist'] * RANDOMNESS)
	
	damage = force - resist
	if damage < 1:
		damage = 1
	
	raiseStat(target, 'hp', -damage)
	
	return damage

def regen(unit):
	dSp = unit['regen']/100 * unit['spirit']
	dSp = round(dSp)

	raiseStat(unit, 'sp', dSp)

'Basic results of commands'
# Raise one of unit's stats by an amount
def raiseStat(unit, stat, amount):
	unit[stat] += round(amount)
	
	storeResult.statChange(stat, amount, unit)

# Multiply a stat by an amount
def scaleStat(unit, stat, factor):
	v1 = unit[stat]
	v2 = round(v1 * factor)
	
	unit[stat] = v2
	
	# Calculate and store the change in the affected stat
	amount = v2 - v1
	storeResult.statChange(stat, amount, unit)

	return amount

'Movement'
def move(unit):
	# First special space
	position = logic.globalDict['commandSpecialSpaces'][0]
	
	unitControl.move.toSpace(unit, position)
	
	

'Checks'
# Determine if command hits
# If command misses, store 'miss' in commandResults
def hitCheck(target, factors):
	accuracy = random.gauss(factors['accuracy'], factors['accuracy'] * RANDOMNESS)
	
	evasion = random.gauss(factors['evasion'], factors['evasion'] * RANDOMNESS)
	evasion /= 3
	
	# Succeed w chance a/(a+e)
	rand = random.uniform(0, accuracy + evasion)
	hit = rand <= accuracy
	
	# Store result 'miss'
	if not hit:
		space = target['position']
		storeResult.storeText(space, 'miss')
	
	return hit

# Return true 50% of the time
def coinFlip():
	return random.random() < 0.5


'Other'
# Create the given objects
# Objects are added based on special spaces, in order
def addObjects(*units):
	for i in range(0, len(units)):
		unit = units[i]

		# Change its position before adding
		unit['position'] = logic.globalDict['commandSpecialSpaces'][i]

		# Add game object
		unitControl.object.add(unit)

		# Remove unit from inactive units list, if it's in there
		inactiveUnits = logic.globalDict['inactiveUnits']
		for i in range(0, len(inactiveUnits)):
			if unit == inactiveUnits[i]:
				del inactiveUnits[i]
				break

		storeResult.storeText(unit['position'], 'Poof!')

