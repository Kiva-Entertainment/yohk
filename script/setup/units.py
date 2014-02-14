# Create all units that start on the field
# Store in list all units that don't start on field
from bge import logic
import json

from script.unit import unitControl

STAGE_DATA_FILENAME = 'stageData.json'
# TODO(kgeffen) Remove once better idea align has been hashed out further
ALIGNS = ['solarServants', 'martialLegion']

GENERIC_FILEPATH = logic.expandPath('//script/unit/generic/')

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
	# Each team has list of unit data for units on that team
	for teamNum in range(len(data['units'])):

		# Go through all units on team with given teamNum
		for unit in data['units'][teamNum]:

			# Data is in form of dict with
			# starting space, type of generic
			genericType = unit['type']

			unitData = None
			with open(GENERIC_FILEPATH + genericType + '.json') as genericData:
				unitData = json.load(genericData)
				unitData['team'] = teamNum

			unitControl.add(unitData, unit['space'])

def addInactiveUnits():
	for i in [1, 2]:
		filepath = logic.expandPath('//parties/') + logic.globalDict['party' + str(i)] + '.json'
		
		# Load all of stage's data from file
		with open(filepath) as partyData:
			inactiveUnits = json.load(partyData)

			for unitData in inactiveUnits:
				unitData['align'] = ALIGNS[i - 1]
				unitData['team'] = i
				logic.globalDict['inactiveUnits'].append(unitData)
