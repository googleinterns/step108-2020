from __future__ import print_function
import numpy as np
from ortools.linear_solver import pywraplp
import csv
import sys

def f_var(day, team1, team2):
    return f'x{day}_{team1}_{team2}'

NUM_IN_DIVISION = 5
def team_to_division(team):
    return team // NUM_IN_DIVISION

NUM_IN_CONFERENCE = 15
def team_to_conference(team):
    return team // NUM_IN_CONFERENCE

# EXT_SOLVER = pywraplp.Solver.BOP_INTEGER_PROGRAMMING
# EXT_SOLVER = pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
EXT_SOLVER = pywraplp.Solver.SCIP_MIXED_INTEGER_PROGRAMMING
# EXT_SOLVER = pywraplp.Solver.SAT_INTEGER_PROGRAMMING


solver = pywraplp.Solver('NBA Schedule',
                         EXT_SOLVER)
solver.EnableOutput()
solver.SetNumThreads(1)

teams = 30
days = 177
weeks = (days + 6) // 7
week_len = 7

# teams = 7
# days = (teams-2)*7

xs = [[[None for team2 in range(teams)] for team1 in range(teams)] for i in range(days)]
for day in range(days):
    for team1 in range(teams):
        for team2 in range(teams):
            if team1 != team2:
                xs[day][team1][team2] = solver.BoolVar(f_var(day, team1, team2))


print('Number of variables =', solver.NumVariables())

# 4 games a week
for team1 in range(teams):
    for week in range(0, days, week_len):
        week_vars = []
        for day in range(week, min(week + week_len, days)):
            for team2 in range(teams):
                if team1 != team2:
                    week_vars.append(xs[day][team1][team2])
                    week_vars.append(xs[day][team2][team1])
        solver.Add(solver.Sum(week_vars) <= 4)

# 41 home/away games
for team1 in range(teams):
    home_vars = []
    away_vars = []
    for day in range(days):
        for team2 in range(teams):
            if team1 != team2:
                home_vars.append(xs[day][team1][team2])
                away_vars.append(xs[day][team2][team1])
    solver.Add(solver.Sum(home_vars) == 41)
    solver.Add(solver.Sum(away_vars) == 41)

# one game per day
for team1 in range(teams):
    for day in range(days):
        day_vars = []
        for team2 in range(teams):
            if team1 != team2:
                day_vars.append(xs[day][team1][team2])
                day_vars.append(xs[day][team2][team1])
        solver.Add(solver.Sum(day_vars) <= 1)

# division and conference constraints
for team1 in range(teams):
    team1_div = team_to_division(team1)
    team1_conf = team_to_conference(team1)
    teams_in_div = [team for team in range(teams) if team_to_division(team) == team1_div]
    teams_in_conf = [team for team in range(teams) if team_to_conference(team) == team1_conf and team not in teams_in_div]
    teams_other_conf = [team for team in range(teams) if team not in teams_in_div and team not in teams_in_conf]
    div_vars = {t: [] for t in teams_in_div if t != team1}
    conf_vars_home = {t: [] for t in teams_in_conf}
    conf_vars_away = {t: [] for t in teams_in_conf}
    other_conf_vars = {t: [] for t in teams_other_conf}
    for day in range(days):
        for team2 in range(teams):
            if team1 != team2:
                team2_var = xs[day][team1][team2]
                if team2 in teams_in_div:
                    div_vars[team2].append(team2_var)
                elif team2 in teams_in_conf:
                    conf_vars_home[team2].append(team2_var)
                    conf_vars_away[team2].append(xs[day][team2][team1])
                else:
                    other_conf_vars[team2].append(team2_var)
    for t in div_vars:
        # 4 games against same-division teams
        solver.Add(solver.Sum(div_vars[t]) == 2)
    for t in conf_vars_home:
        # 4 games against 6 same-conference teams
        solver.Add(solver.Sum(conf_vars_home[t]) <= 2)
        # 3 games against the remaining same-conference teams
        solver.Add(solver.Sum(conf_vars_home[t]) + solver.Sum(conf_vars_away[t]) >= 3)
    for t in other_conf_vars:
        # 2 games against the other-conference teams
        solver.Add(solver.Sum(other_conf_vars[t]) == 1)


infinity = solver.infinity()
v = solver.Var(0, infinity, False, "v")
ws = [None for team in range(teams)]
zs = [[None for day in range(days)] for team in range(teams)]
ys = [[None for day in range(days)] for team in range(teams)]
for team in range(teams):
    ws[team] = solver.Var(0, infinity, False, f"w_{team}")
    for day in range(days):
        zs[team][day] = solver.Var(0, infinity, False, f"z_{team}_{day}")
        ys[team][day] = solver.BoolVar(f"y_{team}_{day}")

# Encode ys as home bools
# y = 0 when home
for team in range(teams):
    for day in range(days):
        home_vars = [xs[day][team][t] for t in range(teams) if t != team]
        solver.Add(ys[team][day] >= solver.Sum(home_vars))

# y = 1 when away
for team in range(teams):
    for day in range(days):
        away_vars = [xs[day][t][team] for t in range(teams) if t != team]
        solver.Add(ys[team][day] <= 1 - solver.Sum(away_vars))

# Encode travel costs (home <-> away -> +1 cost)
for team in range(teams):
    for day in range(1, days):
        solver.Add(zs[team][day] >= 0)
        solver.Add(zs[team][day] >= ys[team][day] - ys[team][day-1])


# Team cost
for team in range(teams):
    solver.Add(ws[team] == solver.Sum(zs[team]))

# Max team cost
solver.Add(v >= solver.Sum(ws))

print('Number of constraints =', solver.NumConstraints())

solver.Minimize(v)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.Objective().Value())
    print(f'Number of matches: {sum(x.solution_value() for x in np.asarray(xs).flatten() if x is not None)}')

    # Debugging
    # for team in range(teams):
    #     for week in range(0, days, week_len):
    #         s = 0
    #         for day in range(week, week + week_len):
    #                 for team2 in range(teams):
    #                     if xs[day][team][team2]:
    #                         s += xs[day][team][team2].solution_value()
    #         print(f'{team} | {week // 7}: {s}')
    # for x in all_x:
    #     if x is not None and x.solution_value() == 1.0:
    #         print(f'{x} = {x.solution_value()}')
    # for team in range(teams):
    #     for day in range(days):
    #         if ys[team][day].solution_value() != 0:
    #             print(f'{ys[team][day]} = {ys[team][day].solution_value()}')

    # If provided in the command-line, write the schedule to a csv file
    try:
        with open(sys.argv[1], "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["day", "team1", "team2"])
            for day in range(days):
                for team1 in range(teams):
                    for team2 in range(teams):
                        if team1 != team2:
                            if xs[day][team1][team2].solution_value():
                                writer.writerow([day, team1, team2])
    except:
        pass

else:
    print('The problem does not have an optimal solution.')

print('\nAdvanced usage:')
print('Problem solved in %f milliseconds' % solver.wall_time())
print('Problem solved in %d iterations' % solver.iterations())
print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
