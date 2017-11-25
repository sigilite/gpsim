import random

class Deck:
	def __init__(self, name=None):
		self.name = name

	def __repr__(self):
		return self.name

class Abzan(Deck):
	archetype = ['abzan']  ### Every deck will have an archetype, which is a list of increasing specificity.

	def mod(self, opp): #### returns a tuple (win_modifier, time_modifier). win is out of 100%, time is a multiplier.
		enemy = opp.archetype

		if 'jeskai' in enemy:
			return (6, 1)
		if 'red_deck_wins' in enemy:
			return (3, 0.8)
		if 'abzan' in enemy:
			return (1, 1.1)

class Jeskai(Deck):
	archetype = ['jeskai']

	def mod(self, opp):
		enemy = opp.archetype

		if 'abzan' in enemy:
			return (2, 1)
		if 'red_deck_wins' in enemy:
			return (4, 0.8)
		if 'jeskai' in enemy:
			return (1, 1)

class Red_Deck_Wins(Deck):
	archetype = ['red_deck_wins']

	def mod(self, opp):
		enemy = opp.archetype

		if 'abzan' in enemy:
			return (1, 0.9)
		if 'jeskai' in enemy:
			return (3, 0.9)
		if 'red_deck_wins' in enemy:
			return (1, 0.8)


def battle(x,y): ### Players x and y play a single game. Return (winning_player, time_taken).

	### On a roll of 0-50, x wins. On 50-100, y wins. Modify accordingly.
	roll = random.random() * 100
	threshold = 50 + x.deck.mod(y.deck)[0] + x.skill - y.deck.mod(x.deck)[0] - y.skill
	if roll <= threshold:
		winner = x
	else:
		winner = y
	time = (random.random() * 15) + 5 ### Default time is a random number from 5-20.
	time = time * x.deck.mod(y.deck)[1] * y.deck.mod(x.deck)[1] ### Scale the time by both players' time modifiers.
	return (winner, time)

def match(x,y): ### A match between players x and y. Returns a tuple (winner, game_count) or ('DRAW', game_count).
	if y == 'BYE':
		return (x, [0,0])

	time = 0
	score = [0,0] ### The game_count is a 2-element list, with the winner's score first.
	while True:
		w, t = battle(x,y)
		time += t
		if time > 50:
			if score[0] == score[1]:
				return ('DRAW', score)
			elif score[0] > score[1]:
				return (x, score)
			else:
				score[0], score[1] = score[1], score[0]
				return (y, score)
		if w is x:
			score[0] += 1
			if score[0] == 2:
				return (x, score)
		else:
			score[1] += 1
			if score[1] == 2:
				score[0], score[1] = score[1], score[0]
				return (y, score)


class Player:
	def __init__(self, name, deck, skill=0):
		self.name = name
		self.deck = deck
		self.skill = skill ### A percentage modifier on all battle results.

		self.record = [0,0,0]
		self.points = 0
		self.opponents = [] ### List of who you've already played against. 'BYE' pairings will accumulate here.
		self.game_record = [0,0]

	def __repr__(self):
		return 'Player{0} ({1})'.format(self.name, self.deck)


	def tb1(self): ### Opponents' match win percentage
		a = sum([x.record[0] for x in self.opponents if x != 'BYE'])
		b = sum([x.record[0] + x.record[1] + x.record[2] for x in self.opponents if x != 'BYE'])
		if b == 0:
			return 0
		return a/b

	def tb2(self): ### Player's game win percentage
		if self.game_record == [0,0]:
			return 0
		return self.game_record[0]/(self.game_record[0] + self.game_record[1])

	def tb3(self): ### Opponents' game win percentage
		a = sum([x.game_record[0] for x in self.opponents if x != 'BYE'])
		b = sum([x.game_record[1] for x in self.opponents if x != 'BYE'])
		if a + b == 0:
			return 0
		return a/(a+b)



class Tournament:
	def __init__(self, players):
		self.players = players
		self.round = 0 ### Number of rounds already finished.
		self.standings = players  ### List of players in order of highest points after the latest round.

	def pairings(self):
		new_pairings = []  ### Build up a list of pairings as we go through the list of standings.
		already_paired = []  ### List of players that have gotten paired already.
		for x in self.standings:
			if x in already_paired:
				pass
			else:
				for y in self.standings:
					if (y is not x) and (y not in x.opponents) and (y not in already_paired):
						new_pairings.append((x,y))
						already_paired.append(x)
						already_paired.append(y)
						break 
					else:
						pass

		for x in self.standings:
			if x not in already_paired:
				new_pairings.append((x, 'BYE'))
		return new_pairings  ### Returns a list with pairings as tuples. Some players may be paired with 'BYE'.

	def make_standings(self): ### A method that orders players into current standings, counting tiebreakers.
		self.standings = []
		same_points = []

		n = max([x.points for x in self.players])
		while n >= 0:
			for x in self.players:
				if x.points == n:
					same_points.append(x)

			while same_points:
				highest_ranked = max(same_points, key= lambda x: (x.tb1(), x.tb2(), x.tb3()))
				self.standings.append(highest_ranked)
				same_points.remove(highest_ranked)

			n -= 1
			same_points = []


	def play_round(self):
		pairs = self.pairings()
		for x in pairs:
			x[0].opponents.append(x[1])
			if not x[1] == 'BYE':
				x[1].opponents.append(x[0])

			winner, game_count = match(x[0], x[1])
			if winner == 'DRAW':
				i = 0
				while i < 2:
					x[i].points += 1
					x[i].record[2] += 1
					x[i].game_record[0] += game_count[0]
					x[i].game_record[1] += game_count[0]
					i += 1
			else:
				winner.points += 3
				winner.record[0] += 1
				winner.game_record[0] += game_count[0]
				winner.game_record[1] += game_count[1]

				if winner is x[0]:
					loser = x[1]
				else:
					loser = x[0]
				if loser is not 'BYE':
					loser.record[1] += 1
					loser.game_record[0] += game_count[1]
					loser.game_record[1] += game_count[0]
		self.round +=1
		self.make_standings()


	def day_one(self, rounds=9):
		while self.round < rounds:
			self.play_round()
		

	def cut_to_day_two(self, cutoff=18): ### Turns the list of players into just the ones who made day 2.
		day_two_players = []
		for x in self.players:
			if x.points >= 18:
				day_two_players.append(x)
		self.players = day_two_players
		self.make_standings()

	def day_two(self, rounds=6):
		x = self.round
		while self.round < x+rounds:
			self.play_round()
		

	def top_8_announce(self):
		print('Ladies and gentlemen, after fifteen rounds we have your Top 8!')
		i = 0
		while i < 8:
			print('{0}.'.format(i+1), self.standings[i], self.standings[i].record)
			i += 1




sample_players = [Player(name, Abzan('Abzan')) for name in range(60)]
sample_players.extend([Player(name, Jeskai('Jeskai')) for name in range(60,120)])
sample_players.extend([Player(name, Red_Deck_Wins('Red Deck Wins')) for name in range(120,181)])

gp = Tournament(sample_players)
gp.day_one()
gp.cut_to_day_two()
gp.day_two()
gp.top_8_announce()




			












