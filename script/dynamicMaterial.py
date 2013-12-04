# The method for switching material's images dynamically
from bge import logic, texture

STARTING_MATERIAL = 'MAdynamic'

# Switch the image that an object's material uses
# to the image at 'path'
def switchMaterialsImage(path, objectName):
	scene = logic.getCurrentScene()
	obj = scene.objects[objectName]
	
	"""Create a new Dynamic Texture"""
	# Get the reference pointer (ID) of the internal texture
	ID = texture.materialID(obj, STARTING_MATERIAL)
	
	# Create a texture object
	objectTexture = texture.Texture(obj, ID)
	
	# Create a new source with an external image	
	newSource = texture.ImageFFmpeg(path)
	
	# The texture has to be stored in a permanent Python object
	# NOTE(kgeffen) logic.texture is instantiated in startup.py
	# NOTE(kgeffen) Each object with a dynamic texture has its
	# own texture stored with key = that object's name
	logic.texture[objectName] = objectTexture
	
	# Update/replace the texture
	logic.texture[objectName].source = newSource
	logic.texture[objectName].refresh(False)
