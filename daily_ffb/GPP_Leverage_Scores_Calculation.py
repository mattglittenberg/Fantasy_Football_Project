import pandas as pd
from math import erf, sqrt


class Leverage:

    def __init__(self):
        self.winning_play()

    def winning_play(self):
        target_scores_fanduel = pd.DataFrame(
            {'Salary': [4500, 6000, 7500, 9000], 'QB': [0, 27.9, 28.8, 29.7], 'RB': [24.5, 25.5, 26.5, 27.4],
             'WR': [22.4, 23.6, 24.7, 25.9], 'TE': [17.1, 18.7, 20.3, 21.9], 'D': [17.1, 0, 0, 0]})

        target_scores_dk = pd.DataFrame(
            {'Salary': [4500, 6000, 7500, 9000], 'QB': [0, 31.2, 32.2, 33.2], 'RB': [28.0, 29.0, 30.0, 31.1],
             'WR': [26.8, 28.1, 29.4, 230.7], 'TE': [24.0, 26.3, 28.6, 0], 'D': [15.3, 0, 0, 0]})

        # proj = mu = mean
        # stdev =
        # t_score = target_score
        proj = 17.1825
        stdev = 5.3
        t_score = 26.5
        prob = ((1 - (erf((t_score - proj) / (stdev * sqrt(2))))) / 2) * 100
        print(prob)

        # Target Scores
        # 4500 - 5,999

    def implied_ownership(self):
        pass

        # Take sum of all players at a position hitting there top score(from winning play) / proj
        # Then multiply by sum of all ownership at the position?

    def ownership(self):
        pass


Leverage()
