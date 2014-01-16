# Create all units that start on the field
# Store in list all units that don't start on field
from bge import logic
import json
import copy

from script import unitControl

STAGE_DATA_FILENAME = 'stageData.json'

def do():
	addActiveUnits()
	addInactiveUnits()

def addActiveUnits():
	filepath = logic.expandPath('//stages/') + logic.globalDict['stage'] + '/' + STAGE_DATA_FILENAME
	
	# Load all of stage's data from file
	data = None
	with open(filepath) as stageDataFile:
		data = json.load(stageDataFile)

	# Add active units to field
	for unit in data['activeUnits']:
		unitControl.object.add(unit)

def addInactiveUnits():
	filepath = logic.expandPath('//parties/') + logic.globalDict['party'] + '.json'
	
	# Load all of stage's data from file
	with open(filepath) as partyData:
		inactiveUnits = json.load(partyData)

		# TODO(kgeffen) Remove once each side has own units
		for team in ['solarServants', 'martialLegion']: 
			for unit in inactiveUnits:
				unit['align'] = team
				logic.globalDict['inactiveUnits'].append(copy.deepcopy(unit))
