from nba_api.stats.endpoints import boxscoretraditionalv2
from ast import literal_eval
import pandas as pd
import time
import timeit

def get_boxscores(game_ids, verbose = False, saveas = None):
    total_ids = len(game_ids)
    lst = []
    time_taken = [10]
    start = timeit.default_timer()
    for i in range(len(game_ids)):
        time.sleep(0.36)
        gid = game_ids[i]

        successful = False
        while not successful:
            try:
                get_start = timeit.default_timer()
                bx = boxscoretraditionalv2.BoxScoreTraditionalV2(gid, timeout=round(2*sum(time_taken)/len(time_taken), 0))
                get_end = timeit.default_timer()
                time_taken.append(get_end-get_start)
                successful = True
            except Exception as e:
                if verbose:
                    print(f"Timeout error on iteration {i}, taking a 3 second break before resuming")
                time.sleep(3)

        players = bx.get_data_frames()[0]
        lst.append(players)
        if i%100 == 1:
            stop = timeit.default_timer()
            if verbose:
                print(f"{i-1}/{total_ids} done: {round(i/total_ids*100,1)}% ... has taken {round((stop-start)/60,0)} min, total projected: {round((stop-start)/(i/total_ids)/60, 2)} min, remaining projected: {round(((stop-start)/(i/total_ids)-(stop-start))/60, 2)} min")
    boxscores_concat = pd.concat(lst, axis = 0, ignore_index = True)
    if saveas:
        boxscores_concat.to_csv(f"{saveas}.csv",index=False)
    return boxscores_concat
