# Controls all audio that plays during game
from bge import logic
import aud

# Play a soundEffect sound once
def play(soundName):
	filepath = logic.expandPath('//audio/soundEffects/') + soundName + '.wav'

	sound = aud.Factory.file(filepath)

	aud.device().play(sound)
