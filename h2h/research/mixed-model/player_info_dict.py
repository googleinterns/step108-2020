from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.endpoints import boxscoreplayertrackv2
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.static import teams
from json import JSONDecodeError
import pandas as pd
import numpy as np
import random
import requests
import math
import json
import time
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

games = pd.read_csv("../common-datasets/all_gamelogs.csv")
boxscores = pd.read_csv("../common-datasets/all_boxscores_concatenated.csv")
season_stats_per_poss = pd.read_csv("../common-datasets/player-seasons_per_possession.csv")
season_stats_totals = pd.read_csv("../common-datasets/player-seasons_totals.csv")
season_stats_advanced_totals = pd.read_csv("../common-datasets/player-seasons-advanced_totals.csv")
playerinfo = pd.read_csv("../common-datasets/commonplayerinfo.csv")

starters_boxscores = boxscores.dropna(subset = ["START_POSITION"])
starters_ids = list(starters_boxscores["PLAYER_ID"].unique())
list_all_game_ids = games[games['SEASON'] > 2002]["GAME_ID"].unique()

starters_dict = {x[0]:x[1] for x in list(zip(starters_boxscores["PLAYER_ID"], starters_boxscores["PLAYER_NAME"]))}

ids_dict = {x[1]:x[0] for x in list(zip(starters_boxscores["PLAYER_ID"], starters_boxscores["PLAYER_NAME"]))}

player_info_dict = {k:dict() for k in starters_dict.keys()} #starters_dict is ID -> NAME
for player_id in player_info_dict.keys():
    #trim the above datasets to only include the ones we want
    per_poss = season_stats_per_poss[season_stats_per_poss["PLAYER_ID"] == player_id].reset_index(drop=True)
    per_poss = per_poss.rename(index = {i:yr for i, yr in enumerate(list(per_poss["SEASON"]))})
    totals = season_stats_totals[season_stats_totals["PLAYER_ID"] == player_id].reset_index(drop=True)
    totals = totals.rename(index = {i:yr for i, yr in enumerate(list(totals["SEASON"]))})
    advanced = season_stats_advanced_totals[season_stats_advanced_totals["PLAYER_ID"] == player_id].reset_index(drop=True)
    advanced = advanced.rename(index = {i:yr for i, yr in enumerate(list(advanced["SEASON"]))})
    pinfo = playerinfo[playerinfo["PERSON_ID"] == player_id].reset_index(drop=True)
    player_info_dict[player_id] = dict()


    try:
        ht = int(list(advanced["PLAYER_HEIGHT_INCHES"])[0])
    except Exception as e:
        print(player_id, starters_dict[player_id], e)
        ht = 6*12 + 6
    try:
        pick = int(list(advanced["DRAFT_NUMBER"])[0])
        if pick > 60:
            pick = "Undrafted"
    except:
        pick = "Undrafted"


    player_info_dict[player_id]["seasons_avail"] = sorted(list(totals["SEASON"]))
    player_info_dict[player_id]["FIRST_SEASON"] = int(pinfo.at[0,"FROM_YEAR"])
    player_info_dict[player_id]["PICK"] = pick
    player_info_dict[player_id]["HEIGHT"] = ht

    for season in player_info_dict[player_id]["seasons_avail"]:
        player_info_dict[player_id][season] = dict()
        player_season = player_info_dict[player_id][season]

        #stats from per_poss
        player_season["FG3M_PP"] = per_poss.at[season, "FG3M"]
        player_season["FG3A_PP"] = per_poss.at[season, "FG3A"]

        player_season["FTM_PP"] = per_poss.at[season, "FTM"]
        player_season["FTA_PP"] = per_poss.at[season, "FTA"]

        player_season["FG2M_PP"] = per_poss.at[season, "FGM"] - per_poss.at[season, "FG3M"]
        player_season["FG2A_PP"] = per_poss.at[season, "FGA"] - per_poss.at[season, "FG3A"]

        player_season["OREB_PP"] = per_poss.at[season, "OREB"]
        player_season["DREB_PP"] = per_poss.at[season, "DREB"]

        player_season["AST_PP"] = per_poss.at[season, "AST"]
        player_season["TOV_PP"] = per_poss.at[season, "TOV"]
        player_season["STL_PP"] = per_poss.at[season, "STL"]
        player_season["BLK_PP"] = per_poss.at[season, "BLK"]

        player_season["PF_PP"] = per_poss.at[season, "PF"]
        player_season["PFD_PP"] = per_poss.at[season, "PFD"]

        player_season["AGE"] = per_poss.at[season, "AGE"]


        #stats from totals
        player_season["MIN_TOT"] = totals.at[season, "MIN"]

        player_season["FG3M_TOT"] = totals.at[season, "FG3M"]
        player_season["FG3A_TOT"] = totals.at[season, "FG3A"]
        player_season["FG3_PCT"] = totals.at[season, "FG3_PCT"]
        player_season["FG3_FREQ"] = totals.at[season, "FG3A"] / max(totals.at[season, "FGA"], 1)

        player_season["FTM_TOT"] = totals.at[season, "FTM"]
        player_season["FTA_TOT"] = totals.at[season, "FTA"]
        player_season["FT_PCT"] = totals.at[season, "FT_PCT"]

        player_season["FG2M_TOT"] = totals.at[season, "FGM"] - totals.at[season, "FG3M"]
        player_season["FG2A_TOT"] = totals.at[season, "FGA"] - totals.at[season, "FG3A"]
        player_season["FG2_PCT"] = player_season["FG2M_TOT"] / max(player_season["FG2A_TOT"],1)

        player_season["OREB_TOT"] = totals.at[season, "OREB"]
        player_season["DREB_TOT"] = totals.at[season, "DREB"]

        player_season["AST_TOT"] = totals.at[season, "AST"]
        player_season["TOV_TOT"] = totals.at[season, "TOV"]
        player_season["STL_TOT"] = totals.at[season, "STL"]
        player_season["BLK_TOT"] = totals.at[season, "BLK"]

        player_season["PF_TOT"] = totals.at[season, "PF"]
        player_season["PFD_TOT"] = totals.at[season, "PFD"]

        player_season["W"] = totals.at[season, "W"]
        player_season["L"] = totals.at[season, "L"]
        player_season["W_PCT"] = totals.at[season, "W_PCT"]
        player_season["PLUS_MINUS"] = totals.at[season, "PLUS_MINUS"]
        player_season["AST/TOV"] = totals.at[season, "AST"] / max(totals.at[season, "TOV"],1) ##causes lots of NaN

        #stats from advanced
        player_season["NET_RATING"] = advanced.at[season, "NET_RATING"]
        player_season["OREB_PCT"] = advanced.at[season, "OREB_PCT"]
        player_season["DREB_PCT"] = advanced.at[season, "DREB_PCT"]
        player_season["USG_PCT"] = advanced.at[season, "USG_PCT"]
        player_season["TS_PCT"] = advanced.at[season, "TS_PCT"]
        player_season["AST_PCT"] = advanced.at[season, "AST_PCT"]

        #static stats
        player_season["HEIGHT"] = ht

with open('player_info_dict.json', 'w') as fp:
    json.dump(player_info_dict, fp, cls=NpEncoder)

with open('starters_dict.json', 'w') as fp:
    json.dump(starters_dict, fp, cls=NpEncoder)

with open('ids_dict.json', 'w') as fp:
    json.dump(ids_dict, fp, cls=NpEncoder)
