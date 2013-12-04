# Until stage selection is supported, this is how the path to the stage's dir is created
from bge import logic

# TODO(kgeffen) Remove once stage selection has been enabled
TEMP_STAGE_NAME = 'earth'

# TODO(kgeffen) Remove once stage selection has been enabled
def do():
    # get path to data for selected level
    stageRoot = logic.expandPath('//') + 'stages/' + TEMP_STAGE_NAME + '/'
    logic.globalDict['stageFilepath'] = stageRoot
