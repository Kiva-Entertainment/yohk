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

from script import objectControl, getPosition
from script.command import storeResult

# How random calculations are
RANDOMNESS = 0.1

'Basic commands'
def standardAttack(targetNumber, factors):
	force = 2 * random.gauss(factors['force'], factors['force'] * RANDOMNESS)
	resist = random.gauss(factors['resist'], factors['resist'] * RANDOMNESS)
	
	damage = force - resist
	if damage < 1:
		damage = 1
	
	raiseStat(targetNumber, 'hp', -damage)
	
	return damage

'Basic results of commands'
# Raise one of unit's stats by an amount
def raiseStat(unitNumber, stat, amount):
	logic.globalDict['units'][unitNumber][stat] += round(amount)
	
	storeResult.statChange(stat, amount, unitNumber)

# Multiply a stat by an amount
def scaleStat(unitNumber, stat, factor):
	v1 = logic.globalDict['units'][unitNumber][stat]
	v2 = round(v1 * factor)
	
	logic.globalDict['units'][unitNumber][stat] = v2
	
	# Calculate and store the change in the affected stat
	amount = v2 - v1
	storeResult.statChange(stat, amount, unitNumber)

'Movement'
def move(unitNumber):
	# First special space
	position = logic.globalDict['commandSpecialSpaces'][0]
	
	logic.globalDict['units'][unitNumber]['position'] = position
	
	# Move actual object
	obj = objectControl.getFromScene(str(unitNumber), 'battlefield')
	obj.worldPosition = getPosition.onGround(position)

'Other'
# Determine if command hits
# If command misses, store 'miss' in commandResults
def hitCheck(targetNumber, factors):
	accuracy = random.gauss(factors['accuracy'], factors['accuracy'] * RANDOMNESS)
	
	evasion = random.gauss(factors['evasion'], factors['evasion'] * RANDOMNESS)
	evasion /= 3
	
	# Succeed w chance a/(a+e)
	rand = random.uniform(0, accuracy + evasion)
	hit = rand <= accuracy
	
	# Store result 'miss'
	if not hit:
		space = logic.globalDict['units'][targetNumber]['position']
		storeResult.storeText(space, 'miss')
	
	return hit
