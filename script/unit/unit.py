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
		print(unit.strength)

def add(unitData):
	battlefield = sceneControl.get('battlefield')

	# Add game object
	obj = battlefield.addObject('unit', 'ground')

	unit = Unit(obj)
	unit.setup(unitData)

class Unit(types.KX_GameObject):
	def setup(self, unitData):
		''' Setup the unit '''
		self.setupStats(unitData)
		
		# Move unit object to correct location
		self.worldPosition = getPosition.onGround(self.position)

		self.setModel(self.model)

		# TODO(kgeffen) Add to timeline
		# logic.globalDict['time'].add(self)

	def setupStats(self, unitData):
		''' Set stats of unit to given values or defaults if no values given'''
		# For each stat in default, if present in unitData, assign from that,
		# Else, assign default value 
		for statType in DEFAULT_UNIT.keys():
			
			# Value is default, or gotten from unit data if present
			value = DEFAULT_UNIT[statType];
			if statType in unitData:
				value = unitData[statType]

			self.__setattr__(statType, value)

	def setModel(self, model):
		''' Switch mesh '''
		self.model = model

		# Load mesh into memory only if it isn't already loaded
		filepath = logic.expandPath('//models/') + model + '.blend'
		if filepath not in logic.LibList():
			logic.LibLoad(filepath, 'Mesh')
		
		# Switch objects mesh
		self.replaceMesh(model)
