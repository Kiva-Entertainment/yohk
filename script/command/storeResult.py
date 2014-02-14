# Format and store the result of a command
# Either textual (ex: 'miss') or stat change (ex: 'mv +12')
# Called by generic.command.py
from bge import logic

# Store textualized result of command in commandResults dictionary
def storeText(space, text):
	result = {'space' : space, 'text' : text}
	logic.globalDict['commandResults'].append(result)

# Store result of stat change in commandResults dictionary
def statChange(stat, delta, unit):

	# Don't store stat change of 0
	if round(delta) != 0:

		# Space that result should be displayed
		space = unit.position

		# Form the (amount of change) portion of the text
		deltaText = formDeltaText(delta)
		text = stat + ' ' + deltaText
		
		storeText(space, text)

# Form the 'amount changed' portion of the displayed text
# Ex: '+12' portion of display 'Agility +12'
def formDeltaText(delta):
	
	if delta >= 0: # Change is non-negative
		return '+' + str(round(delta))
		
	else: # Change already has its sign (-)
		return str(round(delta))
