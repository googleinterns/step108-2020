import csv
import numpy as np
import random
import sys
WEEK_LEN = 7
IN_FILE = sys.argv[1]
OUT_FILE = sys.argv[2]

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
	weekly = [None for i in range(weeks)]

	for week in range(weeks):
		vertices = {v: [False] * WEEK_LEN for v in range(teams)}
		edges = [Edge(match) for match in matches if match[0] == week]
		random.shuffle(edges)
		for edge in edges:
			v1 = vertices[edge.match[1]]
			v2 = vertices[edge.match[2]]
			color = choose_color(v1, v2)
			edge.color = color
			v1[color] = v2[color] = True
		weekly[week] = edges

	for week_edges in weekly:
		week_edges.sort(key=lambda x: x.color)
	with open(OUT_FILE, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(['day', 'team1', 'team2'])
		for week, week_edges in enumerate(weekly):
			for edge in week_edges:
				writer.writerow([WEEK_LEN * week + edge.color, edge.match[1], edge.match[2]])


# Randomly choose a color based on the available ones
def choose_color(v1, v2):
	candidates = []
	for i in range(WEEK_LEN):
		if v1[i] is v2[i] is False:
			candidates.append(i)
	# Algorithm should never fail (proof in README.md)
	if not candidates:
		raise AssertionError("Too many colors")
	else:
		return random.choice(candidates)

if __name__ == '__main__':
	main()
