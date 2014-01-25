# Contains all effects that happen in game
# An effect is like a command, but has no source
# For example, the poison damage that a poisoned unit experiences each turn
from bge import logic
import sys

from script.command import generic, cleanup

# Perform the given effecy on the given target
def perform(effect, target):
	# Get dynamically the method specified by _effect_ and call it
	effectMethod = getattr(sys.modules[__name__], effect)
	effectMethod(target)

	# Do any necessary post-effect cleanup
	cleanup.fromEffectResolving()

'''Effects'''

def poisonDamage(unit):
	dHp = -round(unit['health'] / 10)
	generic.command.raiseStat(unit, 'hp', dHp)
