from nba_api.stats.endpoints import leaguegamelog
import pandas as pd
import time
import timeit

def get_game_record(season_start=1997, season_end = 2018, verbose = False, saveas = None):
    lst = []
    time_taken = [10]
    start = timeit.default_timer()
    for season in range(season_start, season_end + 1):
        time.sleep(0.36)
        successful = False
        while not successful:
            try:
                get_start = timeit.default_timer()
                games = leaguegamelog.LeagueGameLog(season = season, timeout=round(2*sum(time_taken)/len(time_taken), 0))
                get_end = timeit.default_timer()
                time_taken.append(get_end-get_start)
                successful = True
            except Exception as e:
                if verbose:
                    print(f"Timeout error on iteration {i}, taking a 3 second break before resuming")
                time.sleep(3)

        gamelog = games.get_data_frames()[0]
        lst.append(gamelog)
        if i%100 == 1:
            stop = timeit.default_timer()
            if verbose:
                print(f"{i-1}/26069 done: {round(i/26069*100,1)}% ... has taken {round((stop-start)/60,0)} min, total projected: {round((stop-start)/(i/26069)/60, 2)} min, remaining projected: {round(((stop-start)/(i/26069)-(stop-start))/60, 2)} min")
    games_concat = pd.concat(lst, axis = 0, ignore_index = True)
    if saveas:
        games_concat.to_csv(f"{saveas}.csv",index=False)
    return games_concat
