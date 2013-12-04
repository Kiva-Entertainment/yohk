# Display results of commands by moving text object and changing its text
# Methods called by commandResult text object in battlefield
from bge import logic

from script import objectControl, getPosition

# How high above the ground the display is
HEIGHT_ABOVE = 2.0
# Name of the object that display copies the rotation from
OBJECT_NAME_ROTATION_COPY = 'cursorSlow'

# Make commandResult visible and change it to state 3
# Target waits while results are displayed
def display():
	obj = objectControl.getFromScene('commandResult', 'battlefield')
	
	obj.setVisible(True)
	obj.state = logic.KX_STATE3
	
	logic.globalDict['cursor'] = 'wait'

# Make commandResult invisible and change it to state 1
# Target done waiting
def endDisplay():
	obj = objectControl.getFromScene('commandResult', 'battlefield')
	
	# NOTE(kgeffen) Can't use objectControl.hide because object doesn't become deactivated,
	# just waits until messaged (And must be actively awaiting the message)
	obj.setVisible(False)
	obj.state = logic.KX_STATE1
	
	# NOTE(kgeffen) To prevent it flickering next time it displays a result
	obj['Text'] = ''
	
	# Cursor was waiting until results were done displaying
	logic.globalDict['cursor'] = 'selecting'

# NOTE(kgeffen) Speed of cycling is controlled by frequency of controller
# Cycle to the next result to be displayed and display it. If none left, end
def cycle():
	results = logic.globalDict['commandResults']
	
	if len(results) == 0:
		# All results have already been displayed
		endDisplay()
	else:
		result = logic.globalDict['commandResults'].pop()
		displayResult(result)

# Display the given result in the correct location
def displayResult(result):
	obj = objectControl.getFromScene('commandResult', 'battlefield')
	
	# Set text
	obj['Text'] = result['text']
	
	# Set postion
	position = getPosition.onGround(result['space'])
	position[2] += HEIGHT_ABOVE
	
	obj.worldPosition = position
	
	# Adjust rotation to face camera
	adjustRotation()

from mathutils import Matrix
from math import radians

# Copy the rotation of slowTarget, which is the camera's parent
def adjustRotation():
	resultDisplay = objectControl.getFromScene('commandResult', 'battlefield')
	
	# The object whose rotation the display copies
	obj = objectControl.getFromScene(OBJECT_NAME_ROTATION_COPY, 'battlefield')
	orientation = obj.orientation
	
	# Adjustments have to be made to the orientation 
	xAdjust = Matrix.Rotation(radians(90.0), 3, 'X')
	zAdjust = Matrix.Rotation(radians(-45.0), 3, 'Z')
	orientation *= zAdjust * xAdjust # NOTE(kgeffen) Order matters, don't change order
	
	resultDisplay.orientation = orientation
