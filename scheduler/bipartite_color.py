import csv
import numpy as np
import random
import copy

WEEK_LEN = 7
IN_FILE = 'v2_opt.csv'
OUT_FILE = 'v2_sched_opt.csv'
BASE_EVEN_WEEK = [0, 2, 4, 6]
BASE_ODD_WEEK = [1, 3, 5, 6]
EVEN_WEEK = BASE_EVEN_WEEK + BASE_ODD_WEEK
ODD_WEEK = BASE_ODD_WEEK + BASE_EVEN_WEEK


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
				if week % 2 == 0:
					base_week = EVEN_WEEK
				else:
					base_week = ODD_WEEK
				writer.writerow([WEEK_LEN*week + base_week[edge.color], edge.match[1], edge.match[2]])


def choose_color(v1, v2, chosen):
	candidates = []
	for i in range(WEEK_LEN):
		if v1[i] is v2[i] is False:
			candidates.append(i)

	if not candidates:
		raise AssertionError("Too many colors")
	else:
		min = float("inf")
		ind = 0
		for i, val in enumerate(chosen):
			if val < min:
				ind = i
				min = val
		chosen[ind] += 1
		return ind


if __name__ == '__main__':
	main()
