"""Fugue XXI, the departure ("La partenza"), bars 50-66.

b50-54  Farewell.  Over the fundamental and its octave (Corni 1 and 2 hold B-flat from the
        summit's last chord to the end) the friends sing their theme twice in the two-voice
        texture of Bach's Arioso (in sixths): Amico 10 with Amico 15, then Amico 20 with Amico 5.
        Between the phrases the horns answer with the Aria's octave call, each further away.
b55-62  The relay.  Each voice in turn takes over the note of the voice below it, tongues it in
        the posthorn rhythm, and steps up to its own partial, where it stays: partial 3, 4, 5 ...
        22, slowly at first (two beats apart), then a beat apart -- the subject's rocket, played by
        the whole company up the whole series.  Every note from b55 on is a partial of B-flat1
        and is tuned as one (just intonation, see NOTES.md); the cracked notes of section C are
        now simply where they belong.
b62-66  The chord of the first twenty-two partials.  Far away, the first postilion (Corno 4,
        who began the fugue) blows the head of the subject once more and returns to his partial.
"""
from xxi import *  # noqa

# partial n's written pitch
PN = {n: PARTIAL_NOTE[n].replace('Cb6', 'B5') for n in PARTIAL_NOTE}
ORDER = list(range(3, 23))
# arrival beat of partial n, counted in beats from the start of bar b55 (0-based)
ARRIVE = {}
for k, n in enumerate(ORDER[:8]):          # partials 3-10: two beats apart
    ARRIVE[n] = 2 * k
for k, n in enumerate(ORDER[8:]):          # partials 11-22: one beat apart
    ARRIVE[n] = 16 + k
END_BAR = 66


def place(sc, b0=50):
    b = lambda k: b0 + k - 1  # noqa: E731   (b(1) = bar 50)
    # ---- the fundamental and its octave hold from the last chord of the summit
    sc.put(V(1), b(2), 1, f"Bb1:{16 * (END_BAR - 51 + 1)}")
    sc.put(V(2), b(1), 3, f"Bb2:{8 + 16 * (END_BAR - 51 + 1)}")
    # ---- farewell: the friends' theme in Bach's Arioso texture (sixths), twice
    sc.theme(V(10), b(1), 3, T, 'T (farewell)', 2)
    sc.put(V(15), b(1), 3, "R:2 D4:1 Eb4:1 F4:2 Eb4:1 D4:1 C4:2 D4:1 Eb4:1 F4:1 G4:1 A4:1 Bb4:1 "
           "Bb4:4 A4:2 G4:2 F4:3 Eb4:1 D4:4")
    sc.theme(V(20), b(3), 3, octv(T, 1), 'T (farewell, an octave higher)', 2)
    sc.put(V(5), b(3), 3, "R:2 D4:1 Eb4:1 F4:2 Eb4:1 D4:1 C4:2 D4:1 Eb4:1 F4:1 G4:1 A4:1 Bb4:1 "
           "Bb4:4 A4:2 G4:2 F4:3 Eb4:1 D4:4")
    # the horns' answers, each further away
    sc.put(V(16), b(2), 3, "Bb4:2 Bb5:1 Bb4:1")
    sc.put(V(8), b(4), 3, "Bb4:2 Bb5:1 Bb4:1")
    sc.put(V(22), b(5), 3, "F5:2 F6:1 F5:1")
    # ---- the relay up the series
    total = (END_BAR - 55 + 1) * 4          # beats from b55.1 to the end
    for n in ORDER:
        a = ARRIVE[n]                       # it tongues the note below on beat a, arrives on a + 1
        bar, beat = 55 + a // 4, a % 4 + 1
        lower = PN[n - 1] if n != 8 else PN[6]     # (Corno 8 takes F, not the seventh)
        # it takes the note below, turns round its own note once, and stays
        toks = f"{lower}:2 {PN[n]}:1 {lower}:1 {PN[n]}:{4 * (total - a - 1)}"
        if n == 4:
            # the first postilion leaves his partial for the last call (b64-65) and returns to it
            call = "Bb3:4 R:2 Bb3:1 Bb3:1 F4:2 F4:2 F4:2 F4:2 D4:2 Bb3:2 Bb3:2 Bb3:1 Bb3:1"
            pre = (64 - 55) * 4 - a - 1
            post = total - (64 - 55) * 4 - 6
            toks = f"{lower}:2 {PN[n]}:1 {lower}:1 {PN[n]}:{4 * pre} {call} Bb3:{4 * post}"
        sc.put(V(n), bar, beat, toks)
