from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.endpoints import boxscoreplayertrackv2
from ast import literal_eval
import pandas as pd
import time

def make_vals_and_labels(read_encoded = None, read_unencoded = None, write_encoded = None, season_start = 1997, season_end = 2018, write_unencoded = None):
    """ Makes an encoded dataset into usable numpy arrays.

    Generates or reads a dataset that contains a record of games, with columns
    representing the players and rows representing games. A player has 1 or -1
    on a row if they were home or away players in that game, respectively.
    Then, separates the target column and the data, and stores the feature list,
    to be used by the user (in theory to train a machine learning model).

    Args:
        read_encoded: Without this arg, this method will generate a new
            dataset. If given, it will instead read a CSV with the given name,
            and then separate into values and labels.
        read_unencoded: Used only if you want to call
            _encode_player_in_game_dataset. See downstream description.
        write_encoded: Used only if you want to call
            _encode_player_in_game_dataset. See downstream description.
        season_start: Used only if you want to call
            _encode_player_in_game_dataset. See downstream description.
        season_end: Used only if you want to call
            _encode_player_in_game_dataset. See downstream description.
        write_unencoded: Used only if you want to call
            _encode_player_in_game_dataset. See downstream description.

    Returns:
        - values: numpy array of dimension [number_of_games, number_of_players]
        - labels: numpy array of dimension [number_of_games, 1]
        - feature_list: list of feature names, dimension [1, number_of_players]

    Raises:
        None
    """
    if read_encoded: #already have encoded csv... just read
        dataset = pd.read_csv(read_encoded) #no need to eval, all 0 and 1
    else:
        if read_unencoded: #have unencoded csv, just need to encode
            dataset = _encode_player_in_game_dataset(read_unencoded = read_unencoded)
        else: #don't have anything, need to generate from scratch
            dataset = _encode_player_in_game_dataset(season_start = season_start, season_end = season_end, write_encoded = write_encoded, write_unencoded = write_unencoded)

    labels = np.array(dataset['label'])
    values = ml_record.drop(['label'], axis = 1)
    feature_list = list(values.columns)
    values = np.array(values)

    return values, labels, feature_list


def _encode_player_in_game_dataset(read_unencoded = None, write_encoded = None, season_start = 1997, season_end = 2018, write_unencoded = None):
    """ 'k-hot encodes' a dataframe that has lists of players on the winning
    and losing teams of a game

    Calls _generate_player_in_game_dataset or reads a dataset that contains a
    record of games, with columns containing the players on each team, and a
    record of the team ID of both the winning team and the home team to help
    encode the dataset. Then, encodes it, placing 1 or -1 appropriately on each
    player's column.

    Args:
        read_unencoded: Without this arg, this method will generate a new
            dataset. If given, it will instead read a CSV with the given name,
            and then encode it.
        write_encoded: By default, function doesn't save the encoded dataset.
            If you want to save the encoded dataframe, put a .csv file name in
            this arg.
        season_start: Used only if you want to call
            _generate_player_in_game_dataset. See downstream description.
        season_end: Used only if you want to call
            _generate_player_in_game_dataset. See downstream description.
        write_unencoded: Used only if you want to call
            _generate_player_in_game_dataset. See downstream description.

    Returns:
        A dataframe that has columns for every individual player in the raw
        dataset that was either read from CSV or generated, plus a label column
        indicating the outcome of the game. Each row represents a game. A
        player's value in a given row is -1 if they were on the away team, 1 if
        they were on the home team. Label column is 1 for a home win, 0 for an
        away win.

    Raises:
        None
    """
    if read_unencoded: #have unencoded csv, just need to encode
        raw_dataset = pd.read_csv(read_unencoded)
        raw_dataset["winning_team_players"] = raw_dataset["winning_team_players"].apply(lambda x:literal_eval(x))
        raw_dataset["losing_team_players"] = raw_dataset["losing_team_players"].apply(lambda x:literal_eval(x))
    else: #generate from scratch, decide if want to write the unencoded to CSV
        raw_dataset = _generate_player_in_game_dataset(season_start, season_end, write_unencoded = write_unencoded)

    #want the names of all the players who played, because that will be our feature column names
    all_players = set()
    for row in raw_dataset.itertuples():
        all_players.update(row.winning_team_players,row.losing_team_players)
    all_players = sorted(list(all_players))

    #we condense all the names for ease, then add a label column, and create the dataframe
    cols = [condensed_name(player) for player in all_players]
    cols.append("label")
    encoded_data = pd.DataFrame(columns=cols, index=range(raw_dataset.shape[0]))
    for row in raw_dataset.itertuples():

        #label is 1 for a home win, and home players have a 1 / away players have a -1
        if row.winning_team_id == row.home_team_id:
            for player in row.winning_team_players:
                encoded_data.at[row.Index, condensed_name(player)] = 1
            for player in row.losing_team_players:
                encoded_data.at[row.Index, condensed_name(player)] = -1
            encoded_data.at[row.Index, "label"] = 1
        #label is 0 for an away win, home players again have 1 / away players -1
        else:
            for player in row.winning_team_players:
                encoded_data.at[row.Index, condensed_name(player)] = -1
            for player in row.losing_team_players:
                encoded_data.at[row.Index, condensed_name(player)] = 1
            encoded_data.at[row.Index, "label"] = 0
    #the places where we didn't put a 1 or a -1 are NaN by default, so we fill with 0s
    encoded_data = encoded_data.fillna(0)
    if write_encoded: #if they want the encoded data written, encode it
        encoded_data.to_csv(write_encoded,index=False)
    return encoded_data



def _generate_player_in_game_dataset(season_start, season_end, write_unencoded = None):
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
        write_unencoded: By default, function only returns a dataframe. If you
            want to save this unencoded dataset, put a .csv filename in this arg

    Returns:
        A dataframe that has columns: 'winning_team_id' [int],
        'home_team_id' [int], 'game_id' [int], 'winning_team_players' [set],
        'losing_team_players' [set]

    Raises:
        None
    """
    record = pd.DataFrame(columns=['game_id', 'home_team_id', 'winning_team_id', 'winning_team_players', 'losing_team_players'])

    for year in range(season_start,season_end+1):
        #get all games in a season, then unpack the dataframe
        gamelog_for_season = _try_to_get("gamelog", year)
        gamelog_df = gamelog_for_season.get_data_frames()[0]

        for row in gamelog_df.itertuples():
            if row.WL == "W": #only want the winning team so we don't duplicate games

                #unpack the return item to get the dataframe we want
                bx = _try_to_get("boxscore", row.GAME_ID)
                individual_boxscore = bx.get_data_frames()[0]
                players_dict = _map_team_to_players(individual_boxscore)

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
    if write_unencoded:
        record.to_csv(write_unencoded,index=False)
    return record

def str_to_mins(inp):
    """ Quick method to convert strings in form x:xx or xx:xx into integer
    seconds"""
    lst = inp.split(":")
    sec = int(lst[0])*60 + int(lst[1])
    return sec

def _try_to_get(endpoint, parameter, max_retries = 5, timeout = 10):
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

def _map_team_to_players(boxscore, min = 3):
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
