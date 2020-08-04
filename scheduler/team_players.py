import csv
import json

YEAR = 2018

teams = {}
with open("teams.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    cols = next(reader)
    team_id = cols.index("team_id")
    for row in reader:
        teams[row[team_id]] = row

allgames = {}
with open("allgames.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    cols = next(reader)
    game_id = cols.index("GAME_ID")
    team_id = cols.index("TEAM_ID")
    for row in reader:
        year = int(row[0][1:])
        if year == YEAR:
            allgames[row[game_id]] = {"teams": [row[team_id], next(reader)[team_id]], "scores": []}

with open("all_boxscores_concatenated.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    cols = next(reader)
    game_id = cols.index("GAME_ID")
    player_name = cols.index("PLAYER_NAME")
    start_pos = cols.index("START_POSITION")
    for row in reader:
        id = row[game_id]
        if id in allgames:
            allgames[id]["scores"].append(row)

def filter(players):
    return [f"{player[player_name]}{YEAR}{player[start_pos]}" for player in players]

players = {}
for team in teams:
    for gamedex in allgames:
        game = allgames[gamedex]
        if team in game["teams"]:
            scores = game["scores"]
            if team == "1610612762" or team == "1610612758":
                print()
            begin = 0
            for score in scores:
                if score[1] == team:
                    break
                begin += 1
            players[team] = filter(scores[begin:begin+5])
            break

with open("team_players.json", "w") as f:
    json.dump(players, f)
