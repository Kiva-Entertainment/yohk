# Call methods for given commands dynamically
from script.align import align

def name(alignment):
	return callMethodForAlignment(alignment, 'name')
def icon(alignment):
	return callMethodForAlignment(alignment, 'icon')
def color(alignment):
	return callMethodForAlignment(alignment, 'color')

# NOTE(kgeffen) This method is not called by any script besides the above
# NOTE(kgeffen) The data for each command is stored in a standardized class
# Each of those classes has identical methods like 'name', 'icon', etc.
# Call a method (Ex: 'name') for a given alignment
def callMethodForAlignment(alignment, methodName, *arguments):
	# The class with the data for given alignment
	alignClass = getattr(align, alignment)
	
	# The method to call
	method = getattr(alignClass, methodName)
	
	# Call it with the arguments provided
	result = method(*arguments)
	return result
