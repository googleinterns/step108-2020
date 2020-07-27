import numpy as np
from ortools.linear_solver import pywraplp
import csv
import sys

# TODO schedule 3 games separately
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
# solver.SetNumThreads(1)

TEAMS = 30
DAYS = 177
WEEKS = (DAYS + 6) // 7
WEEK_LEN = 7
GAMES_PER_WEEK = 4

# TEAMS = 8
# DAYS = (teams-2)*7
# WEEKS = teams-2


def base_model():
    xs = [[None for team in range(TEAMS)] for week in range(WEEKS)]
    ys = [[[None for team2 in range(TEAMS)] for team1 in range(TEAMS)] for week in range(WEEKS)]
    for week in range(WEEKS):
        for team1 in range(TEAMS):
            xs[week][team1] = solver.BoolVar(f'{week}_{team1}')
            for team2 in range(TEAMS):
                if team1 != team2:
                    ys[week][team1][team2] = solver.BoolVar(f'{week}_{team1}_{team2}')

    # # First formulation
    # for week in range(weeks):
    #     for team1 in range(teams):
    #         home_vars = [ys[week][team1][team2] for team2 in range(teams) if team1 != team2]
    #         away_vars = [ys[week][team2][team1] for team2 in range(teams) if team1 != team2]
    #         solver.Add(sum(home_vars) <= GAMES_PER_WEEK * xs[week][team1])
    #         solver.Add(sum(away_vars) <= GAMES_PER_WEEK * (1 - xs[week][team1]))

    # Bind is_home boolean to games
    for week in range(WEEKS):
        for team1 in range(TEAMS):
            for team2 in range(TEAMS):
                if team1 != team2:
                    solver.Add(ys[week][team1][team2] <= xs[week][team1])
                    solver.Add(ys[week][team2][team1] <= xs[week][team1])
                    # solver.Add(ys[week][team2][team1] <= 1 - xs[week][team1])

    # 4 games per week
    for week in range(WEEKS):
        for team1 in range(TEAMS):
            home_vars = [ys[week][team1][team2] for team2 in range(TEAMS) if team1 != team2]
            away_vars = [ys[week][team2][team1] for team2 in range(TEAMS) if team1 != team2]
            solver.Add(sum(home_vars) + sum(away_vars) <= GAMES_PER_WEEK)

    # 41 home and away games
    for team1 in range(TEAMS):
        home_vars = [ys[week][team1][team2] for team2 in range(TEAMS) for week in range(WEEKS) if team1 != team2]
        away_vars = [ys[week][team2][team1] for team2 in range(TEAMS) for week in range(WEEKS) if team1 != team2]
        solver.Add(solver.Sum(home_vars) == 41)
        solver.Add(solver.Sum(away_vars) == 41)
        # Use this instead if you change the number of teams
        # solver.Add(solver.Sum(home_vars) == teams-2)
        # solver.Add(solver.Sum(away_vars) == teams-2)

    for team1 in range(TEAMS):
        team1_div = team_to_division(team1)
        team1_conf = team_to_conference(team1)
        teams_in_div = [team for team in range(TEAMS) if team_to_division(team) == team1_div]
        teams_in_conf = [team for team in range(TEAMS) if
                         team_to_conference(team) == team1_conf and team not in teams_in_div]
        teams_other_conf = [team for team in range(TEAMS) if team not in teams_in_div and team not in teams_in_conf]
        div_vars = {t: [] for t in teams_in_div if t != team1}
        conf_vars_home = {t: [] for t in teams_in_conf}
        conf_vars_away = {t: [] for t in teams_in_conf}
        other_conf_vars = {t: [] for t in teams_other_conf}
        for week in range(WEEKS):
            for team2 in range(TEAMS):
                if team1 != team2:
                    team2_var = ys[week][team1][team2]
                    if team2 in teams_in_div:
                        div_vars[team2].append(team2_var)
                    elif team2 in teams_in_conf:
                        conf_vars_home[team2].append(team2_var)
                        conf_vars_away[team2].append(ys[week][team2][team1])
                    else:
                        other_conf_vars[team2].append(team2_var)
        for t in div_vars:
            # 4 games against same-division teams
            solver.Add(sum(div_vars[t]) == 2)
        for t in conf_vars_home:
            # 4 games against 6 same-conference teams
            solver.Add(sum(conf_vars_home[t]) <= 2)
            # 3 games against the remaining same-conference teams
            solver.Add(sum(conf_vars_home[t]) + sum(conf_vars_away[t]) >= 3)
        for t in other_conf_vars:
            # 2 games against the other-conference teams
            solver.Add(sum(other_conf_vars[t]) == 1)

    return solver, [xs, ys]


def add_cost(solver, vars):
    xs, ys = vars
    zs = [[None for team in range(TEAMS)] for week in range(WEEKS)]
    for week in range(WEEKS):
        for team in range(TEAMS):
            zs[week][team] = solver.BoolVar(f'z_{week}_{team}')

    for week in range(WEEKS):
        for team1 in range(TEAMS):
            home_vars = [ys[week][team1][team2] for team2 in range(TEAMS) if team1 != team2]
            away_vars = [ys[week][team2][team1] for team2 in range(TEAMS) if team1 != team2]
            solver.Add(zs[week][team1] >= sum(home_vars) + sum(away_vars) - 3)

    ws = [solver.BoolVar(f'w_{team}') for team in range(TEAMS)]
    for team in range(TEAMS):
        week_zs = []
        for week in range(WEEKS):
            week_zs.append(zs[week][team])
        solver.Add(ws[team] >= sum(week_zs))

    v = solver.Var(0, solver.infinity(), False, "v")
    for team in range(TEAMS):
        solver.Add(v >= ws[team])
    solver.Minimize(v)

    # solver.Minimize(sum(np.array(zs).flatten()))

    return vars + [zs, ws, v]



def solve(solver, vars):
    ys = vars[1]
    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())

        flattened = [y for y in np.array(ys).flatten() if y is not None]
        print(f'Number of matches: {sum(y.solution_value() for y in flattened)}')

        # Debugging
        # team1 = 0
        # print(ws[team1].solution_value())
        # for week in range(weeks):
        #     home_vars = [ys[week][team1][team2] for team2 in range(teams) if team1 != team2]
        #     away_vars = [ys[week][team2][team1] for team2 in range(teams) if team1 != team2]
        #     print(team1, week, sum(map(lambda x: x.solution_value(), home_vars)) + sum(map(lambda x: x.solution_value(), away_vars)))
        #     print(zs[week][team1].solution_value())
        # for week in range(weeks):
        #     for team1 in range(teams):
        #         for team2 in range(teams):
        #             if team1 != team2:
        #                 print(ys[week][team1][team2], ys[week][team1][team2].solution_value())

        # If provided in the command-line, write the schedule to a csv file
        try:
            with open(sys.argv[1], "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["week", "team1", "team2"])
                for week in range(WEEKS):
                    for team1 in range(TEAMS):
                        for team2 in range(TEAMS):
                            if team1 != team2:
                                if ys[week][team1][team2].solution_value():
                                    writer.writerow([week, team1, team2])
        except:
            pass

    else:
        print('The problem does not have an optimal solution.')

    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())


if __name__ == '__main__':
    solver, vars = base_model()
    # vars = add_cost(solver, vars)
    solve(solver, vars)