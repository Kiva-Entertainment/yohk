# Add all necessary scenes
# After background scenes have been added, hideBackground is called and they are hidden
from bge import logic

from script import sceneControl

BACKGROUND_SCENES = ['basicInfo', 'commandSelect', 'info']
OVERLAY_SCENES = ['battlefieldOverlay', 'sound']

# Add all necessary scenes, even ones that are hidden
# NOTE(kgeffen) Background scenes must be hidden only after they exist
# They are hidden during next tic
def primary():
	for scene in BACKGROUND_SCENES + OVERLAY_SCENES:
		logic.addScene(scene, 1)

# This method is called on next tic after above method
# It hides all scenes that should start hidden
def secondary():
	sceneControl.hide(*BACKGROUND_SCENES)
