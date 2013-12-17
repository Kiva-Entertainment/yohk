# Controls all audio that plays during game
from bge import logic
import aud

device = aud.device()

# Play a sound with given name once
# Sound wav file must exist in audio
def play(soundName):
	filepath = logic.expandPath('//audio/') + soundName + '.wav'

	sound = aud.Factory(filepath)

	device.play(sound)
