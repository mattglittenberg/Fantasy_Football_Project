from nfldfs import games as games

# Pull fantasy points data for various seasons and week on different daily fantasy platforms

site = input('Select dfs site:')
first_season = input('Select starting season:')
first_week = input('Select starting week:')
last_season = input ('Select ending season:')
last_week = input('Select ending week:')

dfg = games.find_games(dfs_site=site, season_from=first_season, week_from=first_week,
                       season_to=last_season, week_to=last_week)
stats = games.get_game_data(dfg)

if site == 'fd':
    stats.to_csv(r'C:\Users\mattg\PycharmProjects\Fantasy_Football\stats_fd.csv', index=False, header=True)
if site == 'dk':
    stats.to_csv(r'C:\Users\mattg\PycharmProjects\Fantasy_Football\stats_dk.csv', index=False, header=True)
if site == 'yh':
    stats.to_csv(r'C:\Users\mattg\PycharmProjects\Fantasy_Football\stats_yh.csv', index=False, header=True)
