# Reads in a csv schedule and verifies NBA scheduling rules

import csv


# Handles test output
class TestDecorator:
    def __init__(self):
        self.decorated = []

    def __call__(self, func):
        def new(*args):
            try:
                func(*args)
                print(f"***{func.__doc__}***")
            except AssertionError:
                print(f"---{func.__doc__}---")

        self.decorated.append(new)
        return new

Test = TestDecorator()


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


def main():
    file_name = "schedule.csv"
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

    team_d = {team: [] for team in range(teams)}
    for row in rows:
        day = row[0]
        home_team = row[1]
        away_team = row[2]
        m = Match(day, home_team, away_team)
        team_d[home_team].append(m)
        team_d[away_team].append(m)

    # BEGIN TESTS
    for test in Test.decorated:
        test(teams, days, team_d)


@Test
def weekLimit(teams, days, team_d):
    """Team plays at most 4 matches / week"""
    for team in team_d:
        week_cnt = 0
        for day in range(days):
            for match in team_d[team]:
                if match.day == day:
                    week_cnt += 1
            if day % 7 == 6:
                assert week_cnt <= 4
                week_cnt = 0

@Test
def dayLimit(teams, days, team_d):
    """Team plays at most one match / day"""
    for team in team_d:
        for day in range(days):
            day_cnt = 0
            for match in team_d[team]:
                if match.day == day:
                    day_cnt += 1
            assert day_cnt <= 1

@Test
def homeAway(teams, days, team_d):
    """Team plays 41 home and 41 away games"""
    for team in team_d:
        home_cnt = 0
        away_cnt = 0
        for match in team_d[team]:
            if match.home_team == team:
                home_cnt += 1
            else:
                away_cnt += 1
        assert home_cnt == 41
        assert away_cnt == 41

@Test
def divMatches(teams, days, team_d):
    """Team plays 4 matches against division"""
    for team in team_d:
        teams_in_div = [t for t in range(teams) if t != team and team_to_division(t) == team_to_division(team)]
        teams_cnt = {t: 0 for t in teams_in_div}
        for match in team_d[team]:
            if match.home_team in teams_in_div:
                teams_cnt[match.home_team] += 1
            elif match.away_team in teams_in_div:
                teams_cnt[match.away_team] += 1
        assert all(cnt == 4 for cnt in teams_cnt.values())

@Test
def otherConfMatches(teams, days, team_d):
    """Team plays exactly 1 match against teams in the other conference"""
    for team in team_d:
        teams_in_conf = [t for t in range(teams) if team_to_conference(t) != team_to_conference(team)]
        teams_cnt = {t: 0 for t in teams_in_conf}
        for match in team_d[team]:
            if match.home_team in teams_in_conf:
                teams_cnt[match.home_team] += 1
            elif match.away_team in teams_in_conf:
                teams_cnt[match.away_team] += 1
        assert all(cnt == 1 for cnt in teams_cnt.values())

@Test
def sameConfMatches4(teams, days, team_d):
    """Team plays 4 matches against 6 teams in conference (outside of division)"""
    for team in team_d:
        teams_in_conf = [t for t in range(teams) if team_to_conference(t) == team_to_conference(team) and team_to_division(t) != team_to_division(team)]
        teams_cnt = {t: 0 for t in teams_in_conf}
        for match in team_d[team]:
            if match.home_team in teams_in_conf:
                teams_cnt[match.home_team] += 1
            elif match.away_team in teams_in_conf:
                teams_cnt[match.away_team] += 1
        assert sum(cnt == 4 for cnt in teams_cnt.values()) == 6

@Test
def sameConfMatches3(teams, days, team_d):
    """Team plays 3 matches against 4 teams in conference (outside of division)"""
    for team in team_d:
        teams_in_conf = [t for t in range(teams) if t != team and team_to_conference(t) == team_to_conference(team) and team_to_division(t) != team_to_division(team)]
        teams_cnt = {t: 0 for t in teams_in_conf}
        for match in team_d[team]:
            if match.home_team in teams_in_conf:
                teams_cnt[match.home_team] += 1
            elif match.away_team in teams_in_conf:
                teams_cnt[match.away_team] += 1
        assert sum(cnt == 3 for cnt in teams_cnt.values()) == 4


if __name__ == "__main__":
    main()