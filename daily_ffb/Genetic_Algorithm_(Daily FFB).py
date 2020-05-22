import pandas as pd
import random
import time
import ujson


# OPTIMIZE: Optimize Algorithm
# TODO: Make better fitness function
# TODO: Incorporate Injury news
# FIXME: Determine how to incorporate actual points for testing
# FIXME: Not sure this is optimizing points?

class GeneticAlgorithm:

    def __init__(self, num_lineups, runtime=60, test=False):
        self.source = input("Which site would you like lineups for?")
        self.num_lineups = num_lineups
        self.runtime = runtime
        self.test = test
        self.qb = []
        self.rb = []
        self.wr = []
        self.te = []
        self.flex = []
        self.dst = []
        self.top_lineups = []

    def player_load(self):
        if self.source == 'fd':
            roster = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/daily_ffb/final_roster_fd.csv')
            roster.drop(['index', 'pos_rank', 'drop_off', 'sd_pts', 'floor', 'ceiling',  'avg_type', 'avg'], axis=1, inplace=True)
        elif self.source == 'dk':
            roster = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/daily_ffb/final_roster_dk.csv')
            roster.drop(['pos_rank', 'drop_off', 'sd_pts', 'avg_type', 'avg'], axis=1, inplace=True)
        elif self.source == 'yh':
            roster = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/daily_ffb/final_roster_yh.csv')
            roster.drop(['pos_rank', 'drop_off', 'sd_pts', 'avg_type', 'avg'], axis=1, inplace=True)

        # if self.test:
        #     actual = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/daily_ffb/week_13.csv', sep=';')
        #     name_list = actual['Name'].to_list()
        #     name_list = [" ".join(n.split(", ")[::-1]) for n in name_list]
        #     actual['Name'] = name_list
        #     actual.Name.replace({'Tampa Bay': 'Tampa Bay Buccaneers', 'Kansas City': 'Kansas City Chiefs',
        #                          'Tennessee': 'Tennessee Titans', 'LA Rams': 'Los Angeles Rams',
        #                          'New Orleans': 'New Orleans Saints',
        #                          'Cincinnati': 'Cincinnati Bengals', 'Pittsburgh': 'Pittsburgh Steelers',
        #                          'Buffalo': 'Buffalo Bills',
        #                          'Washington': 'Washington Redskins', 'Green Bay': 'Green Bay Packers',
        #                          'Indianapolis': 'Indianapolis Colts',
        #                          'Denver': 'Denver Broncos', 'Minnesota': 'Minnesota Vikings',
        #                          'Baltimore': 'Baltimore Ravens',
        #                          'Jacksonville': 'Jacksonville Jaguars', 'Carolina': 'Carolina Panthers',
        #                          'Seattle': 'Seattle Seahawks',
        #                          'Houston': 'Houston Texans', 'Chicago': 'Chicago Bears', 'Dallas': 'Dallas Cowboys',
        #                          'Cleveland': 'Cleveland Browns', 'San Francisco': 'San Francisco 49ers',
        #                          'Detroit': 'Detroit Lions',
        #                          'Miami': 'Miami Dolphins', 'New York J': 'New York Jets',
        #                          'New England': 'New England Patriots',
        #                          'LA Chargers': 'Los Angeles Chargers', 'Philadelphia': 'Philadelphia Eagles',
        #                          'Oakland': 'Oakland Raiders',
        #                          'Atlanta': 'Atlanta Falcons', 'Arizona': 'Arizona Cardinals',
        #                          'New York G': 'New York Giants'}, inplace=True)
        #     actual.drop(
        #         ['Week', 'Year', 'GID', 'Pos', 'Team', 'h/a', 'Oppt',
        #          'FD salary'], axis=1, inplace=True)
        #
        #     roster = pd.merge(roster, actual, on='Name')
        players = roster.to_dict('index')

        # OPTIMIZE: Is there a way to speed this up?
        for key in players:
            if players.get(key).get('points') > 0:
                if players.get(key).get('position') == 'QB':
                    self.qb.append(players.get(key))
                elif players.get(key).get('position') == 'RB':
                    self.rb.append(players.get(key))
                elif players.get(key).get('position') == 'WR':
                    self.wr.append(players.get(key))
                elif players.get(key).get('position') == 'TE':
                    self.te.append(players.get(key))
                elif players.get(key).get('position') == 'DST':
                    self.dst.append(players.get(key))

                if players.get(key).get('position') != 'DST' and players.get(key).get('position') != 'QB':
                    self.flex.append(players.get(key))

    def create_lineup(self):
        while True:
            lineup = [self.qb[random.randint(0, (len(self.qb) - 1))], self.rb[random.randint(0, (len(self.rb) - 1))],
                      self.rb[random.randint(0, (len(self.rb) - 1))], self.wr[random.randint(0, (len(self.wr) - 1))],
                      self.wr[random.randint(0, (len(self.wr) - 1))], self.wr[random.randint(0, (len(self.wr) - 1))],
                      self.te[random.randint(0, (len(self.te) - 1))],
                      self.flex[random.randint(0, (len(self.flex) - 1))],
                      self.dst[random.randint(0, (len(self.dst) - 1))]]

            lineup = self.good_lineup(lineup)
            if lineup:
                return lineup

    def good_lineup(self, lineup):

        total_pts = 0
        total_salary = 0
        actual_points = 0
        total_teams = []
        total_players = len(set(player['name'] for player in lineup))

        # OPTIMIZE
        for player in lineup:
            total_pts += round(player['points'], 3)
            total_salary += player['salary']
            # if self.test:
            #     actual_points += player['FD points']
            if player['team'] not in total_teams:
                total_teams.append(player['team'])

        if total_salary < 60000 and len(total_teams) and total_players == 9:
            lineup.extend((total_salary, total_pts))
            return lineup
        else:
            return False

    # OPTIMIZE: Currently slowest running method
    def mate_lineups(self, lineup1, lineup2):

        qbs = [lineup1[0], lineup2[0], self.qb[random.randint(0, (len(self.qb) - 1))],
               self.qb[random.randint(0, len(self.qb) - 1)]]
        rbs = [lineup1[1], lineup1[2], lineup2[1], lineup2[2], self.rb[random.randint(0, (len(self.rb) - 1))]]
        wrs = [lineup1[3], lineup1[4], lineup1[5], lineup2[3], lineup2[4], lineup2[5],
               self.wr[random.randint(0, (len(self.wr) - 1))]]
        tes = [lineup1[6], lineup2[6], self.te[random.randint(0, (len(self.te) - 1))],
               self.te[random.randint(0, len(self.te) - 1)]]
        flex = [lineup1[7], lineup2[7], self.flex[random.randint(0, (len(self.flex) - 1))],
                self.flex[random.randint(0, len(self.flex) - 1)]]
        dst = [lineup1[8], lineup2[8], self.dst[random.randint(0, (len(self.dst) - 1))],
               self.dst[random.randint(0, len(self.dst) - 1)]]

        def select_players(p_list, num_needed):
            open_players = ujson.loads(ujson.dumps(p_list))
            final_players = []
            while len(final_players) < num_needed:
                idx = random.randint(0, (len(open_players) - 1))
                final_players.append(open_players[idx])
                open_players.remove(open_players[idx])

            return final_players

        while True:
            mated_lineup = []
            mated_lineup.extend(select_players(qbs, 1))
            mated_lineup.extend(select_players(rbs, 2))
            mated_lineup.extend(select_players(wrs, 3))
            mated_lineup.extend(select_players(tes, 1))
            mated_lineup.extend(select_players(flex, 1))
            mated_lineup.extend(select_players(dst, 1))

            lineup = self.good_lineup(mated_lineup)

            if lineup:
                return lineup

    # TODO: Make more greedy, maybe do some reading?
    def generate_lineups(self):

        new_lineups = [self.create_lineup() for _ in range(10)]
        new_lineups.sort(key=lambda x: x[-2], reverse=True)

        self.top_lineups.extend(new_lineups)

        offspring1 = self.mate_lineups(new_lineups[0], new_lineups[1])
        offspring2 = self.mate_lineups(new_lineups[0], new_lineups[2])
        offspring3 = self.mate_lineups(new_lineups[1], new_lineups[2])

        self.top_lineups.append(
            self.mate_lineups(offspring1, self.top_lineups[random.randint(0, len(self.top_lineups) - 1)]))
        self.top_lineups.append(
            self.mate_lineups(offspring2, self.top_lineups[random.randint(0, len(self.top_lineups) - 1)]))
        self.top_lineups.append(
            self.mate_lineups(offspring3, self.top_lineups[random.randint(0, len(self.top_lineups) - 1)]))

        self.top_lineups.append(offspring1)
        self.top_lineups.append(offspring2)
        self.top_lineups.append(offspring3)

    def run_program(self):

        total_time = time.time() + self.runtime

        while time.time() < total_time:
            self.generate_lineups()
            self.top_lineups.sort(key=lambda x: x[-2], reverse=True)
            self.top_lineups = self.top_lineups[:(self.num_lineups + 1)]

    def save(self):

        final_lineups = [[player['name'] if isinstance(player, dict) else player for player in lineup]
                         for lineup in self.top_lineups]

        # TODO: If this works, change to faster method using list(OrderedDict.fromkeys(list)

        final_lineups = [final_lineups[i] for i in range(len(final_lineups) - 1) if
                         final_lineups[i] != final_lineups[i + 1]]
        # FIXME: ADD player ID to projections
        # lineups_for_upload = [[player['Id'] if isinstance(player, dict) else player for player in lineup]
        #                       for lineup in self.top_lineups]
        # lineups_for_upload = [lineup[:9] for lineup in lineups_for_upload]

        final_header = ['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE', 'FLEX', 'D', 'SALARY', 'POINTS']
        # upload_header = ['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE', 'FLEX', 'D']

        final = pd.DataFrame(final_lineups, columns=final_header)
        print(final)
        # if self.test:
        #     final['ERROR'] = abs(final['POINTS'] - final['ACTUAL'])
        #     final['% ERROR'] = abs((final['ERROR'] / final['ACTUAL']) * 100)
        # upload = pd.DataFrame(lineups_for_upload, columns=upload_header)

        # final.to_csv(
        #     r'C:\Users\mattg\PycharmProjects\Fantasy_Football\daily_ffb\Lineups\Test_Files\final_lineups_05182020_test.csv',
        #     index=False, header=True)
        # upload.to_csv(r'C:\Users\mattg\PycharmProjects\Fantasy_Football\daily_ffb\Lineups\upload_lineups.csv',
        #               index=False, header=True)


# if __name__ == "__main__":
#     g = GeneticAlgorithm(num_lineups=15, runtime=6)
#     g.player_load()
#     g.run_program()
#     g.save()

g = GeneticAlgorithm(num_lineups=5, runtime=5)
g.player_load()
g.run_program()
g.save()
