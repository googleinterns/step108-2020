from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd
import requests
import time

def get_season_stats(season_start=1997, season_end = 2018, per_mode = "PerPossession", verbose = False, saveas = None):
    lst = []
    time_taken = [10]
    start = timeit.default_timer()
    for season in range(season_start, season_end + 1):
        time.sleep(0.36)

        successful = False
        while not successful:
            try:
                get_start = timeit.default_timer()
                games = leaguedashplayerstats.LeagueDashPlayerStats(per_mode_detailed = per_mode, season = f"{season}-{str(season+1)[-2:]}", timeout=round(2*sum(time_taken)/len(time_taken), 0))
                get_end = timeit.default_timer()
                time_taken.append(get_end-get_start)
                successful = True
            except Exception as e:
                if verbose:
                    print(f"Timeout error on season {season}-{str(season+1)[-2:]}, taking a 3 second break before resuming")
                time.sleep(3)

        gamelog = games.get_data_frames()[0]
        gamelog["SEASON"] = season
        lst.append(gamelog)
    season_infos = pd.concat(lst, axis = 0, ignore_index = True)
    if saveas:
        season_infos.to_csv(f"{saveas}.csv",index=False)
    return season_infos
