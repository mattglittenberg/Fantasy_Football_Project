import pandas as pd
from scipy.stats import shapiro


# TODO: Add DK and Yahoo functionality
class Projections:
    def __init__(self):
        self.source = input("Which site would you like projections for?")
        self.qb_dict = {}
        self.rb_dict = {}
        self.wr_dict = {}
        self.te_dict = {}
        self.dst_dict = {}
        self.qb_roster = None
        self.rb_roster = None
        self.wr_roster = None
        self.te_roster = None
        self.dst_roster = None
        self.final_roster = None
        self.load_stats_data()
        self.load_proj_data()
        self.add_data()

    def load_stats_data(self):
        if self.source == 'fd':
            stats_data = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/daily_ffb/sub_stats_fd.csv')
        elif self.source == 'dk':
            stats_data = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/daily_ffb/sub_stats_dk.csv')
        elif self.source == 'yh':
            stats_data = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/daily_ffb/sub_stats_yh.csv')
        else:
            print('Not valid projection site')

        qb_df = stats_data[(stats_data['position'] == 'QB')]
        qb_df.reset_index(inplace=True)
        rb_df = stats_data[(stats_data['position'] == 'RB')]
        rb_df.reset_index(inplace=True)
        wr_df = stats_data[(stats_data['position'] == 'WR')]
        wr_df.reset_index(inplace=True)
        te_df = stats_data[(stats_data['position'] == 'TE')]
        te_df.reset_index(inplace=True)
        dst_df = stats_data[(stats_data['position'] == 'Def')]
        dst_df.reset_index(inplace=True)

        # QB
        qb_mean = qb_df.groupby('salary')['points'].mean().round(2)
        qb_median = qb_df.groupby('salary')['points'].median().round(2)
        qb_stats = pd.merge(qb_mean, qb_median, on='salary')
        qb_stats.rename(columns={'points_x': 'mean', 'points_y': 'median'}, inplace=True)
        self.qb_dict = qb_stats.to_dict()

        # RB
        rb_mean = rb_df.groupby('salary')['points'].mean().round(2)
        rb_median = rb_df.groupby('salary')['points'].median().round(2)
        rb_stats = pd.merge(rb_mean, rb_median, on='salary')
        rb_stats.rename(columns={'points_x': 'mean', 'points_y': 'median'}, inplace=True)
        self.rb_dict = rb_stats.to_dict()

        # WR
        wr_mean = wr_df.groupby('salary')['points'].mean().round(2)
        wr_median = wr_df.groupby('salary')['points'].median().round()
        wr_stats = pd.merge(wr_mean, wr_median, on='salary')
        wr_stats.rename(columns={'points_x': 'mean', 'points_y': 'median'}, inplace=True)
        self.wr_dict = wr_stats.to_dict()

        # TE
        te_mean = te_df.groupby('salary')['points'].mean().round(2)
        te_median = te_df.groupby('salary')['points'].median().round(2)
        te_stats = pd.merge(te_mean, te_median, on='salary')
        te_stats.rename(columns={'points_x': 'mean', 'points_y': 'median'}, inplace=True)
        self.te_dict = te_stats.to_dict()

        # DST
        dst_mean = dst_df.groupby('salary')['points'].mean().round(2)
        dst_median = dst_df.groupby('salary')['points'].median().round(2)
        dst_stats = pd.merge(dst_mean, dst_median, on='salary')
        dst_stats.rename(columns={'points_x': 'mean', 'points_y': 'median'}, inplace=True)
        self.dst_dict = dst_stats.to_dict()

    def load_proj_data(self):
        proj_data = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/daily_ffb/projections_week13.csv')
        proj_data = proj_data[
            (proj_data['avg_type'] == 'robust') & (proj_data['team'] != 'FA') & (proj_data['points'] > 0)]
        proj_data['name'] = proj_data['first_name'].astype(str) + ' ' + proj_data['last_name'].astype(str)
        name = proj_data.pop('name')
        proj_data.insert(0, 'name', name)
        proj_data.name.replace({'Mark Ingram': 'Mark Ingram II', 'Marvin Jones': 'Marvin Jones Jr',
                                'Odell Beckham': 'Odell Beckham Jr.', 'Allen Robinson': 'Allen Robinson II',
                                'Willie Snead': 'Willie Snead IV', 'Melvin Gordon': 'Melvin Gordon III',
                                'Todd Gurley': 'Todd Gurley II', 'Phillip Dorsett': 'Phillip Dorsett II',
                                'Will Fuller': 'Will Fuller V', 'Wayne Gallman': 'Wayne Gallman Jr.',
                                'Steven Sims': 'Steven Sims Jr.', 'Benny Snell': 'Benny Snell Jr.',
                                'Gardner Minshew': 'Gardner Minshew II', 'Dwayne Haskins': 'Dwayne Haskins Jr.',
                                'Jeff Wilson': 'Jeff Wilson Jr.', 'Richie James': 'Richie James Jr.',
                                'DJ Chark': 'DJ Chark Jr.', 'Steven Mitchell': 'Steven Mitchell Jr.',
                                'D.J. Moore': 'DJ Moore', 'Ronald Jones': 'Ronald Jones II',
                                'Alexander Armah': 'Alex Armah'})
        proj_data.drop(['id', 'first_name', 'last_name', 'age', 'exp', 'pos', 'avg_type', 'tier'], axis=1, inplace=True)
        if self.source == 'fd':
            fd_roster = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/daily_ffb/FanDuel_NFL_players.csv')
            fd_roster.rename(columns={'Nickname': 'name'}, inplace=True)
            roster = fd_roster.drop(fd_roster.columns.difference(['name', 'Salary']), axis=1)
        if self.source == 'dk':
            pass
            # FIXME: ADD DK ROSTER
        if self.source == 'yh':
            pass
            # FIXME: ADD YH ROSTER

        merged_roster = pd.merge(proj_data, roster, on='name')
        merged_roster.rename(columns={'Salary': 'salary'}, inplace=True)

        self.qb_roster = merged_roster[merged_roster['position'] == 'QB']
        self.rb_roster = merged_roster[merged_roster['position'] == 'RB']
        self.wr_roster = merged_roster[merged_roster['position'] == 'WR']
        self.te_roster = merged_roster[merged_roster['position'] == 'TE']
        self.dst_roster = merged_roster[merged_roster['position'] == 'DST']

    def add_data(self):

        def normal_test(roster):
            norm_dict = {}
            group = roster.groupby('salary')['points']
            for sal_pt, g in group:
                if len(g) < 3:
                    norm_dict.update({sal_pt: 'median'})
                else:
                    stat, p = shapiro(g)
                    if p > 0.05:
                        norm_dict.update({sal_pt: 'mean'})
                    else:
                        norm_dict.update({sal_pt: 'median'})
            return norm_dict

        def insert_avg(roster, dic, norm_dict):

            roster['avg_type'] = roster['salary'].map(norm_dict)
            for i, row in roster.iterrows():
                if row['avg_type'] == 'mean':
                    roster.at[i, 'avg'] = dic['mean'][row['salary']]
                elif row['avg_type'] == 'median':
                    roster.at[i, 'avg'] = dic['median'][row['salary']]

            return roster

        qb_norm = normal_test(self.qb_roster)
        self.qb_roster = insert_avg(self.qb_roster, self.qb_dict, qb_norm)

        rb_norm = normal_test(self.rb_roster)
        self.rb_roster = insert_avg(self.rb_roster, self.rb_dict, rb_norm)

        wr_norm = normal_test(self.wr_roster)
        self.wr_roster = insert_avg(self.wr_roster, self.wr_dict, wr_norm)

        te_norm = normal_test(self.te_roster)
        self.te_roster = insert_avg(self.te_roster, self.te_dict, te_norm)

        dst_norm = normal_test(self.dst_roster)
        self.dst_roster = insert_avg(self.dst_roster, self.dst_dict, dst_norm)

    def run_calc(self):

        def calc_value(pos_roster):
            pos_roster['value'] = pos_roster.apply(lambda row: row.points - row.avg, axis=1)

            return pos_roster

        # for player in roster, get value from stats based on salary, subtract mean/median from proj

        roster_list = [self.qb_roster, self.rb_roster, self.wr_roster, self.te_roster, self.dst_roster]
        final_roster_list = [calc_value(roster) for roster in roster_list]
        self.final_roster = pd.concat(final_roster_list)
        self.final_roster.reset_index(inplace=True)

    def save_proj(self):
        if self.source == 'fd':
            self.final_roster.to_csv(r'C:\Users\mattg\PycharmProjects\Fantasy_Football\daily_ffb\final_roster_fd.csv',
                                     index=False, header=True)
        if self.source == 'dk':
            self.final_roster.to_csv(r'C:\Users\mattg\PycharmProjects\Fantasy_Football\daily_ffb\final_roster_dk.csv',
                                     index=False, header=True)
        if self.source == 'yh':
            self.final_roster.to_csv(r'C:\Users\mattg\PycharmProjects\Fantasy_Football\daily_ffb\final_roster_yh.csv',
                                     index=False, header=True)


dfp = Projections()
dfp.run_calc()
# dfp.save_proj()
