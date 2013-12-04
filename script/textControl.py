# Operations done to text

# Wrap the given text at the given character limit so that no line of text is longer
# than the limit
def wrap(text, characterLimit):
	wrappedText = ''
	for line in text.split('\n'):

		# Form fragments from line split at spaces
		fragments = line.split(' ')
		for fragment in fragments:
			
			# The last line of the string being formed
			lastLine = wrappedText.split('\n')[-1]
			fragmentFits = ( len(lastLine) + len(fragment) <= characterLimit )
			
			if fragmentFits:
				wrappedText += fragment + ' '
			else:
				# Fragment does not fit on line, put on new line
				wrappedText += '\n' + fragment + ' '
		
		# Preserve line seperation
		wrappedText += '\n'

	return wrappedText
