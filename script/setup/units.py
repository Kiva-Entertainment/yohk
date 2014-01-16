# Create all units that start on the field
# Store in list all units that don't start on field
from bge import logic
import json

from script import unitControl

STAGE_DATA_FILENAME = 'stageData.json'
# TODO(kgeffen) Remove once better idea align has been hashed out further
ALIGNS = {'1' : 'solarServants',
		'2' : 'martialLegion'}

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
	for i in ['1', '2']:
		filepath = logic.expandPath('//parties/') + logic.globalDict['party' + i] + '.json'
		
		# Load all of stage's data from file
		with open(filepath) as partyData:
			inactiveUnits = json.load(partyData)

			for unit in inactiveUnits:
				unit['align'] = ALIGNS[i]
				logic.globalDict['inactiveUnits'].append(unit)
