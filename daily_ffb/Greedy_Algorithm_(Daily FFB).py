import pandas as pd
import random
import time
import copy


# FIXME: Fix logic for putting in last player, must have 9 players and maximize FPPG

class GreedyAlgorithm:

    def __init__(self, num_lineups, runtime=60):
        self.num_lineups = num_lineups
        self.runtime = runtime
        self.salary_cap = 60000
        self.player_list = []
        self.load_players()
        self.create_lineup()

    def load_players(self):
        roster = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/daily_ffb/FanDuel_NFL_players.csv')
        roster.drop(
            ['First Name', 'Last Name', 'Played', 'Game', 'Opponent', 'Injury Indicator', 'Injury Details',
             'Tier'], axis=1, inplace=True)
        roster = roster [roster.FPPG > 0]
        roster.rename(columns={'Nickname': 'Name'}, inplace=True)
        roster['V/W'] = round(roster['FPPG']/roster['Salary'], 5)

        worth_df = roster.sort_values(by=['V/W'], inplace=True, ascending=False)
        self.player_list = roster.values.tolist()

        print(len(self.player_list))

#TODO: Write this method

    def create_lineup(self):
        lineup = []
        qb = 0
        rb = 0
        wr = 0
        te = 0
        dst = 0
        inx = 0
        while len(lineup) < 9 and inx < len(self.player_list) - 1:
            player = self.player_list[inx]
            pos = player[1]
            sal = player[4]
            if pos == 'QB' and qb < 1:
                lineup.append(player)
                self.salary_cap -= sal
                qb += 1
            elif pos == 'RB' and rb < 3 and wr < 4 and te < 2:
                lineup.append(player)
                self.salary_cap -= sal
                rb += 1
            elif pos == 'WR' and wr < 4 and rb < 3 and te < 2:
                lineup.append(player)
                self.salary_cap -= sal
                wr += 1
            elif pos == 'TE' and te < 2 and rb < 3 and wr < 4:
                lineup.append(player)
                self.salary_cap -= sal
                te += 1
            elif pos == 'D' and dst < 1:
                lineup.append(player)
                self.salary_cap -= sal
                dst += 1
            if self.salary_cap < 0:
                self.salary_cap += sal
                lineup.remove(player)
            inx += 1
        print(lineup)
        print(len(lineup))
        print(self.salary_cap)

GreedyAlgorithm(10)








