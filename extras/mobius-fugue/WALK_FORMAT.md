# Walk format (for `tools/render_walk.py`)

A score that is meant to be heard while walking carries a `walk` block in
its `metadata`, and a `seat` for each voice.

```json
"metadata": {
  "walk": {
    "room": [10.0, 8.0],
    "rt60": 0.8,
    "wet": 0.06,
    "listener": [[0, 5.0, 1.5, 0], [8, 3.6, 4.2, -40], ...],
    "mirror": [[96, 192]]
  }
}
"voices": [{"name": "Violino I", "gm_program": 40, "seat": [3.0, 5.5], ...}, ...]
```

- **Coordinates** are metres in a rectangular room, `x` from 0 (left wall) to
  `room[0]` (right wall), `y` from 0 (entrance wall) to `room[1]` (far wall),
  as seen by someone standing at the entrance facing in. Ears are at the same
  height as the instruments (the walk is flat).
- **`seat`**: where each player sits (fixed for the whole piece).
- **`listener`**: keyframes `[t, x, y, facing]`, with `t` in quarter notes of
  score time (the same units as event `t`). `facing` is in degrees: 0 faces
  the far wall (+y), +90 faces the right wall (+x), -90 the left wall.
  Facing is *unwrapped*: going from 0 to 360 is one full turn to the right;
  from 0 to -10 is a small turn left. Between keyframes the renderer eases
  position and facing smoothly (slow start, slow stop). Two keyframes with the
  same position mean standing still.
- **`mirror`**: score-time intervals `[t_on, t_off]` during which the
  listener is mirror-reversed, as after one trip round a Möbius strip: every
  sound's left and right are exchanged relative to the listener (front, back
  and distance are unchanged). The switch is instantaneous, so put it where
  nothing is sounding (a general pause), or the trick shows.
- **`rt60`, `wet`**: the room's reverberation time (s) and late-reverb level.
  Defaults 0.8 s and 0.06: a small, fairly dry room, so the lines stay
  distinct. Four first-order wall reflections per player are always added;
  they move with the listener and carry most of the sense of the room.
- Voices play their `gm_program` (40 violin, 41 viola, 42 cello) unless the
  renderer is told otherwise.

Practical limits for a believable walk: at most about 1.2 m/s, turns of at
most about 90° per second (a deliberate pirouette can be faster), never
closer than 1 m to a player, never through a player.
