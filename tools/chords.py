"""Tiny chord-naming helpers shared by the critic and the reduction printer."""
NAMES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NAMES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
TEMPLATES = {
    '': (0, 4, 7), 'm': (0, 3, 7), 'o': (0, 3, 6), '+': (0, 4, 8),
    '7': (0, 4, 7, 10), 'm7': (0, 3, 7, 10), 'ø7': (0, 3, 6, 10), 'o7': (0, 3, 6, 9),
    'maj7': (0, 4, 7, 11), '7(no5)': (0, 4, 10), 'm(no5)7': (0, 3, 10),
}
# Preference order when several templates fit.
ORDER = ['', 'm', '7', 'o7', 'ø7', 'm7', 'o', 'maj7', '7(no5)', 'm(no5)7', '+']
# Semitones from the root to the note that must resolve down (the chord seventh).  A diminished
# triad ('o') counts as a rootless dominant seventh: B-D-F is G7 without its G, and its seventh is
# F, the diminished fifth above the triad's root, whichever of the three is in the bass.
SEVENTH = {'7': 10, 'm7': 10, 'ø7': 10, 'o7': 9, 'maj7': 11, '7(no5)': 10, 'm(no5)7': 10, 'o': 6}
# A missing chord member costs more than the bass bonus (3) plus any gap in ORDER, so a complete
# triad is never read as an incomplete seventh chord on the bass: B-D-F over D is B diminished
# (a rootless G7), not D-F-Ab-B with the leading tone B as its "seventh".
MISSING = 7
INTERVALS = ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'TT', 'P5', 'm6', 'M6', 'm7', 'M7']


def pname(p, flats=False):
    names = NAMES_FLAT if flats else NAMES_SHARP
    return f"{names[p % 12]}{p // 12 - 1}"


def chord_candidates(pcs, bass_pc=None):
    """All (root, quality) whose template contains every pitch class in pcs."""
    pcs = set(pcs)
    out = []
    for q in ORDER:
        t = TEMPLATES[q]
        for r in range(12):
            cs = {(r + x) % 12 for x in t}
            if pcs <= cs and len(pcs) >= min(3, len(cs)):
                # missing chord members weigh heavily, so an incomplete seventh chord
                # (e.g. B-D-F) is read as the triad it sounds like, not a rootless 7th
                score = ORDER.index(q) + (0 if bass_pc == r else 3) + MISSING * (len(cs) - len(pcs))
                out.append((score, r, q))
    out.sort()
    return [(r, q) for _, r, q in out]


def name_chord(pcs, bass_pc=None, flats=False):
    names = NAMES_FLAT if flats else NAMES_SHARP
    c = chord_candidates(pcs, bass_pc)
    if not c:
        return None
    r, q = c[0]
    s = names[r] + q
    if bass_pc is not None and bass_pc != r:
        s += '/' + names[bass_pc]
    return s


def name_dyad(pcs, bass_pc=None, flats=False):
    """Interval label for a sonority of two pitch classes, e.g. 'C-E (M3)', measured up from the
    bass's pitch class (one pitch class: 'C (P1)').  Two pitch classes do not determine a chord,
    so no chord name is claimed."""
    names = NAMES_FLAT if flats else NAMES_SHARP
    if len(set(pcs)) == 1:
        return f"{names[next(iter(pcs)) % 12]} (P1)"
    a, b = sorted(set(pcs))
    if bass_pc == b:
        a, b = b, a
    return f"{names[a]}-{names[b]} ({INTERVALS[(b - a) % 12]})"
