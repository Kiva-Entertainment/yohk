# Display results of commands by moving text object and changing its text
# Methods called by commandResult text object in battlefield
from bge import logic
from math import radians
from mathutils import Matrix, Vector

from script import objectControl, getPosition

# How high above the ground the display is
HEIGHT_ABOVE = 2.0
# Name of the object that display copies the rotation from
OBJECT_NAME_ROTATION_COPY = 'cursorSlow'

# Make commandResult visible and change it to state 3
# Target waits while results are displayed
def display():
	textObj = objectControl.getFromScene('commandResult', 'battlefield')
	textObj.setVisible(True)

# Make commandResult invisible and change it to state 1
# Target done waiting
def endDisplay():
	textObj = objectControl.getFromScene('commandResult', 'battlefield')
	
	# NOTE(kgeffen) Can't use objectControl.hide because object doesn't become deactivated,
	# just waits until messaged (And must be actively awaiting the message)
	textObj.setVisible(False)
	textObj.state = logic.KX_STATE1

# Play any effects that happen on commandResult
# Called every tic while text is visible
def playEffects():
	textObj = objectControl.getFromScene('commandResult', 'battlefield')

	# Raise
	textObj.worldPosition += Vector((0.0, 0.0, 0.01))

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
	textObj = objectControl.getFromScene('commandResult', 'battlefield')

	# Set text
	textObj['Text'] = result['text'].capitalize()
	
	# Set postion
	position = getPosition.onGround(result['space'])
	position[2] += HEIGHT_ABOVE
	
	textObj.worldPosition = position
	
	# Adjust rotation to face camera
	adjustRotation(textObj)

	# The number of characters in the text
	numChars = len(result['text'])

	# Center the text object over the unit it describes
	centerText(textObj, numChars)

# Center the given object based on the number of characters command result contains
def centerText(obj, numChars):
	# NOTE(kgeffen) Each character has length 0.1
	textObjectLength = 0.1 * numChars
	
	# Move object to the left by half of its total length
	adjustment = Vector((-textObjectLength/2, 0.0, 0.0))

	obj.localPosition += adjustment

# Copy the rotation of slowTarget, which is the camera's parent
def adjustRotation(resultDisplay):
	
	# The object whose rotation the display copies
	obj = objectControl.getFromScene(OBJECT_NAME_ROTATION_COPY, 'battlefield')
	orientation = obj.orientation
	
	# Adjustments have to be made to the orientation 
	xAdjust = Matrix.Rotation(radians(90.0), 3, 'X')
	zAdjust = Matrix.Rotation(radians(-45.0), 3, 'Z')
	orientation *= zAdjust * xAdjust # NOTE(kgeffen) Order matters, don't change order
	
	resultDisplay.orientation = orientation
