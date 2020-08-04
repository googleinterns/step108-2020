import csv
import numpy as np
import random
import sys
WEEK_LEN = 7
IN_FILE = sys.argv[1]
OUT_FILE = sys.argv[2]
BASE_EVEN_WEEK = [0, 2, 4, 6]
BASE_ODD_WEEK = [1, 3, 5, 6]
EVEN_WEEK = BASE_EVEN_WEEK + BASE_ODD_WEEK
ODD_WEEK = BASE_ODD_WEEK + BASE_EVEN_WEEK
# TODO list of all games, 0 if second half / 1 if first half
# TODO 41 games in each half, 20/21 games

class Edge:
	def __init__(self, match):
		self.match = match
		self.color = 0

	def __repr__(self):
		return f'{{{self.match}: {self.color}}}'


def main():
	with open(IN_FILE, "r") as f:
		reader = csv.reader(f)
		headers = next(reader)
		rows = list(reader)

	matches = np.array(rows).astype(int)
	weeks, teams = np.amax(matches, axis=0)[:2] + 1
	weekly = {}

	for week in range(weeks):
		chosen = [0 for i in range(WEEK_LEN)]
		vertices = {v: [False] * WEEK_LEN for v in range(teams)}
		edges = [Edge(match) for match in matches if match[0] == week]
		random.shuffle(edges)
		for edge in edges:
			v1 = vertices[edge.match[1]]
			v2 = vertices[edge.match[2]]
			color = choose_color(v1, v2, chosen)
			edge.color = color
			v1[color] = v2[color] = True
		weekly[week] = edges
		print(chosen)

	weekly = {week: sorted(weekly[week], key=lambda x: x.color) for week in weekly}
	with open(OUT_FILE, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(['day', 'team1', 'team2'])
		for week in weekly:
			week_arr = weekly[week]
			for edge in week_arr:
				# # Messes up the sorted property of days
				# if week % 2 == 0:
				# 	base_week = EVEN_WEEK
				# else:
				# 	base_week = ODD_WEEK
				# writer.writerow([WEEK_LEN*week + base_week[edge.color], edge.match[1], edge.match[2]])
				writer.writerow([WEEK_LEN * week + edge.color, edge.match[1], edge.match[2]])


def choose_color(v1, v2, chosen):
	candidates = []
	for i in range(WEEK_LEN):
		if v1[i] is v2[i] is False:
			candidates.append(i)

	if not candidates:
		raise AssertionError("Too many colors")
	else:
		return random.choice(candidates)
		# min = float("inf")
		# idx = 0
		# for val in candidates:
		# 	if val < min:
		# 		idx = val
		# 		min = val
		# chosen[idx] += 1
		# return idx


if __name__ == '__main__':
	main()
