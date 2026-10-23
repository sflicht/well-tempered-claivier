# Fugue VIII: shorter revision in progress

These files checkpoint an incomplete revision. The current delivered audition
remains `../fugue_viii_passage_revision/08-fugue-passage-revised.json`.
The new full piece has not been assembled, rendered or auditioned.

| Component | Intended global beats | Source | Status |
| --- | --- | --- | --- |
| Opening and retained retort passage | 0–112, clarinet tail to 116 | `opening.json`, `build_opening.py` | Composed and symbolically checked |
| Tonal episode | 112–144 | `tonal-episode.json`, `compose_tonal_episode.py` | Composed; clarinet at local 0–4 deliberately supplied by opening tail |
| Return | 144–176 | `return.json`, `build_return.py` | Composed and symbolically checked |
| Culmination and close | 176–240 | Not yet written | Outstanding |

The goal is a 60-bar piano-led form. The component files contain local
metadata and timing; do not concatenate them without checking joins, the
carried clarinet phrase, thematic annotations and the eventual new ending.
Written checks do not establish audible success or strict historical
counterpoint. Review notes record the remaining musical limitations.

`../../tools/shape_fugue_viii_piano.py` is a separate performance helper that
changes velocity and gate only. Its demonstration output is not an adopted
edition and is excluded from the repository.
