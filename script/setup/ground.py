# Switch the ground mesh and create all ground variables stored in the globalDict
from bge import logic

from script import objectControl

GROUND_HEIGHT_FILENAME = 'groundHeight.txt'

# Setup the ground mesh and all ground vars
def do():
	filepath = logic.globalDict['stageFilepath']
	
	setupGroundHeight(filepath)
	setupMapDimensions()
	
	switchMapMesh(filepath)

# Setup an array for the height of the ground of each space on the map
# NOTE(kgeffen) At the moment, the groundHeight.txt has all of the data and is evaled
def setupGroundHeight(filepath):
	with open(filepath + GROUND_HEIGHT_FILENAME) as heightFile:
		# TODO(kgeffen) This is easily tamperable, switch to more secure solution
		logic.globalDict['groundHeight'] = eval(heightFile.read())

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
