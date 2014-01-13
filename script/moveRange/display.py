# Display all spaces that selected unit can move to
from bge import logic

from script import marker

def do():
	for move in logic.globalDict['validMove']:
		space = move['space']
		marker.add(space, 'markerMove')
