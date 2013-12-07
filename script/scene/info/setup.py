# Setup the Info scene
from bge import logic

from script import sceneControl, dynamicMaterial, objectControl

# Stats displayed on first screen
STATS = [['name', 'model'],
		['health', 'spirit', 'move', 'actions', 'speed', 'regen'],
		['strength', 'toughness', 'intelligence', 'willpower', 'focus', 'agility']]

# The stats that should be displayed as x/y
RATIO_STATS = {'health' : 'hp',
				'spirit' : 'sp',
				'move' : 'mv',
				'actions' : 'act'}

# Name of object that displays unit's face
FACE_OBJECT_NAME = 'info_face'

# Base of name of object that displays stat text for unit
# NOTE(kgeffen) There are multiple, named _name_1, _name_2, etc.
TEXT_OBJECT_NAME_BASE = 'info_text'

def attempt(cont):
	if cont.sensors['setup'].positive:
		do()

def do():
	# The unit whose info is being displayed
	unit = logic.globalDict['described']

	faceImage(unit)
	statText(unit)


# Display the correct face based on the unit's model type (Ex: Soldier)
def faceImage(unit):
	model = unit['model']

	path = logic.expandPath('//images/faces/' + model + '.png')
	
	dynamicMaterial.switchMaterialsImage(path, FACE_OBJECT_NAME)

# Display all of the unit's stat text
def statText(unit):
	# Setup each text object
	# Each list of stats displayed by a different text object
	quantityTextObjects = len(STATS)
	for i in range(0, quantityTextObjects):

		# Get text that object will display
		text = statsInLines(unit, STATS[i])
		
		# Get text object
		objectName = TEXT_OBJECT_NAME_BASE + str(i)
		obj = objectControl.getFromScene(objectName, 'info')
		
		# Set that object's text
		obj['Text'] = text

# Return the desired stats in order
# Deals with special cases (hp/health, etc.)
def statsInLines(unit, stats):
	text = ''
	
	for stat in stats:
		# Add stat as line, or as ratio if is a stat which is
		# displayed as a ratio (Ex: Hp/health)
		if not stat in RATIO_STATS:
			text += str(unit[stat]) + '\n'
		else:
			numeratorStat = RATIO_STATS[stat]
			numerator = str(unit[numeratorStat])
			
			denominator = str(unit[stat])
			
			text += numerator + '/' + denominator + '\n'
			
	return text

