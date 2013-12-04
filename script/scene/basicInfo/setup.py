# Setup the graphical aspects of the basicInfo scene
from bge import logic

from script import unitControl, dynamicMaterial, objectControl

TEXT_OBJECT_NAME = 'basicInfo_text'
FACE_OBJECT_NAME = 'basicInfo_face'

def attempt(cont):
	if cont.sensors['start'].positive:
		do()

def do():
	actorData = unitControl.get.actor()['data']
	
	statsText(actorData)
	faceImage(actorData)


# Display the correct text about the selected unit
def statsText(unitData):
	# <unitName>
	# hp: <hp>/<health>
	# sp: <sp>/<spirit>
	text = unitData['name'] + '\n'
	text += 'hp: ' + str(unitData['hp']) + '/' + str(unitData['health']) + '\n'
	text += 'sp: ' + str(unitData['sp']) + '/' + str(unitData['spirit'])
	
	textObject = objectControl.getFromScene(TEXT_OBJECT_NAME, 'basicInfo')
	textObject['Text'] = text

# Display the face for the selected unit based on its model type
def faceImage(data):
	face = data['model']
	
	path = logic.expandPath('//images/Faces/' + face + '.png')
	
	dynamicMaterial.switchMaterialsImage(path, FACE_OBJECT_NAME)
