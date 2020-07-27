from ortools.linear_solver import pywraplp
import numpy as np
import json
import sys

EXT_SOLVER = pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING
solver = pywraplp.Solver('Schedule', EXT_SOLVER)
solver.EnableOutput()
solver.SetNumThreads(1)

TEAMS = 30
CONF_1 = (0, TEAMS // 2)
CONF_2 = (TEAMS // 2, TEAMS)
# DIVS = [()]
NUM_IN_DIVISION = 5
NUM_IN_CONFERENCE = 15
ADJ_NUM = NUM_IN_CONFERENCE - NUM_IN_DIVISION


def team_to_division(team):
	return team // NUM_IN_DIVISION


def team_to_conference(team):
	return team // NUM_IN_CONFERENCE


# Matrix for encoding which teams play each other 3 times
# todo ask Ross if better to encode as TEAMS x (CONF - DIV) --- hard to enforce symmetry
# adj_matrix = np.array([[None for j in range(ADJ_NUM)] for i in range(TEAMS)])
# for t1 in range(TEAMS):
# 	for t2 in range(ADJ_NUM):
# 		adj_matrix[t1][t2] = solver.BoolVar(f'A[{t1}][{t2}]')

def preprocess():
	adj_matrix = np.array([[None for j in range(TEAMS)] for i in range(TEAMS)])
	for t1 in range(TEAMS):
		for t2 in range(TEAMS):
			adj_matrix[t1][t2] = solver.BoolVar(f'A[{t1}][{t2}]')

	for t in range(TEAMS):
		solver.Add(adj_matrix[t][t] == 0)

	for t1 in range(TEAMS):
		for t2 in range(t1 + 1, TEAMS):
			solver.Add(adj_matrix[t1][t2] == adj_matrix[t2][t1])

	for t in range(TEAMS):
		t_div = team_to_division(t)
		t_conf = team_to_conference(t)
		teams_in_conf = [team for team in range(TEAMS) if
		                 team_to_conference(team) == t_conf and team_to_division(team) != t_div]
		other_teams = [team for team in range(TEAMS) if team not in teams_in_conf]
		solver.Add(sum(adj_matrix[t, teams_in_conf]) == 4)
		# todo is the other side necessary?
		for other_team in other_teams:
			solver.Add(adj_matrix[t][other_team] == 0)

	# If a team only plays three matches, 2 home / 1 away x2 && 1 home / 2 away x2
	# <= bool var, sums to 2
	two_home = np.array([[None for j in range(TEAMS)] for i in range(TEAMS)])
	for t1 in range(TEAMS):
		for t2 in range(TEAMS):
			two_home[t1][t2] = solver.BoolVar(f'H[{t1}][{t2}]')

	for t1 in range(TEAMS):
		for t2 in range(t1 + 1, TEAMS):
			solver.Add(two_home[t1][t2] == two_home[t2][t1])
			solver.Add(two_home[t1][t2] <= adj_matrix[t1][t2])

	for t in range(TEAMS):
		t_div = team_to_division(t)
		t_conf = team_to_conference(t)
		teams_in_conf = [team for team in range(TEAMS) if
		                 team_to_conference(team) == t_conf and team_to_division(team) != t_div]
		solver.Add(sum(two_home[t, teams_in_conf]) == 2)

	print('Number of variables =', solver.NumVariables())
	print('Number of constraints =', solver.NumConstraints())
	status = solver.Solve()

	print('\nAdvanced usage:')
	print('Problem solved in %f milliseconds' % solver.wall_time())
	print('Problem solved in %d iterations' % solver.iterations())
	print('Problem solved in %d branch-and-bound nodes' % solver.nodes())

	if status == pywraplp.Solver.OPTIMAL:
		try:
			with open(sys.argv[1], "w") as f:
				json.dump({
					"adj_matrix": [[x.solution_value() for x in row] for row in adj_matrix],
					"two_home": [[x.solution_value() for x in row] for row in two_home]
				}, f)
		except:
			print("Error writing to file")

		return adj_matrix, two_home
	else:
		print('The problem does not have an optimal solution.')
		return None, None


if __name__ == '__main__':
	preprocess()
