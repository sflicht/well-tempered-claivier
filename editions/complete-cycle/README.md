# Recovered complete-cycle editions

This directory restores the full 48-movement drafts that preceded the later
individual recompositions. The initial repository import omitted them; this
recovery preserves both whole-cycle editions alongside the newer work.

## Where the music is

- **Original first edition:** [baseline/scores](baseline/scores), 24 preludes
  and 24 fugues, preserved byte for byte.
- **Second working edition:** [scores](scores), another complete set of
  24 preludes and 24 fugues, preserved byte for byte.
- **Movement index:** [CYCLE_INDEX.md](../../CYCLE_INDEX.md), with direct links
  to every prelude and fugue in both editions.
- **Historical programs:** [tools](tools), all 38 Python source files from
  the recovered archive. These are kept separate from current root tools.
- **Original documentation:** [README.txt](README.txt) and
  [cycle-manifest.json](cycle-manifest.json), unchanged historical records.

The exact recovered [complete source ZIP](../../archive/well-tempered-clAIvier-complete-source.zip)
contains all **466 original files**, including both editions' JSON scores,
canonical and intermediate revision sources, audits, and the second edition's
48 MIDI, 48 MusicXML, 48 LilyPond and 48 individual PDF score exports, plus
the cycle-guide PDF. These notation and MIDI exports are preserved inside
the ZIP; the editable JSON scores and source programs are also browsable here.
The ZIP does not contain the separately delivered full-cycle audio or videos.

## Provenance and verification

The archive describes itself as **Second working edition — 2026-10-23** and
identifies `baseline/scores` as the unchanged first-edition baseline.
It was recovered from the previously delivered
`well-tempered-clAIvier-complete-source.zip`, version 1.

- Archive size: **9,876,750 bytes**.
- SHA256: `6e3312c1c4c11fe98b921f0b637f4daebe2e75c56a01e97165fa433c9135fde6`.
- ZIP integrity and member paths checked; 466 files, 83,625,133 unpacked bytes.
- Each edition contains exactly 24 preludes and 24 fugues, numbered I–XXIV.
- Every fugue has N+1 written part streams (2–25).
- All 96 score hashes match the preserved cycle manifest.
- All 48 second-edition score copies match the archive's canonical `work/cycle_*` files.
- Event counts: 27,089 in the first edition; 50,619 in the second.

[archive-inventory.json](archive-inventory.json) records every original member's
size and SHA256. The hashes establish preservation, not musical success.

## Relation to current revisions

These are **historical complete drafts**. Subsequent listener feedback rejected
the earlier fugues' lack of independent counterpoint, rhythmic vitality,
distinct character and convincing cumulative form. Historical favorable
language and automated audits must be read in that context. A count of
25 part streams does not establish 25-part counterpoint.

The later replacement Fugue I, Prelude IV, nine-voice study and Fugue VIII
remain under the repository's root `work/` directories. In particular, the
recovered cycle's Fugue VIII, “A narrow stair” (quarter = 86), is distinct from
the later “The procession finds a dance floor” (quarter = 108). Restoring this
archive does not replace the current revision.

## Rendering or running the historical workflow

For the complete original directory structure, extract the ZIP to a separate
working directory and use its frozen JSON scores. Historical generators alone
do not reproduce the second edition; the archived revision files are required.

```bash
python3 -m zipfile -e archive/well-tempered-clAIvier-complete-source.zip recovered-full-cycle
cd recovered-full-cycle
python3 tools/render_music.py --help
python3 tools/animate_cycle.py --help
```

The original workflow used Python 3.12 with mido, numpy, scipy, pyfluidsynth,
ortools, Pillow, reportlab and pypdf, plus LilyPond, FFmpeg, Poppler and a
General MIDI soundfont. Third-party dependencies and the soundfont are not
included. See the original README for the historical rendering details.
