# Controls all audio that plays during game
from bge import logic
import aud

device = aud.device()
storedSounds = {}

# Play a sound with given name once
# Sound wav file must exist in audio
def play(soundName):
	# Determine if a factory for sound already exists
	soundAlreadyStored = soundName in storedSounds

	if not soundAlreadyStored:
		storeSound(soundName)

	device.play(storedSounds[soundName])

# Store in storedSounds a pairing of the sound's name and its aud.Factory
def storeSound(soundName):
	# Make an aud.factory for sound
	filepath = logic.expandPath('//audio/') + soundName + '.wav'
	soundFactory = aud.Factory(filepath)

	storedSounds[soundName] = soundFactory
