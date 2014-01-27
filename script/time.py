# Create starting time array
# Called from setup scripts
from bge import logic

# The size of the timeline
SIZE = 10
NUM_TEAMS = 2

def setup():
	logic.globalDict['time'] = Timeline([])

def endTurn(cont):
	if cont.sensors[0].positive:
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

	def endTurn(self):
		self.churn()

		# NOTE(kgeffen) Less hazardous while(true)
		for i in range(SIZE * NUM_TEAMS):
			if self[0][0] == []:
				self.churn()
			else:
				break

	def add(self, unit):
		# Add unit to its teams timeline
		teamsTimeline = self[ unit['team'] - 1 ]
		for turn in teamsTimeline:
			turn.append(unit)

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







