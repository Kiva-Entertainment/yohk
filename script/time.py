# Create starting time array
# Called from setup scripts
from bge import logic

from script import upkeep

# The size of the timeline
SIZE = 100
NUM_TEAMS = 2

def setup():
	logic.globalDict['time'] = Timeline([])

def endTurn(cont):
	if cont.sensors[0].positive:
		logic.globalDict['time'].endTurn()

def ensureFirstTurnHasActor():
	# Implementation detail: Calling end turn ensures starting turn has actor
	# Kinda risky to use, but works
	logic.globalDict['time'].endTurn()

class Timeline(list):
	def __init__(self, old):
		# Which team is currently acting
		self.team = 1

		'Setup timeline for each team'
		# Timeline has 1 entry per team
		for i in range(NUM_TEAMS):
			self.append([])

			# Each team's timeline has SIZE turns
			for j in range(SIZE):
				self[i].append([])

	# Churns current turn to end and proceeds to next turn
	def churn(self):
		# Cycle through list of timelines (One for each team)
		teamTimeline = self.pop(0)
		self.append(teamTimeline)

		# Self is now on next team's timeline
		self.team += 1

		# If self has looped around to teams 1s timeline, churn each team timeline once
		if self.team > NUM_TEAMS:
			self.team = 1

			for timeline in self:
				turn = timeline.pop(0)
				timeline.append(turn)

	# End the current turn and go to the next turn with actors
	def endTurn(self):
		for unit in self[0][0]:
			upkeep.do(unit)

		self.churn()

		# NOTE(kgeffen) Less hazardous while(true)
		for i in range(SIZE * NUM_TEAMS):
			if self[0][0] == []:
				self.churn()
			else:
				break

	# Add the given unit to appropriate timeline
	def add(self, unit):
		# Add unit to its teams timeline
		teamsTimeline = self[ unit['team'] - 1 ]
		for turnNum in range(1, len(teamsTimeline)): # Ignore first turn

			# Speed is how many turns occur per 1 in which unit acts
			speed = unit['speed']
			if speed == 0:
				return
			else:
				if turnNum % speed == 0:
					teamsTimeline[turnNum].append(unit)

	# Remove all instances of the given unit in all timelines
	def remove(self, unit):
		for teamNum in range(len(self)):
			for turnNum in range(len(self[teamNum])):
				# Filter specified turn to exclude given unit
				turn = self[teamNum][turnNum]
				turn = list(filter((unit).__ne__, turn))
				self[teamNum][turnNum] = turn

	# Return string describing the current timeline
	def asString(self):
		result = ''

		for turnNum in range(SIZE):
			for teamTimeline in self:

				# If turn has actors for given team, add it with trailing newline
				if teamTimeline[turnNum] != []:
					for unit in teamTimeline[turnNum]:
						result += unit['name'] + '\n'
					result += '\n'

		return result

