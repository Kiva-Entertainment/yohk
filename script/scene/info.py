# Contains all methods used in the 'Info' scene
from bge import logic
from math import pi
import dynamicMaterial
import utility
from script import sceneControl

MAX_LIST_NUMBER = 4 - 1

# Stats displayed in lists on screen 2-4
LIST_STATS = ['commands', 'equipment', 'attributes']
# Stats displayed on first screen
FIRST_SCREEN_STATS = [['name', 'type', 'model', 'essence'], \
			 ['health', 'spirit', 'move', 'actions', 'speed', 'regen'], \
			['strength', 'toughness', 'intelligence', 'willpower', 'focus', 'agility']]
# The stats that should be displayed as x/y
RATIO_STATS = {'health' : 'hp',\
			'spirit' : 'sp',\
			'move' : 'mv',\
			'actions' : 'act'}

FACE_OBJECT_NAME = 'info_face'
TEXT_NAME_BASE = 'info_text'
ICON_NAME_BASE = 'info_icon'

# Cycle through the entries in the list currently viewed
def cycle(cont):
	screenNumber = cont.owner['currentScreen']
	if screenNumber != 0: # First screen doesn't change
		
		# List of stats displayed on current screen ex: [smack, defend, slash]
		statList = logic.globalDict['infoLists'][screenNumber - 1]
		if len(statList) != 0:
			
			upKey = cont.sensors['upKey'].positive
			downKey = cont.sensors['downKey'].positive
			
			if upKey:
				entry = statList.pop()
				statList.insert(0, entry)
			elif downKey:
				entry = statList.pop(0)
				statList.append(entry)
			else:
				# Setup doesn't need to happen if no cycling happened
				# This else: return could be removed, but optimization...
				return
			
			Setup.setupStandardScreenObjects(screenNumber)

# Rotate the camera and record which screen is being viewed
def rotate(cont):
	own = cont.owner
	leftKey = cont.sensors['leftKey'].positive
	rightKey = cont.sensors['rightKey'].positive
	currentScreen = own['currentScreen']
	
	if leftKey:
		own.applyRotation([0.0, 0.0, pi/2])
		
		if currentScreen == 0:
			currentScreen = MAX_LIST_NUMBER
		else:
			currentScreen -= 1
	elif rightKey:
		own.applyRotation([0.0, 0.0, -pi/2])
		
		if currentScreen == MAX_LIST_NUMBER:
			currentScreen = 0
		else:
			currentScreen += 1
	
	own['currentScreen'] = currentScreen

def setup(cont):
	if cont.sensors['setup'].positive:
		Setup.do()

class Setup:
	def do():
		unitNumber = logic.globalDict['selected']
		unitData = logic.globalDict['units'][unitNumber]
		
		for i in range(0, 4):
			Setup.setupScreen(unitData, i)
	
	# Setup all information and stored info about a given screen
	# If first screen, call unique method to handle it
	def setupScreen(unitData, screenNumber):
		# NOTE(kgeffen) First screen has a unique layout
		if screenNumber == 0:
			Setup.setupFirstScreen(unitData)
			return
		
		statType = LIST_STATS[screenNumber - 1]
		statList = unitData[statType]
		
		if not len(statList) == 0:
			Setup.makeFlatInfoListCopy(statList, screenNumber)
			Setup.setupStandardScreenObjects(screenNumber)
	
	# First screen has a unique layout
	def setupFirstScreen(unitData):
		scene = logic.getCurrentScene()
		
		Setup.setupFace(unitData)
		
		# Setup each text object on screen 1
		QUANTITY_TEXT_OBJECTS = 3
		for i in range(0, QUANTITY_TEXT_OBJECTS):
			text = Setup.statsInLines(unitData, FIRST_SCREEN_STATS[i])
			
			objectName = TEXT_NAME_BASE + '0_' + str(i)
			obj = scene.objects[objectName]
			obj['Text'] = text
	
	
	"""Used for screens 2-4"""
	# Setup the icon/action/description objects for given screen
	# NOTE(kgeffen) Only called for screens 2-4, not 1 (1 has unique layout)
	def setupStandardScreenObjects(screenNumber):
		Setup.setupList(screenNumber)
		Setup.setupIcon(screenNumber)
		Setup.setupDescription(screenNumber)
	
	# Change the text list for the given screen
	def setupList(screenNumber):
		scene = logic.getCurrentScene()
		
		statList = logic.globalDict['infoLists'][screenNumber - 1]
		
		listText = ''
		for stat in statList:
			listText += stat + '\n'
		
		listObjectName = TEXT_NAME_BASE + str(screenNumber)
		scene.objects[listObjectName]['Text'] = listText
	
	# Changes the icon for given screen
	def setupIcon(screenNumber):
		objectName = ICON_NAME_BASE + str(screenNumber)
		
		# Value of stat/its type (ex: shortSword, equipment)
		statValue = logic.globalDict['infoLists'][screenNumber - 1][0]
		statType = LIST_STATS[screenNumber - 1]
		
		# Check the text folder to get the icon used for the entry
		filename = utility.getFieldFromTxt(statType, statValue, 'icon')
		path = logic.expandPath('//images/icons/' + filename)
		
		dynamicMaterial.switchMaterialsImage(path, objectName)
	
	# Change the description text on screen to display
	# description of top entry in stat list
	def setupDescription(screenNumber):
		scene = logic.getCurrentScene()
		
		statType = LIST_STATS[screenNumber - 1] # Ex: Equipment
		
		statList = logic.globalDict['infoLists'][screenNumber - 1]
		describedEntry = statList[0] # Ex: shortSword
		
		# Get the description from the txt file
		text = utility.getFieldFromTxt(statType, describedEntry, 'description')
		text = utility.wrapText(text, 30)
		
		# Change the text object's text
		listObjectName = TEXT_NAME_BASE + str(screenNumber) + '_description'
		scene.objects[listObjectName]['Text'] = text
	
	# Make a list of all entries in the given statList
	# Flat list used exclusively in Info for working with list
	def makeFlatInfoListCopy(statList, screenNumber):
		flatList = []
		for entry in statList:
			# NOTE(kgeffen) Currently, only commands are arrays within arrays
			# To accomodate format changes, test all lists in this fashion
			if type(entry) == list:
				for subEntry in entry:
					flatList.append(subEntry)
			else:
				flatList.append(entry)
		
		logic.globalDict['infoLists'][screenNumber - 1] = flatList
	
	
	"""Used exclusively for first screen"""
	# Display the correct face based on the unit's model type (Ex: Sumo)
	def setupFace(unitData):
		face = unitData['model']
		path = logic.expandPath('//images/faces/' + face + '.png')
		dynamicMaterial.switchMaterialsImage(path, FACE_OBJECT_NAME)
	
	# Return the desired stats in order
	# Deals with special cases (hp/health, etc.)
	def statsInLines(unitData, stats):
		text = ''
		
		for stat in stats:
			# Add stat as line, or as ratio if is a stat which is
			# displayed as a ratio (Ex: Hp/health)
			if not stat in RATIO_STATS:
				text += str(unitData[stat]) + '\n'
			else:
				numeratorStat = RATIO_STATS[stat]
				numerator = str(unitData[numeratorStat])
				
				denominator = str(unitData[stat])
				
				text += numerator + '/' + denominator + '\n'
				
		return text
	

# Exit the Info scene
def exit(cont):
	if cont.sensors['wKey'].positive:
		sceneControl.resume('battlefield')
		sceneControl.show('battlefieldOverlay')
		sceneControl.hide('info')

