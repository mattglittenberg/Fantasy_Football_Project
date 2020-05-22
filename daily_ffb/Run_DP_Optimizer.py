import pulp
from nfl_dp_optimizer import Fanduel

optimizer = Fanduel(num_lineups=10, overlap=4, solver=pulp.CPLEX_PY(msg=0))
optimizer.create_indicators()
# generate the lineups with the formula and the indicators
lineups = optimizer.create_lineups(eqn=optimizer.no_stacking)
# fill the lineups with player names - send in the positions indicator
filled_lineups = optimizer.fill_lineups(lineups)
# save the lineups
optimizer.save(filled_lineups)
optimizer.save(filled_lineups, show_proj=True)
