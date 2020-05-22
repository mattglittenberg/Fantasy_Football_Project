from functools import lru_cache
import numpy as np
import pandas as pd

@lru_cache(200) # Define a cache with 200 empty slots
def get_games(year,week):
    g = nflgame.games(year,week=week)
    return nflgame.combine_game_stats(g)



def get_score_for_player(player):
    # Sample the year and week
    year = np.random.choice([2013, 2014, 2015],
                            p=[.2, .3, .5])
    week = np.random.randint(1, 18)

    # Find the player and score them for the given week/year
    for p in get_games(year, week):
        if p.player is None:
            continue
        if player == p.player:
            return score_player(p)

    return get_score_for_player(player)  # Retry due to bye weeks / failure for any other reason

def simulate(team, exps=10):
    scores = pd.DataFrame(data=np.zeros((exps,len(team))),
                          columns = [p.name for p in team])
    for n in range(exps):
        for player in team:
            scores.loc[n,player.name] += get_score_for_player(player)
    return scores


outcome = simulate(tm, exps=100)
outcome.head()
