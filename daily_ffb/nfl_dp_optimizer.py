import csv
import pandas as pd
from tqdm import tqdm
import pulp

# FIXME: Testing not working, eliminating players, probs because names are different
# FIXME: self.salary_cap doesn't work, had to inherit it
# TODO: Add Flex position functionality
# OPTIMIZE: Optimize Algorithm


class DynamicProgrammingOptimizer:
    def __init__(self, num_lineups, overlap, solver, test=False):
        self.num_lineups = num_lineups
        self.overlap = overlap
        self.solver = solver
        self.test = test
        self.qb_df = None
        self.skill_players_df = None
        self.dst_df = None
        self.num_teams = None
        self.positions = {'RB': [], 'WR': [], 'TE': []}
        self.skill_player_teams = []
        self.qb_teams = []
        self.dst_teams = []
        self.dst_opponents = []
        self.num_qbs = 0
        self.num_skill_players = 0
        self.num_dsts = 0
        self.actuals = test
        self.salary_cap = 60000
        self.player_load()

    def player_load(self):
        roster = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/daily_ffb/final_roster_fd.csv')
        roster.drop(['index', 'pos_rank', 'drop_off', 'sd_pts','avg_type', 'avg'], axis=1,
                    inplace=True)

        if self.test:
            actual = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/daily_ffb/week_13.csv', sep=';')
            name_list = actual['Name'].to_list()
            name_list = [" ".join(n.split(", ")[::-1]) for n in name_list]
            actual['Name'] = name_list
            actual.Name.replace({'Tampa Bay': 'Tampa Bay Buccaneers', 'Kansas City': 'Kansas City Chiefs',
                                 'Tennessee': 'Tennessee Titans', 'LA Rams': 'Los Angeles Rams',
                                 'New Orleans': 'New Orleans Saints',
                                 'Cincinnati': 'Cincinnati Bengals', 'Pittsburgh': 'Pittsburgh Steelers',
                                 'Buffalo': 'Buffalo Bills',
                                 'Washington': 'Washington Redskins', 'Green Bay': 'Green Bay Packers',
                                 'Indianapolis': 'Indianapolis Colts',
                                 'Denver': 'Denver Broncos', 'Minnesota': 'Minnesota Vikings',
                                 'Baltimore': 'Baltimore Ravens',
                                 'Jacksonville': 'Jacksonville Jaguars', 'Carolina': 'Carolina Panthers',
                                 'Seattle': 'Seattle Seahawks',
                                 'Houston': 'Houston Texans', 'Chicago': 'Chicago Bears', 'Dallas': 'Dallas Cowboys',
                                 'Cleveland': 'Cleveland Browns', 'San Francisco': 'San Francisco 49ers',
                                 'Detroit': 'Detroit Lions',
                                 'Miami': 'Miami Dolphins', 'New York J': 'New York Jets',
                                 'New England': 'New England Patriots',
                                 'LA Chargers': 'Los Angeles Chargers', 'Philadelphia': 'Philadelphia Eagles',
                                 'Oakland': 'Oakland Raiders',
                                 'Atlanta': 'Atlanta Falcons', 'Arizona': 'Arizona Cardinals',
                                 'New York G': 'New York Giants'}, inplace=True)
            actual.drop(
                ['Week', 'Year', 'GID', 'Pos', 'Team', 'h/a', 'Oppt',
                 'FD salary'], axis=1, inplace=True)
            actual.rename(columns={'FD points': 'Actual'}, inplace=True)
            roster = pd.merge(roster, actual, on='Name')
        roster = roster[roster['points'] > 0]

        self.qb_df = roster[roster['position'] == 'QB']
        self.qb_df.reset_index(inplace=True)
        self.skill_players_df = roster[(roster['position'] != 'QB') & (roster['position'] != 'DST')]
        self.skill_players_df.reset_index(inplace=True)
        self.dst_df = roster[roster['position'] == 'DST']
        self.dst_df.reset_index(inplace=True)

        self.num_qbs = len(self.qb_df.index)
        self.num_skill_players = len(self.skill_players_df.index)
        self.num_dsts = len(self.dst_df.index)

    def create_indicators(self):
        # create list of teams and variable of number of teams
        teams = list(set(self.skill_players_df['team'].values))
        self.num_teams = len(teams)

        # create player position indicators so you know which position the players are
        for pos in self.skill_players_df.loc[:, 'position']:
            for key in self.positions:
                self.positions[key].append(1 if key in pos else 0)

        # create skill player team indicators so you know which team the players are on
        for player_team in self.skill_players_df.loc[:, 'team']:
            self.skill_player_teams.append([1 if player_team == team else 0 for team in teams])

        # create qb team indicators so you know which position the qb is on
        for qb_team in self.qb_df.loc[:, 'team']:
            self.qb_teams.append([1 if qb_team == team else 0 for team in teams])

        # create dst team indicators so you know which team the unit is
        for dst_team in self.dst_df.loc[:, 'team']:
            self.dst_teams.append([1 if dst_team == team else 0 for team in teams])

        # create dst opponent indicators so you know who the dst is opposing
        # for player_opp in self.skill_players_df.loc[:, 'Opponent']:
        #     self.dst_opponents.append([1 if player_opp == team else 0 for team in self.dst_df.loc[:, 'Team']])

    def create_lineups(self, eqn):

        lineups = []
        for _ in tqdm(range(self.num_lineups)):
            lineup = eqn(lineups)

            if lineup:
                lineups.append(lineup)
            else:
                break

        return lineups

    def save(self, filled_lineups, show_proj=False):
        header = ['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE', 'FLEX', 'D']
        up_header = ['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE', 'FLEX', 'D']
        if self.actuals:
            lineups_for_upload = [lineup[:-2] for lineup in filled_lineups]
            header.extend(('PROJ', 'ACTUAL'))
        else:
            lineups_for_upload = [lineup[:-1] for lineup in filled_lineups]
            header.append('PROJ')

        if not show_proj:
            with open("./dp_lineups.csv", 'w') as f:
                writer = csv.writer(f)
                writer.writerow(up_header)
                writer.writerows(lineups_for_upload)

        elif show_proj:
            with open("./dp_proj_lineups.csv", 'w') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(filled_lineups)


class Fanduel(DynamicProgrammingOptimizer):

    def _init__(self, num_lineups, overlap, solver, test=False):
        super().__init__(self, num_lineups, overlap, solver)
        self.salary_cap = 60000
        self.header = ['QB', 'RB', 'RB', 'WR', 'WR', 'WR', 'TE', 'FLEX', 'D']

    def no_stacking(self, lineups):

        prob = pulp.LpProblem('NFL', pulp.LpMaximize)

        # define qb, players, and dst variables
        qb_lineup = [pulp.LpVariable("quarterback_{}".format(i + 1), cat="Binary") for i in range(self.num_qbs)]
        skill_player_lineup = [pulp.LpVariable("player_{}".format(i + 1), cat="Binary") for i in
                               range(self.num_skill_players)]
        dst_lineup = [pulp.LpVariable("defense_{}".format(i + 1), cat="Binary") for i in range(self.num_dsts)]

        # define player constrains
        prob += (pulp.lpSum(qb_lineup[i] for i in range(self.num_qbs)) == 1)
        prob += (pulp.lpSum(skill_player_lineup[i] for i in range(self.num_skill_players)) == 7)
        prob += (pulp.lpSum(dst_lineup[i] for i in range(self.num_dsts)) == 1)

        # define position requirements
        prob += (pulp.lpSum(
            self.positions['RB'][i] * skill_player_lineup[i] for i in range(self.num_skill_players)) == 3)
        prob += (pulp.lpSum(
            self.positions['WR'][i] * skill_player_lineup[i] for i in range(self.num_skill_players)) == 3)
        prob += (pulp.lpSum(
            self.positions['TE'][i] * skill_player_lineup[i] for i in range(self.num_skill_players)) == 1)


        # add the salary constraint
        prob += ((pulp.lpSum(self.qb_df.loc[i, 'salary'] * qb_lineup[i] for i in range(self.num_qbs)) +
                  pulp.lpSum(self.skill_players_df.loc[i, 'salary'] * skill_player_lineup[i] for i in
                             range(self.num_skill_players)) + pulp.lpSum(self.dst_df.loc[i, 'salary'] * dst_lineup[i] for i in range(self.num_dsts))) <= self.salary_cap)

        # variance constraints - each lineup can't have more than the num overlap of any combination of players in any previous lineups
        for i in range(len(lineups)):
            prob += ((pulp.lpSum(lineups[i][k] * qb_lineup[k] for k in range(self.num_qbs)) +
                      pulp.lpSum(lineups[i][self.num_qbs + k] * skill_player_lineup[k] for k in
                                 range(self.num_skill_players)) +
                      pulp.lpSum(lineups[i][(self.num_qbs + self.num_skill_players) + k] *
                                 dst_lineup[k] for k in range(self.num_dsts))) <= self.overlap)

        # add the objective
        prob += pulp.lpSum(
            (pulp.lpSum(self.qb_df.loc[i, 'points'] * qb_lineup[i] for i in range(self.num_qbs)) +
             pulp.lpSum(
                 self.skill_players_df.loc[i, 'points'] * skill_player_lineup[i] for i in range(self.num_skill_players)) +
             pulp.lpSum(self.dst_df.loc[i, 'points'] * dst_lineup[i] for i in range(self.num_dsts))))

        # solve the problem
        status = prob.solve(self.solver)

        # check if the optimizer found an optimal solution
        if status != pulp.LpStatusOptimal:
            print('Only {} feasible lineups produced'.format(len(lineups)), '\n')
            return None

        # Puts the output of one lineup into a format that will be used later
        lineup_copy = []
        for i in range(self.num_qbs):
            if 0.9 <= qb_lineup[i].varValue <= 1.1:
                lineup_copy.append(1)
            else:
                lineup_copy.append(0)
        for i in range(self.num_skill_players):
            if 0.9 <= skill_player_lineup[i].varValue <= 1.1:
                lineup_copy.append(1)
            else:
                lineup_copy.append(0)
        for i in range(self.num_dsts):
            if 0.9 <= dst_lineup[i].varValue <= 1.1:
                lineup_copy.append(1)
            else:
                lineup_copy.append(0)
        return lineup_copy

    def type1(self, lineups):

        prob = pulp.LpProblem('NFL', pulp.LpMaximize)

        # define qb, players, and dst variables
        qb_lineup = [pulp.LpVariable("quarterback_{}".format(i + 1), cat="Binary") for i in range(self.num_qbs)]
        skill_player_lineup = [pulp.LpVariable("player_{}".format(i + 1), cat="Binary") for i in
                               range(self.num_skill_players)]
        dst_lineup = [pulp.LpVariable("defense_{}".format(i + 1), cat="Binary") for i in range(self.num_dsts)]

        # define player constrains
        prob += (pulp.lpSum(qb_lineup[i] for i in range(self.num_qbs)) == 1)
        prob += (pulp.lpSum(skill_player_lineup[i] for i in range(self.num_skill_players)) == 7)
        prob += (pulp.lpSum(dst_lineup[i] for i in range(self.num_dsts)) == 1)

        # define position requirements
        prob += (pulp.lpSum(
            self.positions['RB'][i] * skill_player_lineup[i] for i in range(self.num_skill_players)) == 3)
        prob += (pulp.lpSum(
            self.positions['WR'][i] * skill_player_lineup[i] for i in range(self.num_skill_players)) == 3)
        prob += (pulp.lpSum(
            self.positions['TE'][i] * skill_player_lineup[i] for i in range(self.num_skill_players)) == 1)

        # add the salary constraint
        prob += ((pulp.lpSum(self.qb_df.loc[i, 'Salary'] * qb_lineup[i] for i in range(self.num_qbs)) +
                  pulp.lpSum(self.skill_players_df.loc[i, 'Salary'] * skill_player_lineup[i] for i in
                             range(self.num_skill_players)) +
                  pulp.lpSum(
                      self.dst_df.loc[i, 'Salary'] * dst_lineup[i] for i in range(self.num_dsts))) <= self.salary_cap)

        # at least 3 teams for the 9 players
        used_team = [pulp.LpVariable("u{}".format(i + 1), cat="Binary") for i in range(self.num_teams)]
        for i in range(self.num_teams):
            prob += (used_team[i] <= (
                    pulp.lpSum(self.qb_teams[k][i] * qb_lineup[k] for k in range(self.num_qbs)) +
                    pulp.lpSum(
                        self.skill_player_teams[k][i] * skill_player_lineup[k] for k in range(self.num_skill_players)) +
                    pulp.lpSum(self.dst_teams[k][i] * dst_lineup[k] for k in range(self.num_dsts))))

        prob += (pulp.lpSum(used_team[i] for i in range(self.num_teams)) >= 3)

        # no qb's against dst constraint
        # for i in range(self.num_dsts):
        #     prob += (6 * dst_lineup[i] + pulp.lpSum(
        #         self.dst_opponents[k][i] * qb_lineup[k] for k in range(self.num_qbs)) <= 6)

        # no skill players against dst constraint
        # for i in range(self.num_dsts):
        #     prob += (6 * dst_lineup[i] + pulp.lpSum(
        #         self.dst_opponents[k][i] * skill_player_lineup[k] for k in range(self.num_skill_players)) <= 6)

        # variance constraints - each lineup can't have more than the num overlap of any combination of players in any previous lineups
        for i in range(len(lineups)):
            prob += ((pulp.lpSum(lineups[i][k] * qb_lineup[k] for k in range(self.num_qbs)) +
                      pulp.lpSum(lineups[i][self.num_qbs + k] * skill_player_lineup[k] for k in
                                 range(self.num_skill_players)) +
                      pulp.lpSum(lineups[i][(self.num_qbs + self.num_skill_players) + k] *
                                 dst_lineup[k] for k in range(self.num_dsts))) <= self.overlap)

        # add the objective
        prob += pulp.lpSum(
            (pulp.lpSum(self.qb_df.loc[i, 'FPPG'] * qb_lineup[i] for i in range(self.num_qbs)) +
             pulp.lpSum(
                 self.skill_players_df.loc[i, 'FPPG'] * skill_player_lineup[i] for i in range(self.num_skill_players)) +
             pulp.lpSum(self.dst_df.loc[i, 'FPPG'] * dst_lineup[i] for i in range(self.num_dsts))))

        # solve the problem
        status = prob.solve(self.solver)

        # check if the optimizer found an optimal solution
        if status != pulp.LpStatusOptimal:
            print('Only {} feasible lineups produced'.format(len(lineups)), '\n')
            return None

        # Puts the output of one lineup into a format that will be used later
        lineup_copy = []
        for i in range(self.num_qbs):
            if 0.9 <= qb_lineup[i].varValue <= 1.1:
                lineup_copy.append(1)
            else:
                lineup_copy.append(0)
        for i in range(self.num_skill_players):
            if 0.9 <= skill_player_lineup[i].varValue <= 1.1:
                lineup_copy.append(1)
            else:
                lineup_copy.append(0)
        for i in range(self.num_dsts):
            if 0.9 <= dst_lineup[i].varValue <= 1.1:
                lineup_copy.append(1)
            else:
                lineup_copy.append(0)
        return lineup_copy

    def type2(self, lineups):
        pass

    def type3(self, lineups):
        pass

    def type4(self, lineups):
        pass

    def type5(self, lineups):
        pass

    def fill_lineups(self, lineups):

        filled_lineups = []
        for lineup in lineups:
            a_lineup = ["", "", "", "", "", "", "", "", ""]
            qb_lineup = lineup[:self.num_qbs]
            skill_player_lineup = lineup[self.num_qbs: (self.num_skill_players + self.num_qbs)]
            dst_lineup = lineup[-1 * self.num_dsts:]
            total_proj = 0
            if self.actuals:
                total_actual = 0
            for num, qb in enumerate(qb_lineup):
                if 0.9 < qb < 1.1:
                    if a_lineup[0] == "":
                        a_lineup[0] = self.qb_df.loc[num, 'name']
                    total_proj += self.qb_df.loc[num, 'points']
                    if self.actuals:
                        total_actual += self.qb_df.loc[num, 'Actual']
            # a_lineup.append(round(total_proj, 2))
            # if self.actuals:
            #     a_lineup.append(round(total_actual, 2))
            for num, player in enumerate(skill_player_lineup):
                if 0.9 < player < 1.1:
                    if self.positions['RB'][num] == 1:
                        if a_lineup[1] == "":
                            a_lineup[1] = self.skill_players_df.loc[num, 'name']
                        elif a_lineup[2] == "":
                            a_lineup[2] = self.skill_players_df.loc[num, 'name']
                        elif a_lineup[6] == "":
                            a_lineup[6] = self.skill_players_df.loc[num, 'name']
                    elif self.positions['WR'][num] == 1:
                        if a_lineup[3] == "":
                            a_lineup[3] = self.skill_players_df.loc[num, 'name']
                        elif a_lineup[4] == "":
                            a_lineup[4] = self.skill_players_df.loc[num, 'name']
                        elif a_lineup[5] == "":
                            a_lineup[5] = self.skill_players_df.loc[num, 'name']
                    elif self.positions['TE'][num] == 1:
                        if a_lineup[7] == "":
                            a_lineup[7] = self.skill_players_df.loc[num, 'name']
                    total_proj += self.skill_players_df.loc[num, 'points']
                    if self.actuals:
                        total_actual += self.skill_players_df.loc[num, 'Actual']
            for num, dst in enumerate(dst_lineup):
                if 0.9 < dst < 1.1:
                    if a_lineup[8] == "":
                        a_lineup[8] = self.dst_df.loc[num, 'name']
                    total_proj += self.dst_df.loc[num, 'points']
                    if self.actuals:
                        total_actual += self.dst_df.loc[num, 'Actual']
            a_lineup.append(round(total_proj, 2))
            if self.actuals:
                a_lineup.append(round(total_actual, 2))
            filled_lineups.append(a_lineup)
        return filled_lineups


optimizer = Fanduel(num_lineups=10, overlap=7, solver=pulp.GUROBI(msg=0))
optimizer.create_indicators()
# generate the lineups with the formula and the indicators
lineups = optimizer.create_lineups(eqn=optimizer.no_stacking)
# fill the lineups with player names - send in the positions indicator
filled_lineups = optimizer.fill_lineups(lineups)
# save the lineups
optimizer.save(filled_lineups)
optimizer.save(filled_lineups, show_proj=True)


