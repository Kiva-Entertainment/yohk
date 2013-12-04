# Call methods for given commands dynamically
from script.command import commands

def perform(commandName, actor, targets):
	# NOTE(kgeffen) Commands that only have single target have param "target"
	# which the first/only entry in targets becomes, commands with (possibly)
	# multiple targets have the param "*targets" which recollects the expanded
	# targets from this call
	callMethodForCommand(commandName, 'perform', actor, *targets)
def displayRange(commandName):
	callMethodForCommand(commandName, 'displayRange')
def cost(commandName):
	return callMethodForCommand(commandName, 'cost')
def description(commandName):
	return callMethodForCommand(commandName, 'description')
def name(commandName):
	return callMethodForCommand(commandName, 'name')
def icon(commandName):
	return callMethodForCommand(commandName, 'icon')

# NOTE(kgeffen) This method is not called by any script besides the above
# NOTE(kgeffen) The data for each command is stored in a standardized class
# Each of those classes has identical methods like 'perform' 'displayRange' etc.
# Call a method (ex: perform) for a given command
def callMethodForCommand(commandName, methodName, *arguments):
	# The class that contains the method to perform the given command
	commandClass = getattr(commands, commandName)
	
	# The method which performs the given command
	commandMethod = getattr(commandClass, methodName)
	
	# Call it with the arguments provided
	result = commandMethod(*arguments)
	# NOTE(kgeffen) Method returns results for some values of methodName (Ex: 'cost')
	# but not for all (Ex: 'displayRange')
	return result
