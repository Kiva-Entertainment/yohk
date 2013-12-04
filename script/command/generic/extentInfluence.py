# Common influences of extent on force/range
# Called by commands.py
from bge import logic
import math

def polynomial(*coefficients):
	extent = logic.globalDict['extent']

	# The result of the polynomial
	result = 0
	# Add each term - Term is coefficient for that term times
	# appropriate power of extent
	for power in range(0, len(coefficients)):
		
		# The coefficient for this term
		c = coefficients[power]

		result += c * (extent ** power)

	return result

# NOTE(kgeffen) Extent of 1 yields quantity
def logarithmic(quantity):
	# The log bas, still in testing
	BASE = 50
	
	extent = logic.globalDict['extent']
	
	# NOTE(kgeffen) Add 1 so that (extent = 1) yields 1, not 0
	coefficient = math.log(extent, BASE) + 1
	
	# Scale by the log of the extent
	quantity *= coefficient
	
	quantity = int(quantity)
	
	return quantity
