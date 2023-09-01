"""Compte Nash probabilities for single and dual type Pokemon.

Assumes that pokemon only have access to STAB moves.

TODO: Add support for arbitrary move combinations. Unfortunately, this
will blow up the number of pokemon to around 300K.
"""

import pandas as pd
import numpy as np
import pygambit

from nash import nash
import type_chart
from type_chart import symmetric_matchup_matrix, TYPES

single_types = [(t,) for t in TYPES]
single_type_matrix = symmetric_matchup_matrix(single_types)
single_type_nash = nash(single_type_matrix)

df = pd.DataFrame({'type': TYPES, 'nash': single_type_nash})
df.sort_values('nash', ascending=False, inplace=True)
print('Single type Nash probabilities:')
print(df)

dual_types = single_types + [(t1, t2) for t1 in TYPES for t2 in TYPES if t1 < t2]
dual_type_matrix = symmetric_matchup_matrix(dual_types)
dual_type_nash = nash(dual_type_matrix)
dual_type_names = ['/'.join(ts) for ts in dual_types]
df = pd.DataFrame({'type': dual_type_names, 'nash': dual_type_nash})
df.sort_values('nash', ascending=False, inplace=True)
print('\nDual type Nash probabilities (nonzero only):')
print(df[df['nash'] > 0])

single_attack_matrix = type_chart.asymmetric_matchup_matrix(
    single_types, dual_types).astype(pygambit.Decimal)
game = pygambit.Game.from_arrays(
    single_attack_matrix, -single_attack_matrix)
solutions = pygambit.nash.lcp_solve(game)
s = solutions[0]

attacker_nash = np.array(s[game.players[0]], dtype=float)
attacker_df = pd.DataFrame({'type': TYPES, 'nash': attacker_nash})
attacker_df.sort_values('nash', ascending=False, inplace=True)
print('\nSingle type attacker Nash probabilities:')
print(attacker_df)

defender_nash = np.array(s[game.players[1]], dtype=float)
defender_df = pd.DataFrame({'type': dual_type_names, 'nash': defender_nash})
defender_df.sort_values('nash', ascending=False, inplace=True)
print('\nDual type defender Nash probabilities (nonzero only):')
print(defender_df[defender_df['nash'] > 0])
