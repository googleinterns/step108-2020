from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.endpoints import boxscoreplayertrackv2
from ast import literal_eval
import pandas as pd
import time

def player_in_game_dataset_encoded(season_start, season_end = 2018, read_filepath = None, write_filepath = None, write_filepath_unencoded = None):
    """ 'k-hot encodes' a dataframe that has lists of players on the winning
    and losing teams of a game

    Generates or reads a dataset that contains a record of games, with columns
    containing the players on each team, and a record of the team ID of both the
    winning team and the home team to help encode the dataset. Then, encodes it,
    placing 1 or -1 appropriately on each player's column. Intended to be used
    for machine learning.

    Args:
        season_start: First season of data to encode. If you put in 2015, this
            means it will use the 2015-2016 season.
        season_end: Last season of data to encode, inclusive. Same format as
            above.
        read_filepath: Without this arg, this method will generate a new datset.
            If given, it will instead read a CSV with the given name.
        write_filepath: By default, function onloy returns a dataframe. If you
            want to save it, put a .csv file name in this arg
        write_filepath_unencoded: If you are generating a raw dataset first,
            this will save it instead of having to generate it each time.

    Returns:
        A dataframe that has columns for every individual player in the raw
        dataset that was either read from CSV or generated, plus a label column
        indicating the outcome of the game. Each row represents a game. A
        player's value in a given row is -1 if they were on the away team, 1 if
        trhey were on the home team. Label column is 1 for a home win, 0 for an
        away win.

    Raises:
        None
    """
    if read_filepath:
        raw_dataset = pd.read_csv(read_filepath)
        #when we read csv, a set will be interpreted as a string so we have to evaluate
        raw_dataset["winning_team_players"] = raw_dataset["winning_team_players"].apply(lambda x:literal_eval(x))
        raw_dataset["losing_team_players"] = raw_dataset["losing_team_players"].apply(lambda x:literal_eval(x))
    else:
        if write_filepath_unencoded:
            raw_dataset = player_in_game_dataset(season_start, season_end, write_filepath = write_filepath_unencoded)
        else:
            raw_dataset = player_in_game_dataset(season_start, season_end)

    #want the names of all the players who played, because that will be our feature column names
    all_players = set()
    for row in record.itertuples():
        all_players.update(row.winning_team_players,row.losing_team_players)
    all_players = sorted(list(all_players))

    #we condense all the names for ease, then add a label column, and create the dataframe
    cols = [condensed_name(player) for player in all_players]
    cols.append("label")
    encoded_record = pd.DataFrame(columns=cols, index=range(record.shape[0]))
    for row in raw_dataset.itertuples():

        #label is 1 for a home win, and home players have a 1 / away players have a -1
        if row.winning_team_id == row.home_team_id:
            for player in row.winning_team_players:
                encoded_record.at[row.Index, condensed_name(player)] = 1
            for player in row.losing_team_players:
                encoded_record.at[row.Index, condensed_name(player)] = -1
            encoded_record.at[row.Index, "label"] = 1
        #label is 0 for an away win, home players again have 1 / away players -1
        else:
            for player in row.winning_team_players:
                encoded_record.at[row.Index, condensed_name(player)] = -1
            for player in row.losing_team_players:
                encoded_record.at[row.Index, condensed_name(player)] = 1
            encoded_record.at[row.Index, "label"] = 0
    #the places where we didn't put a 1 or a -1 are NaN by default, so we fill with 0s
    encoded_record = encoded_record.fillna(0)
    if write_filepath:
        encoded_record.to_csv(write_filepath,index=False)
    return encoded_record



def player_in_game_dataset(season_start, season_end = 2018, write_filepath = None):
    """ Generates a dataframe of NBA games in a given time period, recording the
    players who played on each side of the game.


    Generates a dataset that contains a record of games, with columns
    containing the players on each team, and a record of the team ID of both the
    winning team and the home team.

    Args:
        season_start: First season of data to get. If you put in 2015, this
            means it will use the 2015-2016 season.
        season_end: Last season of data to get, inclusive. Same format as
            above.
        write_filepath: By default, function onloy returns a dataframe. If you
            want to save it, put a .csv file name in this arg

    Returns:
        A dataframe that has columns: 'winning_team_id', 'home_team_id',
        'game_id', 'winning_team_players' (set), 'losing_team_players' (set)

    Raises:
        None
    """

    record = pd.DataFrame(columns=['game_id', 'home_team_id', 'winning_team_id', 'winning_team_players', 'losing_team_players'])

    for year in range(season_start,season_end+1):
        #get all games in a season, then unpack the dataframe
        gamelog_for_season = try_to_get("gamelog", year)
        gamelog_df = gamelog_for_season.get_data_frames()[0]

        for row in gamelog_df.itertuples():
            if row.WL == "W": #only want the winning team so we don't duplicate games

                #unpack the return item to get the dataframe we want
                bx = try_to_get("boxscore", row.GAME_ID)
                individual_boxscore = bx.get_data_frames()[0]
                players_dict = map_team_to_players(individual_boxscore)

                #definitions for our insertion into the dataframe
                game_id = row.GAME_ID
                winning_team_id = row.TEAM_ID
                losing_team_id = next(iter(set(players_dict.keys()) - {winning_team_id}))
                winning_team_players = players_dict[winning_team_id]
                losing_team_players = players_dict[losing_team_id]
                # MATCHUP column has vs. if home game and @ if away game... since we only consider winning teams, if we check the MATCHUP column we implicitly know which team won
                home_team_id = winning_team_id if "vs." in row.MATCHUP else losing_team_id

                #now, insert into the record
                record = record.append({'game_id': game_id, \
                                        'home_team_id': home_team_id, \
                                        'winning_team_id': winning_team_id, \
                                        'winning_team_players': winning_team_players, \
                                        'losing_team_players': losing_team_players},\
                                         ignore_index = True)
    if write_filepath:
        record.to_csv(write_filepath,index=False)
    return record

def str_to_mins(inp):
    """ Quick method to convert strings in form x:xx or xx:xx into integer
    seconds"""
    lst = inp.split(":")
    sec = int(lst[0])*60 + int(lst[1])
    return sec

def try_to_get(endpoint, parameter, max_retries = 5, timeout = 10):
    """ Quick method to try to connect tp the NBA API endpoint. The NBA API is
    notoriously annoying to connect to, so this method tries to circumvent that.
    Has different uses for different endpoints"""
    for _ in range(max_retries):
        try:
            time.sleep(.2) #little delay so the NBA site doesn't get mad
            if endpoint == "boxscore":
                ret = boxscoreplayertrackv2.BoxScorePlayerTrackV2(parameter, timeout = timeout)
            elif endpoint = "gamelog":
                ret = leaguegamelog.LeagueGameLog(season=parameter, timeout = timeout)
            break
        except:
            pass
    return ret

def map_team_to_players(boxscore, min = 3):
    """Given a boxscore for a game, makes a dict mapping teams -> players who
    played >= 'min' minutes in this game for that team"""
    team_list = boxscore['TEAM_ID'].unique()
    players_dict = {k:set() for k in team_list}
    for innerrow in boxscore.itertuples():
        if str_to_mins(innerrow.MIN) >= min*60:
            players_dict[innerrow.TEAM_ID].add(innerrow.PLAYER_NAME)
    return players_dict

def condensed_name(name):
    """Very quick method that removes all the spaces in a player's name. Used
    to make their names suitable to be a column name."""
    return name.replace(" ", "")
