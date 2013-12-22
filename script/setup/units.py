# Create all units that start on the field (Their data stored in gd['units'])
# Store in list all units that don't start on field
from bge import logic
import json

from script import unitControl

STAGE_DATA_FILENAME = 'stageData.json'
# TODO(kgeffen) Remove once stage selection has been enabled
TEMP_STAGE_NAME = 'mars'

def do():
	filepath = logic.expandPath('//stages/') + TEMP_STAGE_NAME + '/' + STAGE_DATA_FILENAME
	
	# Load all of stage's data from file
	data = None
	with open(filepath) as stageDataFile:
		data = json.load(stageDataFile)

	# Add active units to field
	for unit in data['activeUnits']:
		unitControl.object.add(unit)

	# Add inactive units to list
	for unit in data['inactiveUnits']:
		logic.globalDict['inactiveUnits'].append(unit)
