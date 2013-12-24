# Switch the ground mesh and create all ground variables stored in the globalDict
from bge import logic
import json

from script import objectControl

STAGE_DATA_FILENAME = 'stageData.json'
# TODO(kgeffen) Remove once stage selection has been enabled
TEMP_STAGE_NAME = 'mars'

# Setup the ground mesh and all ground vars
def do():
	# TODO(kgeffen) Remove once stage selection has been enabled
	filepath = logic.expandPath('//stages/') + TEMP_STAGE_NAME + '/'
	
	setupGroundHeight(filepath)
	setupMapDimensions()
	
	switchMapMesh(filepath)

def setupGroundHeight(filepath):
	with open(filepath + STAGE_DATA_FILENAME) as stageDataFile:
		logic.globalDict['groundHeight'] = json.load(stageDataFile)['ground']

# Store the x and y of the current map based on the pre-existing groundHeight array
def setupMapDimensions():
	groundHeight = logic.globalDict['groundHeight']
	
	logic.globalDict['xLength'] = len(groundHeight)
	logic.globalDict['yLength'] = len(groundHeight[0])

# Switch the mesh for the map with the one located in the blend in the stage dir
# NOTE(kgeffen) Does not check if library already loaded, this may causes issues in the future
def switchMapMesh(filepath):
	# Load the mesh into bge memory
	logic.LibLoad(filepath + 'ground.blend', 'Mesh')
	
	ground = objectControl.getFromScene('ground', 'battlefield')
	
	# Replace the mesh with the ground mesh loaded from the blend file in the stage dir
	ground.replaceMesh('ground')
