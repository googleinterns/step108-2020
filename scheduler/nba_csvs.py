import requests
import json
import csv
import datetime
import io
import os

OK = 200
team_dir = ""
team_file = "teams.csv"

team_url = "http://data.nba.net/json/cms/noseason/sportsmeta/nba_teams.json"
response = requests.get(team_url)
if response.status_code == OK:
    teams = json.loads(response.content)["sports_content"]["teams"]["team"]
    # NBA API shenanigans
    nba_teams = [team for team in teams if team["is_nba_team"] is True and team["team_name"] != "Home"]
    # Group teams by conference then division (0-14 is one conference and 0-4 is one division)
    nba_teams.sort(key=lambda x: (x["conference"], x["division_id"]))
    if team_dir != "" and not os.path.exists(team_dir):
        os.makedirs(team_dir)
        print(f"Creating {team_dir}/")
    with open(team_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(nba_teams[0].keys())
        for team in nba_teams:
            values = [item[1] for item in team.items()]
            writer.writerow(values)
else:
    print("NBA API call failed to get teams")
    exit(1)

print(f"Wrote teams to {team_file}")


def game_to_date(game):
    date = datetime.datetime.strptime(game[5], "%Y-%m-%d")
    return date


abrv_to_no = {}
for i, team in enumerate(nba_teams):
    abrv_to_no[team["team_abbrev"]] = i

initial_year = 1997
final_year = 2018

yearly = {year: [] for year in range(initial_year, final_year + 1)}
with open("allgames.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    cols = next(reader)
    for row in reader:
        year = int(row[0][1:])
        yearly[year].append(row)
        next(reader) # Every game is duplicated

first_days = {}
wins = {}
GSW = []
homie = []
for year in range(2012, final_year + 1):
    games = yearly[year]
    with open(f'past_schedules/{year}.csv', "w") as f:
        writer = csv.writer(f)
        writer.writerow(["day", "team1", "team2"])
        first_day = game_to_date(games[0])
        first_days[year] = str(first_day)
        wins[year] = []
        for game in games:
            try:

                matchup = game[6].split(" ")
                day = (game_to_date(game) - first_day).days
                team1 = abrv_to_no[matchup[0]]
                team2 = abrv_to_no[matchup[2]]

                team1Home = matchup[1] == "@"
                team1Won = game[7] == "W"
                home_team = team1 if team1Home else team2
                away_team = team2 if team1Home else team1
                homeTeamWon = True if (team1Won and team1Home) or (not team1Won and not team1Home) else False
                writer.writerow([day, home_team, away_team])
                wins[year].append(homeTeamWon)

            except KeyError as e:
                print(e)
                print(f"{year} failed")
                break
with open(f'past_schedules/first_days.json', 'w') as f:
    json.dump(first_days, f)
for year in range(2012, final_year + 1):
    with open(f'past_schedules/wl/{year}.json', 'w') as f:
        json.dump(wins[year], f)

