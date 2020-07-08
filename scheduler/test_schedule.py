import csv
import sys
import unittest
import os


class Match:
    def __init__(self, day, home_team, away_team):
        self.location = None
        self.day = day
        self.home_team = home_team
        self.away_team = away_team

    def __repr__(self):
        return f"Day: {str(self.day).rjust(3)}\tHome: {str(self.home_team).rjust(2)}\t Away: {self.away_team}\tWeek: {self.day // 7}\n"


NUM_IN_DIVISION = 5
def team_to_division(team):
    return team // NUM_IN_DIVISION


NUM_IN_CONFERENCE = 15
def team_to_conference(team):
    return team // NUM_IN_CONFERENCE


try:
    # Avoids argv errors with unittest
    file_name = os.path.join(os.path.abspath(os.path.dirname(__file__)), sys.argv.pop())
    print(file_name)
except:
    print(f"usage: python {__file__} relative_path_to_schedule")
    exit(1)

rows = []
teams = 0
days = 0

with open(file_name, "r") as f:
    reader = csv.reader(f)
    keys = reader.__next__()
    for row in reader:
        row = list(map(int, row))
        teams = max(teams, row[1], row[2])
        rows.append(row)
        days = max(days, row[0])

# Convert from 0-index to count
teams += 1
days += 1

team_d = {team: list() for team in range(teams)}
for row in rows:
    day = row[0]
    home_team = row[1]
    away_team = row[2]
    m = Match(day, home_team, away_team)
    team_d[home_team].append(m)
    team_d[away_team].append(m)


class AssignmentConstraints(unittest.TestCase):

    def testWeekLimit(self):
        """Team plays at most 4 matches / week"""
        for team in team_d:
            week_cnt = 0
            for day in range(days):
                for match in team_d[team]:
                    if match.day == day:
                        week_cnt += 1
                if day % 7 == 6:
                    assert week_cnt <= 4, "Team plays at most 4 matches / week"
                    week_cnt = 0

    def testDayLimit(self):
        """Team plays at most one match / day"""
        for team in team_d:
            for day in range(days):
                day_cnt = 0
                for match in team_d[team]:
                    if match.day == day:
                        day_cnt += 1
                assert day_cnt <= 1, "Team plays at most one match / day"

    def testHomeAway(self):
        """Team plays 41 home and 41 away games"""

        for team in team_d:
            home_cnt = 0
            away_cnt = 0
            for match in team_d[team]:
                if match.home_team == team:
                    home_cnt += 1
                else:
                    away_cnt += 1
            assert home_cnt == 41, "Team plays 41 home games"
            assert away_cnt == 41, "Team plays 41 away games"

    def testDivMatches(self):
        """Team plays 4 matches against division"""

        for team in team_d:
            teams_in_div = [t for t in range(teams) if t != team and team_to_division(t) == team_to_division(team)]
            teams_cnt = {t: 0 for t in teams_in_div}
            for match in team_d[team]:
                if match.home_team in teams_in_div:
                    teams_cnt[match.home_team] += 1
                elif match.away_team in teams_in_div:
                    teams_cnt[match.away_team] += 1
            assert all(cnt == 4 for cnt in teams_cnt.values()), "Team plays 4 matches against division"

    def testOtherConfMatches(self):
        """Team plays exactly 2 matches against teams in the other conference"""

        for team in team_d:
            teams_in_conf = [t for t in range(teams) if team_to_conference(t) != team_to_conference(team)]
            teams_cnt = {t: 0 for t in teams_in_conf}
            for match in team_d[team]:
                if match.home_team in teams_in_conf:
                    teams_cnt[match.home_team] += 1
                elif match.away_team in teams_in_conf:
                    teams_cnt[match.away_team] += 1
            assert all(cnt == 2 for cnt in
                       teams_cnt.values()), "Team plays exactly 2 matches against teams in the other conference"

    def testSameConfMatches4(self):
        """Team plays 4 matches against 6 teams in conference (outside of division)"""

        for team in team_d:
            teams_in_conf = [t for t in range(teams) if
                             team_to_conference(t) == team_to_conference(team) and team_to_division(
                                 t) != team_to_division(team)]
            teams_cnt = {t: 0 for t in teams_in_conf}
            for match in team_d[team]:
                if match.home_team in teams_in_conf:
                    teams_cnt[match.home_team] += 1
                elif match.away_team in teams_in_conf:
                    teams_cnt[match.away_team] += 1
            assert sum(cnt == 4 for cnt in
                       teams_cnt.values()) == 6, "Team plays 4 matches against 6 teams in conference (outside of division)"

    def testSameConfMatches3(self):
        """Team plays 3 matches against 4 teams in conference (outside of division)"""

        for team in team_d:
            teams_in_conf = [t for t in range(teams) if
                             t != team and team_to_conference(t) == team_to_conference(team) and team_to_division(
                                 t) != team_to_division(team)]
            teams_cnt = {t: 0 for t in teams_in_conf}
            for match in team_d[team]:
                if match.home_team in teams_in_conf:
                    teams_cnt[match.home_team] += 1
                elif match.away_team in teams_in_conf:
                    teams_cnt[match.away_team] += 1
            assert sum(cnt == 3 for cnt in
                       teams_cnt.values()) == 4, "Team plays 3 matches against 4 teams in conference (outside of division)"


if __name__ == "__main__":
    unittest.main()
