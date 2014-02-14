# TODO(kgeffen) Describe
from bge import logic, types
import json

from script import sceneControl, getPosition

# The default stats of a unit
DEFAULT_UNIT = None
filepath = logic.expandPath('//script/unit/default.json')
with open(filepath) as dataFile:
	DEFAULT_UNIT = json.load(dataFile)

def test(cont):
	if(cont.sensors[0].positive):
		UNIT = {'team' : 1}
		unit = add(UNIT)

def add(unitData, space):
	battlefield = sceneControl.get('battlefield')

	# Add game object
	obj = battlefield.addObject('unit', 'ground')

	unit = Unit(obj)
	unit.setup(unitData, space)

	logic.globalDict['units'].append(unit)

class Unit(types.KX_GameObject):
	def setup(self, unitData, space):
		''' Setup the unit '''
		self.setupStats(unitData)
		
		# Move unit object to starting location
		# TODO(kgeffen) Should stats in json store as position, or maybe space
		self.move(space)

		self.setModel(self.stats['class'])

		# TODO(kgeffen) Add to timeline
		logic.globalDict['time'].add(self)

	def setupStats(self, unitData):
		''' Set stats of unit to given values or defaults if no values given'''
		# For each stat in default, if present in unitData, assign from that,
		# Else, assign default value
		stats = DEFAULT_UNIT
		for statType in DEFAULT_UNIT.keys():
			
			# Stat of given type is value from unitData if present
			if statType in unitData:
				stats[statType] = unitData[statType]

		self.stats = stats

	def setModel(self, model):
		''' Switch mesh '''
		self.stats['class'] = model

		# Load mesh into memory only if it isn't already loaded
		filepath = logic.expandPath('//models/') + model + '.blend'
		if filepath not in logic.LibList():
			logic.LibLoad(filepath, 'Mesh')
		
		# Switch objects mesh
		self.replaceMesh(model)

	def space(self):
		''' Get the space that unit is in, 2d '''
		x = round(self.position[0])
		y = round(self.position[1])

		return [x,y]

	def die(self):
		''' Self dies '''
		# Delete unit object
		self.endObject()

		# Remove unit from list of units
		# NOTE(kgeffen) Not sure this is necessary
		unitList = logic.globalDict['units']
		unitList = list(filter((self).__ne__, unitList))
		logic.globalDict['units'] = unitList
		
		# Update the time data and display to account for deaths
		logic.globalDict['time'].remove(self)
	
	def move(self, space):
		''' Move self to given space '''
		self.worldPosition = getPosition.onGround(space)
