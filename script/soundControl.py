# Controls all audio that plays during game
from bge import logic
import aud

# TODO(kgeffen) When sounds are loaded, the files sometimes aren't handled correctly
# Specifically, the error is "AUD_FileFactory: File couldn't be read"
# I'm assuming that the file isn't closed properly, and I am unable to use
# with statemenets because Factory doesn't have an __exit__ method.
# Hopefully this new solution works because it only loads each sound once
# However, the bug rarely emerges, so it's not clear if it's solved
# When it happens, all dynamically loaded images stop working

if 'device' not in dir(logic):
	logic.soundDevice = aud.device()
if 'storedSounds' not in dir(logic):
	logic.storedSounds = {}

# Play a sound with given name once
# Sound wav file must exist in audio
def play(soundName):
	# Determine if a factory for sound already exists
	soundAlreadyStored = soundName in logic.storedSounds

	if not soundAlreadyStored:
		storeSound(soundName)

	logic.soundDevice.play(logic.storedSounds[soundName])

# Store in storedSounds a pairing of the sound's name and its aud.Factory
def storeSound(soundName):
	# Make an aud.factory for sound
	filepath = logic.expandPath('//audio/') + soundName + '.wav'
	soundFactory = aud.Factory.file(filepath)

	logic.storedSounds[soundName] = soundFactory
