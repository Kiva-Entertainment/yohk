# Setup the graphical aspects of the basicInfo scene
from bge import logic

from script import dynamicMaterial, objectControl, alignControl

TEXT_OBJECT_NAME = 'basicInfo_text'
FACE_OBJECT_NAME = 'basicInfo_face'
ICON_OBJECT_NAME = 'basicInfo_icon'
BACKDROP_OBJECT_NAME = 'basicInfo_backdrop'

def attempt(cont):
	if cont.sensors['start'].positive:
		do()

def do():
	unit = logic.globalDict['actor']
	
	statsText(unit)
	faceImage(unit)
	alignmentIcon(unit)
	backdropColor(unit)


# Display the correct text about the selected unit
def statsText(unit):
	# <unitName>
	# <alignment>
	# hp: <hp>/<health>
	# sp: <sp>/<spirit>
	text = unit['name'] + '\n'
	text += alignControl.name(unit['align']) + '\n\n'
	text += 'hp: ' + str(unit['hp']) + '/' + str(unit['health']) + '\n'
	text += 'sp: ' + str(unit['sp']) + '/' + str(unit['spirit'])
	
	obj = objectControl.getFromScene(TEXT_OBJECT_NAME, 'basicInfo')
	obj['Text'] = text

# Display the face for the selected unit based on its model type
def faceImage(unit):
	face = unit['model']
	
	path = logic.expandPath('//images/Faces/' + face + '.png')
	
	dynamicMaterial.switchMaterialsImage(path, FACE_OBJECT_NAME)

# Display the icon for the selected unit's alignment
def alignmentIcon(unit):
	filename = alignControl.icon(unit['align'])

	path = logic.expandPath('//images/icons/' + filename)
	
	dynamicMaterial.switchMaterialsImage(path, ICON_OBJECT_NAME)

# Change the color of the backdrop to match unit's alignment
def backdropColor(unit):
	color = alignControl.color(unit['align'])

	obj = objectControl.getFromScene(BACKDROP_OBJECT_NAME, 'basicInfo')
	obj.color = color

