#!/usr/bin/env python3
"""Build the listening app: a static site that plays every render of the cycle.

    python3 tools/build_app.py                    # build _site/ with copies of the media (for Pages)
    python3 tools/build_app.py --link             # symlink the media instead (local use, no copies)
    python3 -m http.server -d _site 8000          # then open http://localhost:8000/
    python3 tools/build_app.py --strips           # first (re)engrave missing or stale score strips
    python3 tools/build_app.py --strips-only      # only engrave the strips (needs LilyPond)
    python3 tools/build_app.py --exclude-archive  # leave out the earlier versions' media (~312 MB)

What it writes (default output folder _site/, git-ignored):
  index.html, app.js, styles.css   the app (copied from app/; no build step)
  catalog.json                     groups, pieces, notes, voice counts, durations and, for each
                                   piece, every rendered file with a human label
  scores/<id>.json                 compact score for the in-browser synth and the piano roll (the
                                   same compaction as tools/build_listening_page.py); <id>-earlier
                                   for the earlier version of a recomposed fugue
  strips/<id>.json, strips/<id>/   the engraved score strip cut into tiles, with its time_to_x map
  media/<repo path>                the renders, notes and guide, copied (or symlinked with --link)

Score strips are engraved once by tools/score_strip.py and committed next to the renders, at
cycle/NN-key/renders/strip-<piece>/strip.png + strip.json (the Möbius extra keeps its own
renders/strip/).  --strips regenerates only those whose score changed since they were made.

The site must stay under GitHub Pages' 1 GB limit; the build reports its size and fails (in copy
mode) if it is larger.  Only the standard library is needed, plus Pillow to cut the strip tiles.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import render_music as rm  # noqa: E402
from build_listening_page import compact  # noqa: E402
from fractions import Fraction  # noqa: E402

MANIFEST = ROOT / 'cycle' / 'listening-manifest.json'
GUIDE = 'cycle/LISTENING_GUIDE.md'
APP_DIR = ROOT / 'app'
APP_FILES = ['index.html', 'app.js', 'styles.css']
REPO_URL = 'https://github.com/sflicht/well-tempered-claivier'
PAGES_LIMIT = 1_000_000_000          # GitHub Pages: a published site may be at most 1 GB
TEMPERAMENTS = ['equal', 'bach-lehman', 'werckmeister3', 'kirnberger3', 'vallotti', 'meantone']

# Score strips: a fixed staff space, and a quarter note about STRIP_QUARTER_SS staff spaces wide
# (the shortest gap between onsets gets between GAP_MIN and GAP_MAX staff spaces).
STRIP_STAFF_SPACE_PX = 10.0
STRIP_QUARTER_SS = 12.0
GAP_MIN, GAP_MAX = 1.6, 3.0
TILE_PIXELS = 4_000_000              # strip tiles of about 4 megapixels, 1024..4096 px wide

ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV',
         'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV']

# The score a strip is engraved from, where it is not the piece's own score (Prelude I is played
# as Shepard layers from prelude.json; its notation is prelude-notation.json, same time axis).
STRIP_SOURCE = {'prelude-1': 'cycle/01-c-major/prelude-notation.json'}
# Strips that already exist elsewhere and are reused as they are.
EXISTING_STRIPS = {'mobius': 'extras/mobius-fugue/renders/strip'}

AUDIO_LABELS = {
    '': ('Piano, Bach-Lehman', 'piano'),
    'equal': ('Piano, equal temperament', 'equal'),
    'meantone': ('Meantone', 'meantone'),
    'violin': ('Violin', 'violin'),
    'spatial': ('Binaural (headphones)', 'binaural'),
    'spatial-choir': ('Binaural, choir', 'binaural-choir'),
    'spatial-strings': ('Binaural, strings', 'binaural-strings'),
    'spatial-instruments': ('Binaural, instruments', 'binaural-instruments'),
    'spatial-concertino': ('Binaural, concertino', 'binaural-concertino'),
    'walk': ('Walking (binaural)', 'walk'),
}
LABEL_OVERRIDES = {
    'cycle/09-e-major/renders/prelude.mp3': ('Piano, just intonation', 'piano'),
    'extras/mobius-fugue/renders/fugue.mp3': ('Strings, Bach-Lehman (stereo)', 'stereo'),
}
# Short excerpts: which piece, and where in the score (quarters) they start and end.
EXCERPTS = {
    'cycle/23-b-major/renders/meantone-demo-bach-lehman.mp3':
        {'piece': 'fugue-23', 'label': 'Excerpt b66–72, Bach-Lehman', 'kind': 'excerpt-bach-lehman',
         'start_q': 260, 'end_q': 288},
    'cycle/23-b-major/renders/meantone-demo-meantone.mp3':
        {'piece': 'fugue-23', 'label': 'Excerpt b66–72, meantone', 'kind': 'excerpt-meantone',
         'start_q': 260, 'end_q': 288},
}
MEDIA_TYPES = {'.mp3': 'audio', '.mp4': 'video', '.pdf': 'pdf', '.mid': 'midi', '.musicxml': 'musicxml',
               '.png': 'image'}
DOWNLOAD_LABELS = {'pdf': 'Score (PDF)', 'midi': 'MIDI', 'musicxml': 'MusicXML'}

EXTRAS = [{
    'id': 'mobius',
    'title': 'Fuga sul nastro di Möbius',
    'score': 'extras/mobius-fugue/fugue.json',
    'concept': 'a string-quartet fugue for a walking listener; halfway round, the room turns into its mirror image',
    'notes': (
        "A fugue a 4 for string quartet, outside the cycle, meant to be heard on headphones as a "
        "listener walking through the room. Carry a left-handed glove once round a Möbius strip and it "
        "comes back right-handed; Bach's crab canon from the Musical Offering is the classic picture on "
        "such a strip, so the subject's head is the Royal Theme's opening, compressed into one bar.\n\n"
        "The four players sit at the corners of a square, and the listener always walks up to and faces "
        "whoever has the subject. Lap 1 ends where it began. In the first seam, a general pause, the room "
        "is mirrored: from then on every sound's left and right are swapped, and the opening returns "
        "literally except that the subject is upside down. After the second seam the room is normal "
        "again, and the finale is a stretto by contrary motion, rectus on the left and inversus on the "
        "right, the listener turning a pirouette between each pair. The coda sounds the head and its "
        "mirror at once over a tonic pedal; the only note they share is the axis, E-flat.\n\n"
        "The video shows the score folding into a Möbius band as it plays; the walk map shows the "
        "listener's path."),
    'tag': 'extra',
}]


# --------------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------------

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key_name(folder_name: str) -> str:
    """'03-c-sharp-major' -> 'C♯ major'."""
    words = folder_name.split('-')[1:]
    out = [words[0].upper()]
    for w in words[1:]:
        if w == 'sharp':
            out[-1] += '♯'
        elif w == 'flat':
            out[-1] += '♭'
        else:
            out.append(w)
    return ' '.join(out)


def clean_title(title: str) -> str:
    """Drop a trailing '(N voices)': the voice count is computed from the score instead."""
    return re.sub(r'\s*\(\d+ voices\)\s*$', '', title)


def split_title(title: str):
    head, sep, rest = title.partition(' · ')
    return (head, rest) if sep else (title, '')


def score_seconds(data) -> float:
    meta = rm.meta_of(data)
    return rm.seconds_at(float(rm.score_duration(data)), rm.tempo_points(meta))


def media_stem(name: str):
    for ext in MEDIA_TYPES:
        if name.endswith(ext):
            return name[:-len(ext)], ext
    return None, None


def parse_guide():
    """Picks ('If you have half an hour') and the per-pair table of LISTENING_GUIDE.md."""
    text = (ROOT / GUIDE).read_text(encoding='utf-8')
    picks, table = [], {}
    sec = re.search(r'^## If you have half an hour\s*$(.*?)(?=^## )', text, re.M | re.S)
    if sec:
        items = re.split(r'^\d+\.\s+', sec.group(1), flags=re.M)[1:]
        for it in items:
            it = ' '.join(it.split())
            m = re.match(r'\*\*(Pair|Fugue|Prelude) ([IVXL]+)\*\*\s*(.*)', it)
            if not m:
                continue
            kind, roman, rest = m.groups()
            num = ROMAN.index(roman)
            route = f'pair/{num}' + ('' if kind == 'Pair' else f'/{kind.lower()}')
            picks.append({'label': f'{kind} {roman}', 'route': route, 'queue': 'pair' if kind == 'Pair' else 'single',
                          'text': rest.lstrip(': ').strip()})
    for line in text.splitlines():
        m = re.match(r'^\|\s*([IVXL]+)\s+[^|(]*\((\d+)\)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$', line)
        if m and m.group(1) in ROMAN:
            table[ROMAN.index(m.group(1))] = {'listen': m.group(3), 'weak': m.group(4)}
    return picks, table


def perf_payload(path, group_voices=False):
    """What the live synth plays, by the rules of render_music.performance_events(): per note
    [t, performed length, pitch, velocity(, cents)] in quarters, where the performed length is
    max(1/32, d * gate) (gate defaults to 0.97) and seconds come from the tempo map; 'cents' is
    present only on notes that carry it (an explicit 0 is kept: that note is not tempered).
    Voices are grouped as in compact() so that solo/mute indices match the display voices."""
    data = json.loads((ROOT / path).read_text(encoding='utf-8'))
    meta = rm.meta_of(data)
    voices = rm.normalized_voices(data)
    if group_voices:
        groups, index = [], {}
        for v in voices:
            key = v.get('name', '').split(' / ')[0]
            if key not in index:
                index[key] = len(groups)
                groups.append([])
            groups[index[key]].extend((e, v) for e in v['events'])
        lists = [sorted(g, key=lambda ev: ev[0]['t']) for g in groups]
    else:
        lists = [[(e, v) for e in v['events']] for v in voices]
    out = []
    for lst in lists:
        rows = []
        for e, v in lst:
            if e.get('p') is None:
                continue
            vel = max(1, min(127, int(e.get('v', v.get('velocity', 72)))))
            length = max(Fraction(1, 32), e['d'] * rm.frac(float(e.get('gate', 0.97))))
            row = [round(float(e['t']), 5), round(float(length), 5), int(e['p']), vel]
            if 'cents' in e:
                row.append(round(float(e['cents']), 3))
            rows.append(row)
        out.append(rows)
    return {'cref': meta.get('cents_reference'), 'v': out}


# --------------------------------------------------------------------------------------------
# Pieces and their media
# --------------------------------------------------------------------------------------------

def manifest_pieces():
    """Pieces of the current edition from the manifest (the 'before' auditions are left out),
    plus the extras.  Each: dict(id, title, score, notes, tag, folder, group, ...)."""
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    out = []
    for g in manifest['groups']:
        for p in g['pieces']:
            score = ROOT / p['score']
            if not p['score'].startswith('cycle/') or not score.exists():
                continue
            folder = score.parent
            q = dict(p)
            if folder.parent.name == 'cycle' and re.match(r'\d\d-', folder.name):
                q.update(group='pair', num=int(folder.name[:2]), folder=folder)
            elif 'appendix' in score.parts:
                q.update(group='appendix', folder=folder)
            else:
                continue
            out.append(q)
    for x in EXTRAS:
        q = dict(x)
        q.update(group='extras', folder=(ROOT / x['score']).parent)
        out.append(q)
    return out


def assign_slugs(pieces):
    """slug = the file stem the piece's renders use (prelude, fugue, prelude-tempered, ...)."""
    by_folder = {}
    for p in pieces:
        by_folder.setdefault(p['folder'], []).append(p)
    for folder, ps in by_folder.items():
        stems = sorted({media_stem(f.name)[0] for f in (folder / 'renders').glob('*') if media_stem(f.name)[0]},
                       key=len) if (folder / 'renders').is_dir() else []
        for p in ps:
            stem = Path(p['score']).stem
            if any(s == stem or s.startswith(stem + '-') for s in stems) or len(ps) > 1 or not stems:
                p['slug'] = stem
            else:
                p['slug'] = stems[0]
    return by_folder


def classify(path: Path, slug: str, siblings: set):
    """Media entry for one rendered file of the piece with this slug."""
    r = rel(path)
    stem, ext = media_stem(path.name)
    typ = MEDIA_TYPES[ext]
    variant = '' if stem == slug else (stem[len(slug) + 1:] if stem.startswith(slug + '-') else stem)
    entry = {'type': typ, 'src': 'media/' + r, 'bytes': path.stat().st_size, 'file': path.name}
    if typ == 'audio':
        if r in EXCERPTS:
            x = EXCERPTS[r]
            entry.update(label=x['label'], kind=x['kind'], start_q=x['start_q'], end_q=x['end_q'])
        else:
            label, kind = LABEL_OVERRIDES.get(r) or AUDIO_LABELS.get(variant) or (variant.replace('-', ' ').capitalize(), variant)
            entry.update(label=label, kind=kind)
        entry['headphones'] = entry['kind'].startswith(('binaural', 'walk'))
    elif typ == 'video':
        entry['label'] = 'Video'
    elif typ == 'image':
        entry['label'] = 'Walk map' if 'walk-map' in stem else variant.replace('-', ' ').capitalize()
    else:
        label = DOWNLOAD_LABELS[typ]
        if variant == 'score':
            label = label if typ == 'pdf' else f'{label} (notation)'
        elif variant == '' and (slug + '-score' + ext) in siblings:
            label = f'{label} (performance)'
        elif variant:
            label = f'{label} ({variant.replace("-", " ")})'
        entry['label'] = label
    return entry


AUDIO_ORDER = ['piano', 'equal', 'meantone', 'walk', 'binaural', 'stereo', 'violin', 'excerpt']


def audio_rank(e):
    k = e['kind']
    for i, base in enumerate(AUDIO_ORDER):
        if k == base or k.startswith(base + '-'):
            return (i, k != base, e['label'])
    return (len(AUDIO_ORDER), False, e['label'])


def collect_media(folder: Path, pieces, renders_dir='renders', exclude=None):
    """Assign every rendered file in folder/renders to a piece: {id: [entries]}."""
    out = {p['id']: [] for p in pieces}
    rdir = folder / renders_dir
    if not rdir.is_dir():
        return out
    files = sorted(f for f in rdir.iterdir() if f.is_file() and media_stem(f.name)[0])
    names = {f.name for f in files}
    for f in files:
        r = rel(f)
        if exclude and exclude(f):
            continue
        if r in EXCERPTS:
            pid = EXCERPTS[r]['piece']
            if pid in out:
                out[pid].append(classify(f, '', names))
            continue
        stem = media_stem(f.name)[0]
        best = None
        for p in pieces:
            s = p['slug']
            if (stem == s or stem.startswith(s + '-')) and (best is None or len(s) > len(best['slug'])):
                best = p
        if best is None and len(pieces) == 1:
            best = pieces[0]
        if best is None:
            print(f'  note: {r} matches no piece; left out', file=sys.stderr)
            continue
        out[best['id']].append(classify(f, best['slug'], names))
    return out


def split_media(entries):
    audio = sorted((e for e in entries if e['type'] == 'audio'), key=audio_rank)
    video = [e for e in entries if e['type'] == 'video']
    images = [e for e in entries if e['type'] == 'image']
    order = {'pdf': 0, 'midi': 1, 'musicxml': 2}
    downloads = sorted((e for e in entries if e['type'] in order), key=lambda e: (order[e['type']], e['label']))
    return audio, video, images, downloads


# --------------------------------------------------------------------------------------------
# Score strips
# --------------------------------------------------------------------------------------------

def strip_dir_for(p) -> Path:
    if p['id'] in EXISTING_STRIPS:
        return ROOT / EXISTING_STRIPS[p['id']]
    return p['folder'] / 'renders' / f"strip-{p['slug']}"


def strip_source(p) -> Path:
    return ROOT / STRIP_SOURCE.get(p['id'], p['score'])


def strip_params(src: Path):
    from score_strip import shortest_gap
    data = json.loads(src.read_text(encoding='utf-8'))
    gap = float(shortest_gap(data))
    gap_ss = round(min(GAP_MAX, max(GAP_MIN, STRIP_QUARTER_SS * gap)), 3)
    return {'staff_space_px': STRIP_STAFF_SPACE_PX, 'gap_ss': gap_ss, 'margin_px': 10}


def strip_state(p):
    """('ok' | 'missing' | 'stale', reason)."""
    d = strip_dir_for(p)
    sj, sp = d / 'strip.json', d / 'strip.png'
    if not (sj.exists() and sp.exists()):
        return 'missing', 'no strip yet'
    if p['id'] in EXISTING_STRIPS:
        return 'ok', 'existing'
    src = strip_source(p)
    try:
        info = json.loads(sj.read_text())
    except ValueError:
        return 'stale', 'unreadable strip.json'
    made = info.get('made_by') or {}
    if made.get('source_sha256'):
        if made['source_sha256'] != sha256(src):
            return 'stale', 'score changed'
        if made.get('params') != strip_params(src):
            return 'stale', 'strip parameters changed'
        return 'ok', ''
    if src.stat().st_mtime > sj.stat().st_mtime:
        return 'stale', 'score is newer'
    return 'ok', ''


def engrave_strip(job):
    """Worker: engrave one strip with tools/score_strip.py and record its provenance."""
    pid, src, out_dir = job
    from score_strip import build_strip
    src, out_dir = Path(src), Path(out_dir)
    params = strip_params(src)
    t0 = time.time()
    try:
        info, _ = build_strip(src, out_dir, margin_px=params['margin_px'], gap_ss=params['gap_ss'],
                              staff_space_px=params['staff_space_px'])
    except Exception as exc:  # noqa: BLE001
        return pid, False, f'{type(exc).__name__}: {str(exc)[-600:]}', time.time() - t0
    info['made_by'] = {'tool': 'tools/score_strip.py (via tools/build_app.py --strips)', 'source': rel(src),
                       'source_sha256': sha256(src), 'params': params}
    (out_dir / 'strip.json').write_text(json.dumps(info, indent=1) + '\n')
    ly = out_dir / 'strip.ly'
    if ly.exists():
        ly.unlink()                 # intermediate (git-ignored); the strip is reproducible from the score
    return pid, True, f"{info['width_px']} x {info['height_px']} px", time.time() - t0


def make_strips(pieces, jobs=2, force=False):
    todo = []
    for p in pieces:
        if p['id'] in EXISTING_STRIPS:
            continue
        state, why = strip_state(p)
        if force or state != 'ok':
            todo.append((p['id'], str(strip_source(p)), str(strip_dir_for(p))))
            print(f'  strip {p["id"]}: {why or "forced"}')
    if not todo:
        print('strips: all up to date')
        return []
    if not shutil.which('lilypond') or not shutil.which('gs'):
        sys.exit('error: --strips needs LilyPond and Ghostscript on PATH')
    # Biggest first, so the long many-staff engravings do not finish last.
    todo.sort(key=lambda j: -Path(j[1]).stat().st_size)
    failures = []
    print(f'strips: engraving {len(todo)} with {jobs} worker(s); about 10-60 s each')
    with concurrent.futures.ProcessPoolExecutor(jobs) as ex:
        for pid, ok, msg, dt in ex.map(engrave_strip, todo):
            print(f'  {"ok  " if ok else "FAIL"} {pid:32s} {dt:6.1f} s  {msg}', flush=True)
            if not ok:
                failures.append((pid, msg))
    return failures


def tile_job(job):
    pid, sdir, out = job
    return pid, tile_strip(pid, Path(sdir), Path(out))


def tile_strip(pid, sdir: Path, out: Path):
    """Cut strip.png into palette PNG tiles under out/strips/<pid>/; returns the site strip JSON."""
    info = json.loads((sdir / 'strip.json').read_text())
    png = sdir / 'strip.png'
    tdir = out / 'strips' / pid
    sj = sdir / 'strip.json'
    stamp = f'{png.stat().st_size}:{int(png.stat().st_mtime)}:{sj.stat().st_size}:{int(sj.stat().st_mtime)}:{TILE_PIXELS}'
    meta_path = out / 'strips' / f'{pid}.json'
    if meta_path.exists() and (tdir / '.stamp').exists() and (tdir / '.stamp').read_text() == stamp:
        return json.loads(meta_path.read_text())
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    img = Image.open(png).convert('RGB')
    W, H = img.size
    tw = int(min(4096, max(1024, TILE_PIXELS // max(1, H))))
    if tdir.exists():
        shutil.rmtree(tdir)
    tdir.mkdir(parents=True)
    tiles = []
    for k, x in enumerate(range(0, W, tw)):
        w = min(tw, W - x)
        tile = img.crop((x, 0, x + w, H)).quantize(colors=64, method=Image.Quantize.MEDIANCUT,
                                                   dither=Image.Dither.NONE)
        name = f'{k:03d}.png'
        tile.save(tdir / name, optimize=True)
        tiles.append([x, w, f'strips/{pid}/{name}'])
    site = {'w': W, 'h': H, 'tiles': tiles,
            't2x': info['time_to_x'], 'staff_y': info.get('staff_y', []),
            'entries': [[e['voice'], e['t'], e.get('label', ''), e['x_px'], e['y_px']] for e in info.get('entries', [])]}
    meta_path.write_text(json.dumps(site, separators=(',', ':')))
    (tdir / '.stamp').write_text(stamp)
    return site


# --------------------------------------------------------------------------------------------
# Site
# --------------------------------------------------------------------------------------------

class Media:
    """Places repository files under out/media/, copying (hard-linking where possible) or symlinking."""

    def __init__(self, out: Path, link: bool):
        self.out, self.link, self.files = out, link, {}

    def add(self, path: Path) -> str:
        r = rel(path)
        if r not in self.files:
            dest = self.out / 'media' / r
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists() or dest.is_symlink():
                dest.unlink()
            if self.link:
                os.symlink(path.resolve(), dest)
            else:
                try:
                    os.link(path, dest)
                except OSError:
                    shutil.copy2(path, dest)
            self.files[r] = path.stat().st_size
        return 'media/' + r


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(',', ':')))


def build_site(pieces, out: Path, link: bool, exclude_archive: bool):
    t0 = time.time()
    out.mkdir(parents=True, exist_ok=True)
    for child in out.iterdir():            # keep only the strip tile cache between builds
        if child.name == 'strips':
            continue
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
    media = Media(out, link)
    for name in APP_FILES:
        shutil.copy2(APP_DIR / name, out / name)
    (out / '.nojekyll').write_text('')

    picks, table = parse_guide()
    by_folder = assign_slugs(pieces)
    media_of, earlier_of = {}, {}
    for folder, ps in by_folder.items():
        media_of.update(collect_media(folder, ps))
        arch = folder / 'archive-n-plus-1'
        if arch.is_dir() and (arch / 'fugue.json').exists():
            fugue = next((p for p in ps if p['slug'] == 'fugue'), None)
            if fugue:
                fake = [{'id': fugue['id'], 'slug': 'fugue'}]
                excl = (lambda f: True) if exclude_archive else None
                earlier_of[fugue['id']] = (arch, collect_media(arch, fake, exclude=excl)[fugue['id']])

    temps = {k: rm.temperament_offsets(k) for k in TEMPERAMENTS}
    catalog_pieces, strips_used, missing_strips = {}, set(), []

    # Cut the strips into tiles (in parallel; cached between builds).
    states = {p['id']: strip_state(p) for p in pieces}
    jobs = [(p['id'], str(strip_dir_for(p)), str(out)) for p in pieces if states[p['id']][0] != 'missing']
    with concurrent.futures.ProcessPoolExecutor(min(4, os.cpu_count() or 1)) as ex:
        list(ex.map(tile_job, jobs))
    for p in pieces:
        pid = p['id']
        data = json.loads((ROOT / p['score']).read_text(encoding='utf-8'))
        c = compact(p['score'], p.get('group_voices', False), p.get('stats_score'))
        c['perf'] = perf_payload(p['score'], p.get('group_voices', False))
        write_json(out / 'scores' / f'{pid}.json', c)
        stats = c.get('stats') if isinstance(c.get('stats'), dict) else {}
        voices = stats.get('voices') or len(c['voices'])
        title = clean_title(p['title'])
        short, sub = split_title(title)
        audio, video, images, downloads = split_media(media_of.get(pid, []))
        for e in audio + video + images + downloads:
            media.add(ROOT / e['src'][len('media/'):])
        rec = {
            'id': pid, 'slug': p['slug'], 'group': p['group'], 'title': title, 'short': short, 'sub': sub,
            'tag': p.get('tag', ''), 'notes': p.get('notes', ''), 'voices': voices,
            'bars': stats.get('bars'), 'duration': round(score_seconds(data), 1),
            'key': c['key'].strip(), 'meter': c['meter'], 'bpm': c['bpm'],
            'score': f'scores/{pid}.json', 'audio': audio, 'video': video, 'images': images,
            'downloads': downloads, 'source': p['score'],
        }
        if p['group'] == 'pair':
            n = p['num']
            rec['num'] = n
            rec['route'] = f"pair/{n}/{p['slug']}"
        else:
            rec['route'] = f"{p['group']}/{pid}"
        notes_md = None
        for cand in ([f"NOTES-{p['slug']}.md"] if p['slug'] in ('prelude', 'fugue') else []) + ['NOTES.md']:
            if (p['folder'] / cand).exists():
                notes_md = media.add(p['folder'] / cand)
                break
        rec['notes_md'] = notes_md
        # Strip
        sdir = strip_dir_for(p)
        state, why = states[pid]
        if state == 'missing':
            missing_strips.append(pid)
            rec['strip'] = None
        else:
            if state == 'stale':
                print(f'  warning: strip for {pid} is stale ({why}); run with --strips', file=sys.stderr)
            tile_strip(pid, sdir, out)
            strips_used.add(pid)
            rec['strip'] = f'strips/{pid}.json'
        # Earlier version
        if pid in earlier_of:
            arch, entries = earlier_of[pid]
            adata = json.loads((arch / 'fugue.json').read_text(encoding='utf-8'))
            ac = compact(rel(arch / 'fugue.json'))
            ac['perf'] = perf_payload(rel(arch / 'fugue.json'))
            write_json(out / 'scores' / f'{pid}-earlier.json', ac)
            a_audio, a_video, _, a_down = split_media(entries)
            for e in a_audio + a_video + a_down:
                media.add(ROOT / e['src'][len('media/'):])
            rec['earlier'] = {
                'score': f'scores/{pid}-earlier.json',
                'voices': (ac.get('stats') if isinstance(ac.get('stats'), dict) else {}).get('voices') or len(ac['voices']),
                'bars': (ac.get('stats') if isinstance(ac.get('stats'), dict) else {}).get('bars'),
                'duration': round(score_seconds(adata), 1),
                'key': ac['key'].strip(), 'meter': ac['meter'], 'bpm': ac['bpm'],
                'sub': ac.get('sub', ''),
                'audio': a_audio, 'downloads': a_down,
                'readme_md': media.add(arch / 'README.md') if (arch / 'README.md').exists() else None,
                'notes_md': media.add(arch / 'NOTES.md') if (arch / 'NOTES.md').exists() else None,
                'source': rel(arch / 'fugue.json'),
            }
        catalog_pieces[pid] = rec

    # Groups
    groups = []
    pairs = {}
    for p in pieces:
        if p['group'] == 'pair':
            pairs.setdefault(p['num'], []).append(p)
    for n in sorted(pairs):
        ps = pairs[n]
        folder = ps[0]['folder']
        ids = [p['id'] for p in ps]
        fugue = next((catalog_pieces[i] for i in ids if catalog_pieces[i]['slug'] == 'fugue'), None)
        main_ids = [i for i in ids if catalog_pieces[i]['slug'] in ('prelude', 'fugue')]
        g = {'id': f'pair-{n}', 'kind': 'pair', 'num': n, 'roman': ROMAN[n], 'key': key_name(folder.name),
             'title': f'Pair {ROMAN[n]}', 'pieces': ids, 'play': main_ids,
             'voices': fugue['voices'] if fugue else None,
             'duration': round(sum(catalog_pieces[i]['duration'] for i in main_ids), 1),
             'concept': (table.get(n) or {}).get('listen', ''), 'weak': (table.get(n) or {}).get('weak', ''),
             'recomposed': bool(fugue and fugue.get('earlier')), 'route': f'pair/{n}'}
        for i in ids:
            catalog_pieces[i]['pair'] = g['id']
            catalog_pieces[i]['key_name'] = g['key']
        groups.append(g)
    for kind, title, sub in [('appendix', 'Appendix', 'Canons and contrapuncti, after Bach’s appended canons'),
                             ('extras', 'Extras', 'Outside the cycle')]:
        ids = [p['id'] for p in pieces if p['group'] == kind]
        if ids:
            groups.append({'id': kind, 'kind': kind, 'title': title, 'sub': sub, 'pieces': ids, 'play': ids,
                           'duration': round(sum(catalog_pieces[i]['duration'] for i in ids), 1)})
    for p in pieces:
        if p['group'] != 'pair':
            rec = catalog_pieces[p['id']]
            rec['concept'] = p.get('concept') or first_sentence(rec['notes'])

    catalog = {
        'title': 'The Well-Tempered clAIvier', 'repo': REPO_URL,
        'guide': media.add(ROOT / GUIDE), 'picks': picks,
        'groups': groups, 'pieces': catalog_pieces, 'temps': temps,
        'cycle': [i for g in groups if g['kind'] in ('pair', 'appendix') for i in g['play']],
        'built': time.strftime('%Y-%m-%d'),
    }
    write_json(out / 'catalog.json', catalog)

    # Drop tile folders of strips no longer in use.
    sroot = out / 'strips'
    if sroot.is_dir():
        for child in sroot.iterdir():
            pid = child.name[:-5] if child.name.endswith('.json') else child.name
            if pid not in strips_used:
                shutil.rmtree(child) if child.is_dir() else child.unlink()

    # Size report.
    def size_of(path: Path):
        total = 0
        for dirpath, _, files in os.walk(path, followlinks=True):
            for f in files:
                try:
                    total += os.stat(os.path.join(dirpath, f)).st_size
                except OSError:
                    pass
        return total

    media_bytes = sum(media.files.values())
    total = size_of(out)
    strips_bytes = size_of(out / 'strips') if (out / 'strips').exists() else 0
    archive_bytes = sum(s for r, s in media.files.items() if '/archive-n-plus-1/' in r)
    mb = lambda b: f'{b / 1e6:,.1f} MB'  # noqa: E731
    print(f'built {out} in {time.time() - t0:.1f} s: {len(catalog_pieces)} pieces, {len(media.files)} media files '
          f'({"symlinked" if link else "copied"}), {len(strips_used)} score strips')
    print(f'site size {mb(total)}: media {mb(media_bytes)} (earlier versions {mb(archive_bytes)}), '
          f'strips {mb(strips_bytes)}, app + scores {mb(total - media_bytes - strips_bytes)}')
    if missing_strips:
        print(f'  {len(missing_strips)} piece(s) without a score strip (piano roll instead): '
              f'{", ".join(missing_strips)}; run with --strips', file=sys.stderr)
    if total > PAGES_LIMIT:
        msg = (f'the site is {mb(total)}, over the GitHub Pages limit of {mb(PAGES_LIMIT)}; '
               'try --exclude-archive (drops the earlier versions\' media)')
        if link:
            print('WARNING: ' + msg, file=sys.stderr)
        else:
            sys.exit('error: ' + msg)
    return catalog


def first_sentence(text: str) -> str:
    m = re.match(r'(.+?[.!?])(\s|$)', text.strip().split('\n')[0])
    return m.group(1) if m else text[:140]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=str(ROOT / '_site'), help='output folder (default _site/)')
    ap.add_argument('--link', action='store_true', help='symlink the media instead of copying (local use)')
    ap.add_argument('--exclude-archive', action='store_true',
                    help="leave out the earlier versions' media (archive-n-plus-1, about 312 MB)")
    ap.add_argument('--strips', action='store_true',
                    help='engrave missing or stale score strips (LilyPond) before building')
    ap.add_argument('--strips-only', action='store_true', help='engrave strips, do not build the site')
    ap.add_argument('--force-strips', action='store_true', help='re-engrave every strip')
    ap.add_argument('--only', default='', help='comma-separated piece ids (with --strips: only these)')
    ap.add_argument('--jobs', type=int, default=2, help='strips engraved in parallel (default 2)')
    a = ap.parse_args()

    pieces = manifest_pieces()
    assign_slugs(pieces)
    failures = []
    if a.strips or a.strips_only or a.force_strips:
        sel = [p for p in pieces if not a.only or p['id'] in a.only.split(',')]
        failures = make_strips(sel, jobs=a.jobs, force=a.force_strips)
        if failures:
            print(f'{len(failures)} strip(s) failed:', file=sys.stderr)
            for pid, msg in failures:
                print(f'  {pid}: {msg}', file=sys.stderr)
    if a.strips_only:
        sys.exit(1 if failures else 0)
    build_site(pieces, Path(a.out).resolve(), a.link, a.exclude_archive)


if __name__ == '__main__':
    main()
