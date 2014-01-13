# Contains all of the data for the various alignments

# Dynamically called by alignControl.py
# NOTE(kgeffen) Class names start with lowercase for ease of use

# TODO(kgeffen) Change 'color' to 'banner' and have each alignment have own banner image

class neutral:
	def name():
		return 'Neutral'
	
	def icon():
		return 'I_Rock_01.png'

	def color():
		return 1, 1, 1, 0.5

class martialLegion:
	def name():
		return 'Martial Legion'

	def icon():
		return 'E_Medal_01.png'

	def color():
		return 0.7, 0.7, 1, 0.5

class solarServants:
	def name():
		return 'Solar Servants'

	def icon():
		return 'E_Necklace_03.png'

	def color():
		return 1, 1, 0.4, 0.5

