"""Print the literal token strings of every planned rung (leader + follower)."""
from realize import statement, placed, tokens, head_ok
from ladder import pair_cost
# (rung d8, key, leader octave, follower form, follower shift, follower octave, leader voice)
RUNGS = [
    (8, 'G', 0, 'rectus', -6, -1, 'upper'),     # 7th below (+octave): E3
    (7, 'e', 0, 'rectus', -9, 0, 'upper'),      # 10th below: G3
    (6, 'a', -1, 'inversus', 3, -1, 'upper'),   # inversion (in G/e) below
    (5, 'd', 0, 'rectus', -11, 0, 'upper'),     # 12th below
    (4, 'F', -2, 'rectus', 8, -2, 'lower'),     # 9th above, bass leads
    (3, 'C', 0, 'rectus', -7, 0, 'upper'),      # octave below
    (2, 'G', 0, 'inversus', 2, -1, 'upper'),    # inversion (in e) below
    (1, 'C', 0, 'inversus', 7, 0, 'upper'),     # mirror, a step below
]
if __name__ == '__main__':
    for d8, key, lo, ff, fs, fo, lv in RUNGS:
        L = statement(key, 'rectus', 0, lo)
        F = statement(key, ff, fs, fo)
        c, w = pair_cost(placed(L, 14), placed(F, 14 + 2 * d8), True)
        print(f'R{d8} {key} lead={lv} cost {c:.1f} head_ok {head_ok(L)} {head_ok(F)}  {w}')
        print('   L:', tokens(L)); print('   F:', tokens(F))
