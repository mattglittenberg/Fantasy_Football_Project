import pandas as pd


# player_load
# ==========================================
# Purpose: read in data files from https://www.fantasypros.com/nfl/projections/___.php?week=draft to data frames
# Input Parameter(s): None
# Return Value: list of position data frames created from csv files
# ==========================================
def player_load():
    qb_data = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/test_projections/Football_Projections_QB.csv')
    qb_data.insert(2, 'POS', 'QB')

    rb_data = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/test_projections/Football_Projections_RB.csv')
    rb_data.insert(2, 'POS', 'RB')

    wr_data = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/test_projections/Football_Projections_WR.csv')
    wr_data.insert(2, 'POS', 'WR')

    te_data = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/test_projections/Football_Projections_TE.csv')
    te_data.insert(2, 'POS', 'TE')

    dst_data = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/test_projections/Football_Projections_DST.csv')
    dst_data.insert(1, 'POS', 'D/ST')

    k_data = pd.read_csv('C:/Users/mattg/PycharmProjects/Fantasy_Football/test_projections/Football_Projections_K.csv')
    k_data.insert(2, 'POS', 'K')

    return [qb_data, rb_data, wr_data, te_data, dst_data, k_data]


# clean_data
# ==========================================
# Purpose: Cleans data from csv files by:
#          - removes fantasy points column
#          - removes team column from D/ST
#          - removes NaN values
#          - renames columns
#          - removes commas from high yardage columns and change to float type
# Input Parameter(s): position_list - list of raw position data frames
# Return Value: position_list - list of cleaned position data frames
# ==========================================
def clean_data(position_list):
    for pos in position_list:
        pos.drop('FPTS', axis=1, inplace=True)
        if pos['Team'].isnull().all():
            pos.drop('Team', axis=1, inplace=True)
        else:
            pos.dropna(inplace=True)
        if pos['POS'].all() == 'QB':
            pos.rename(columns={'ATT': 'PASS_ATT', 'YDS': 'PASS_YDS', 'TDS': 'PASS_TDS',
                                'ATT.1': 'RUSH_ATT', 'YDS.1': 'RUSH_YDS', 'TDS.1': 'RUSH_TDS'}, inplace=True)
            pos['PASS_YDS'] = pos['PASS_YDS'].str.replace(',', "").astype('float')

        if pos['POS'].all() == 'RB':
            pos.rename(columns={'ATT': 'RUSH_ATT', 'YDS': 'RUSH_YDS', 'TDS': 'RUSH_TDS',
                                'YDS.1': 'REC_YDS', 'TDS.1': 'REC_TDS'}, inplace=True)
            pos['RUSH_YDS'] = pos['RUSH_YDS'].str.replace(',', "").astype('float')
        if pos['POS'].all() == 'WR':
            pos.rename(columns={'YDS': 'REC_YDS', 'TDS': 'REC_TDS', 'ATT': 'RUSH_ATT',
                                'YDS.1': 'RUSH_YDS', 'TDS.1': 'RUSH_TDS'}, inplace=True)
            pos['REC_YDS'] = pos['REC_YDS'].str.replace(',', "").astype('float')
        if pos['POS'].all() == 'TE':
            pos.rename(columns={'YDS': 'REC_YDS', 'TDS': 'REC_TDS'}, inplace=True)
            pos['REC_YDS'] = pos['REC_YDS'].str.replace(',', "").astype('float')
        if pos['POS'].all() == 'D/ST':
            pos.rename(columns={'TD': 'DEF_TDS'}, inplace=True)
            pos['YDS_AGN'] = pos['YDS_AGN'].str.replace(',', "").astype('float')
    return position_list


# projection_calc
# ==========================================
# Purpose: Calculates total fantasy points for given league scoring settings
# Input Parameter(s): position_list - list of position data frames without fantasy points calculated
#                     passing - dictionary of passing score settings
#                     rush - dictionary of rushing score settings
#                     rec - dictionary of receiving score settings
#                     kick - dictionary of kicking score settings
#                     dst - dictionary of defense/special teams score settings
# Return Value: position_list - list of position data frames with fantasy points calculated
# ==========================================
def projection_calc(position_list, passing, rush, rec, kick, dst):
    for pos in position_list:
        for index, row in pos.iterrows():
            if pos['POS'].all() == 'QB':
                pass_pts = ((float(row.PASS_YDS) * passing.get('pass_yds')) + (
                            float(row.CMP) / passing.get('completions'))
                            + (float(row.PASS_TDS) * passing.get('pass_tds')))
                rush_pts = (float(row.RUSH_YDS) * rush.get('rush_yds')) + (float(row.RUSH_TDS) * rush.get('rush_tds'))
                total = (pass_pts + rush_pts) - float(row.FL * rush.get('fl_lost'))
                pos.at[index, 'FPTS'] = total
            elif pos['POS'].all() == 'RB':
                rush_pts = (float(row.RUSH_YDS) * rush.get('rush_yds')) + (float(row.RUSH_TDS) * rush.get('rush_tds'))
                rec_pts = (float(row.REC_YDS) * rec.get('rec_yds')) + (float(row.REC_TDS) * rec.get('rec_tds'))
                total = (rush_pts + rec_pts) - float(row.FL * rush.get('fl_lost'))
                pos.at[index, 'FPTS'] = total
            elif pos['POS'].all() == 'WR':
                rush_pts = (float(row.RUSH_YDS) * rush.get('rush_yds')) + (float(row.RUSH_TDS) * rush.get('rush_tds'))
                rec_pts = (float(row.REC_YDS) * rec.get('rec_yds')) + (float(row.REC_TDS) * rec.get('rec_tds'))
                total = (rush_pts + rec_pts) - float(row.FL * rush.get('fl_lost'))
                pos.at[index, 'FPTS'] = total
            elif pos['POS'].all() == 'TE':
                rush_pts = (float(row.RUSH_YDS) * rush.get('rush_yds')) + (float(row.RUSH_TDS) * rush.get('rush_tds'))
                rec_pts = (float(row.REC_YDS) * rec.get('rec_yds')) + (float(row.REC_TDS) * rec.get('rec_tds'))
                total = (rush_pts + rec_pts) - float(row.FL * rush.get('fl_lost'))
                pos.at[index, 'FPTS'] = total
            elif pos['POS'].all() == 'D/ST':
                total = ((float(row.SACK) * dst.get('sack')) + (float(row.INT) * dst.get('int')) +
                         (float(row.FR) * dst.get('fr')) + (float(row.FF) * dst.get('ff')) +
                         (float(row.DEF_TDS) * dst.get('def_tds')) + (float(row.SAFETY) * dst.get('safety')))
                pos.at[index, 'FPTS'] = total
            elif pos['POS'].all() == 'K':
                total = ((float(row.FG) * kick.get('fg_made')) + (float(row.XPT) * kick.get('pat_made'))
                         - ((float(row.FGA) - float(row.FG)) * kick.get('fg_missed')))
                pos.at[index, 'FPTS'] = total
    return position_list
