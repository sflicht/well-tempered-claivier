#!/usr/bin/env python3
"""Engrave a whole score as ONE long horizontal system (a "score strip") for video.

    python3 tools/score_strip.py cycle/03-c-sharp-major/fugue.json --out-dir DIR [--height-px 460]
        [--margin-px 10] [--gap-ss 3.0] [--check] [--keep-work]

Outputs
  DIR/strip.png   the piece engraved by LilyPond as a single system, white background, exactly
                  --height-px tall.  Notes (heads, stems, flags, beams, accidentals, dots, ties,
                  rests) are coloured per voice; notes inside a subject entry are drawn in the full
                  colour, all others in a ~55% tint toward white.  Everything else is black.
  DIR/strip.json  {"width_px", "height_px",
                   "time_to_x": [[t_quarters, x_px], ...]   one point per onset (note or rest, every
                                                            staff, so also every bar line) plus the
                                                            final bar line at the end time,
                   "staff_y": [[top_px, bottom_px], ...]    per staff, top to bottom,
                   "entries": [{"voice", "t", "label", "x_px", "y_px"}, ...]}
  DIR/strip.ly    the LilyPond source that was engraved (for reproducibility).
  DIR/check.png   (--check) three crops (start, middle, end) with a red line at time_to_x of
                  every onset; the measured raster offsets are printed.

x_px of an onset is the left edge of its notehead (or rest) column, so a playhead drawn at
time_to_x(t) sits on the note sounding at t.

How it works
  1. tools/render_music.create_lilypond() writes the normal score; we post-process its text:
     titles, page furniture, text labels, rehearsal and tempo marks are removed; staves get their
     short name only; the paper uses ly:one-line-breaking (one system, page as wide as needed)
     with strictly proportional spacing (x ~ linear in time between onsets).
  2. Scheme callbacks (a) colour every note grob from its moment and its voice's subject spans and
     (b) tag every NoteHead, Rest, BarLine and StaffSymbol with output-attributes, which the SVG
     backend writes onto that grob's <g> element (class + data-t = onset in quarters, exact).
  3. The same .ly is engraved twice, with the SVG backend (positions) and as PDF (pixels).  Layout
     is backend independent, so both have identical geometry.  Ghostscript's bbox device gives the
     exact ink box of the PDF; we choose a resolution so that the ink is height_px - 2*margin tall,
     rasterise the PDF at that resolution and crop.  SVG coordinates map to pixels by the same
     affine transform (SVG unit -> mm -> inch * dpi - crop offset); --check measures it.
"""
from __future__ import annotations

import argparse
import bisect
import concurrent.futures
from fractions import Fraction
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_music as rm  # noqa: E402  (reused: create_lilypond, normalized_voices, frac, ...)

# Voice colours (RGB 0-255) in voice order; voices beyond six reuse them cyclically.
PALETTE = [(200, 120, 0), (20, 120, 190), (0, 130, 90), (180, 60, 140), (150, 140, 0), (190, 70, 0)]
TINT = 0.55                      # non-subject notes: this far from the full colour toward white
COLOURED_GROBS = ['NoteHead', 'Stem', 'Flag', 'Beam', 'Accidental', 'Dots', 'Tie', 'Rest']
MM_PER_INCH = 25.4
PT_PER_INCH = 72.0


# ----------------------------------------------------------------------------------------------
# Score analysis
# ----------------------------------------------------------------------------------------------

def staff_voices(data):
    """Engraved staves in order, each a list of voice indices (host first, then any voices that
    share its staff, mirroring render_music.create_lilypond's "share_staff" handling)."""
    voices = data['voices']
    hosts = {}
    for i, v in enumerate(voices):
        ref = v.get('share_staff')
        if ref is None:
            continue
        h = next(k for k, w in enumerate(voices) if k != i and ref in (w.get('name'), w.get('abbr')))
        hosts.setdefault(h, []).append(i)
    guests = {g for gs in hosts.values() for g in gs}
    return [[i] + hosts.get(i, []) for i in range(len(voices)) if i not in guests]


def subject_spans(data):
    """Per voice, merged [start, end) spans in quarters drawn in full colour: each subject entry
    (t .. t + total subject duration; an entry may carry its own "d"), extended to the end of any
    note that starts inside it (so a held or tied last note stays full colour)."""
    voices = rm.normalized_voices(data)
    entries = data.get('subject_entries') or []
    subj_len = sum((rm.frac(n['d']) for n in data.get('subject') or []), Fraction(0))
    spans = [[] for _ in voices]
    for e in entries:
        v, t0 = int(e['voice']), rm.frac(e['t'])
        t1 = t0 + (rm.frac(e['d']) if 'd' in e else subj_len)
        if t1 <= t0 or not 0 <= v < len(voices):
            continue
        for n in voices[v]['events']:
            if t0 <= n['t'] < t1 and n.get('p') is not None:
                t1 = max(t1, n['t'] + n['d'])
        spans[v].append((t0, t1))
    merged = []
    for sp in spans:
        out = []
        for a, b in sorted(sp):
            if out and a <= out[-1][1]:
                out[-1] = (out[-1][0], max(out[-1][1], b))
            else:
                out.append((a, b))
        merged.append(out)
    return merged


def shortest_gap(data):
    """Smallest distance (quarters) between two neighbouring engraved columns: all note onsets
    and bar lines (notes are split at bar lines), floored at a 32nd note."""
    meta = rm.meta_of(data)
    beats, den = rm.meter_of(meta)
    bar = Fraction(beats * 4, den)
    end = rm.score_duration(data)
    times = {e['t'] for v in rm.normalized_voices(data) for e in v['events']}
    times |= {e['t'] + e['d'] for v in rm.normalized_voices(data) for e in v['events']}
    times |= {bar * k for k in range(int(end / bar) + 1)}
    ts = sorted(times)
    gaps = [b - a for a, b in zip(ts, ts[1:]) if b > a]
    return max(min(gaps, default=Fraction(1)), Fraction(1, 8))


# ----------------------------------------------------------------------------------------------
# LilyPond source
# ----------------------------------------------------------------------------------------------

def scm_colour(rgb):
    return "'(%s)" % ' '.join(f'{c / 255:.4f}' for c in rgb)


def scm_spans(spans):
    """Spans in quarters -> Scheme list of exact (start . end) pairs in whole notes (moments)."""
    def q(x):
        x = Fraction(x) / 4
        return f'{x.numerator}/{x.denominator}'
    return '(list ' + ' '.join(f'(cons {q(a)} {q(b)})' for a, b in spans) + ')'


SCHEME_HELPERS = r'''
% ---- score_strip helpers -------------------------------------------------------------------
% Global time (whole notes, exact rational) of an item = the 'when of its paper column.
#(define (strip-when grob)
   (let ((col (and (ly:item? grob) (ly:item-get-column grob))))
     (and (ly:grob? col) (ly:moment-main (ly:grob-property col 'when)))))

% Quarter-note time as an exact string ("3/2"), for the SVG data-t attribute.
#(define (strip-t-string grob)
   (let ((w (strip-when grob))) (if w (number->string (* 4 w)) "")))

% output-attributes callback: the SVG backend writes these onto the grob's <g> element.
#(define ((strip-attrs class) grob)
   (list (cons 'class class) (cons 'data-t (strip-t-string grob))))

#(define (strip-in-spans? t spans)
   (and t (any (lambda (s) (and (>= t (car s)) (< t (cdr s)))) spans)))

% Colour callback for one voice: full colour inside a subject span, tint elsewhere.
% Items use their own time; a tie uses the note it starts from; a beam is full colour when at
% least half of its stems are inside a span.
#(define ((strip-colourer full tint spans) grob)
   (define (in? g) (strip-in-spans? (strip-when g) spans))
   (cond
    ((ly:item? grob) (if (in? grob) full tint))
    ((grob::has-interface grob 'beam-interface)
     (let* ((stems (ly:grob-array->list (ly:grob-object grob 'stems)))
            (n-in (length (filter in? stems))))
       (if (and (pair? stems) (>= (* 2 n-in) (length stems))) full tint)))
    ((ly:spanner? grob) (if (in? (ly:spanner-bound grob LEFT)) full tint))
    (else tint)))
'''


def colour_overrides(voice, spans):
    """\\override lines colouring all note grobs of one voice."""
    full = PALETTE[voice % len(PALETTE)]
    tint = tuple(round(c + TINT * (255 - c)) for c in full)
    if not any(spans):   # a score without subject entries: everything in full colour
        tint = full
    name = f'strip-colour-{voice}'
    define = f'#(define {name} (strip-colourer {scm_colour(full)} {scm_colour(tint)} {scm_spans(spans[voice])}))'
    return define, ' '.join(f'\\override {g}.color = #{name}' for g in COLOURED_GROBS)


def block_span(lines, start):
    """Index just past the '}' closing the block whose opening '{' is on lines[start]."""
    depth = 0
    for k in range(start, len(lines)):
        depth += lines[k].count('{') - lines[k].count('}')
        if depth == 0:
            return k + 1
    raise ValueError('unbalanced braces in generated LilyPond')


STAFF_RE = re.compile(r'^(\s*\\new Staff \\with \{ )instrumentName = "((?:[^"\\]|\\.)*)" '
                      r'shortInstrumentName = "((?:[^"\\]|\\.)*)"( \} (?:\{|<<))\s*$')
VOICE_RE = re.compile(r'^(\s*\\new Voice )(\{.*)$')


def strip_lilypond(data, base_text, paper_height_mm, gap_ss):
    """Turn create_lilypond's page-oriented source into the one-system strip source."""
    staves = staff_voices(data)
    spans = subject_spans(data)
    lines = base_text.split('\n')

    # 1. Titles and paper: replace the \header and \paper blocks.
    paper = [
        '\\header { tagline = ##f }',
        '\\paper {',
        '  page-breaking = #ly:one-line-breaking   % one system; paper-width grows to fit it',
        f'  paper-height = {paper_height_mm:.1f}\\mm',
        '  top-margin = 10\\mm  bottom-margin = 10\\mm  left-margin = 40\\mm  right-margin = 10\\mm',
        '  print-page-number = ##f  print-first-page-number = ##f',
        '  bookTitleMarkup = ##f  scoreTitleMarkup = ##f',
        '  oddHeaderMarkup = ##f  evenHeaderMarkup = ##f  oddFooterMarkup = ##f  evenFooterMarkup = ##f',
        '  ragged-bottom = ##t  ragged-last-bottom = ##t   % never stretch the staves apart',
        '}',
    ]
    out, k = [], 0
    while k < len(lines):
        s = lines[k].strip()
        if s.startswith('\\header {') or s.startswith('\\paper {'):
            k = block_span(lines, k)
            if s.startswith('\\paper'):
                out += paper
            continue
        if s.startswith('\\score {'):
            out += SCHEME_HELPERS.strip('\n').split('\n')
            out += [colour_overrides(v, spans)[0] for v in range(len(data['voices']))]
        out.append(lines[k])
        k += 1
    lines = out

    # 2. Staves: short name only, a tagged StaffSymbol, and the voice colours.  A staff holding
    #    one voice is coloured in its \with; a shared staff colours each \new Voice instead.
    staff_iter = iter(enumerate(staves))
    pending_voices = []
    for k, line in enumerate(lines):
        m = STAFF_RE.match(line)
        if m:
            si, vs = next(staff_iter)
            short = m.group(3)
            extra = f'\\override StaffSymbol.output-attributes = #\'((class . "staff") (data-staff . "{si}"))'
            if len(vs) == 1:
                extra += ' ' + colour_overrides(vs[0], spans)[1]
                pending_voices = []
            else:
                pending_voices = list(vs)
            lines[k] = f'{m.group(1)}instrumentName = "{short}" shortInstrumentName = "{short}" {extra}{m.group(4)}'
            continue
        m = VOICE_RE.match(line)
        if m and pending_voices:
            v = pending_voices.pop(0)
            lines[k] = f'{m.group(1)}\\with {{ {colour_overrides(v, spans)[1]} }} {m.group(2)}'
    if next(staff_iter, None) is not None or pending_voices:
        raise ValueError('could not match every staff/voice in the generated LilyPond')

    # 3. Layout: proportional spacing, position tags, no text.  Appended at the end of the
    #    existing \layout block so that it overrides create_lilypond's indent.
    #    Proportional notation: a duration d (whole notes) gets 2.4 staff spaces * d / pnd, so the
    #    shortest gap between columns gets gap_ss staff spaces.
    pnd = Fraction(2.4 * float(shortest_gap(data)) / 4 / gap_ss).limit_denominator(2000)
    layout = [
        '    indent = 0  short-indent = 0   % the short staff names hang into the left margin',
        '    \\context { \\Score',
        f'      proportionalNotationDuration = #(ly:make-moment {pnd.numerator}/{pnd.denominator})',
        '      \\override SpacingSpanner.uniform-stretching = ##t',
        '      \\override SpacingSpanner.strict-note-spacing = ##t',
        '      \\override NoteHead.output-attributes = #(strip-attrs "nh")',
        '      \\override Rest.output-attributes = #(strip-attrs "rest")',
        '      \\override BarLine.output-attributes = #(strip-attrs "bar")',
        '      \\omit RehearsalMark  \\omit MetronomeMark',
        '    }',
        '    \\context { \\Voice \\omit TextScript }',
    ]
    start = next(k for k, l in enumerate(lines) if l.strip() == '\\layout {')
    end = block_span(lines, start) - 1          # the line holding the closing brace
    lines[end:end] = layout
    return '\n'.join(lines)


# ----------------------------------------------------------------------------------------------
# Engraving and measuring
# ----------------------------------------------------------------------------------------------

def run(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if p.returncode != 0:
        raise RuntimeError(f'{cmd[0]} failed:\n{p.stdout[-3000:]}\n{p.stderr[-3000:]}')
    return p


def engrave(ly_path, work):
    """Engrave the same source with the SVG backend and as PDF, in parallel."""
    base = ['lilypond', '-dno-point-and-click']
    jobs = {'svg': base + ['-dbackend=svg', '-o', str(work / 'svg'), str(ly_path)],
            'pdf': base + ['--pdf', '-o', str(work / 'pdf'), str(ly_path)]}
    with concurrent.futures.ThreadPoolExecutor(2) as ex:
        res = {k: ex.submit(run, cmd) for k, cmd in jobs.items()}
        logs = {k: r.result().stderr for k, r in res.items()}
    svgs = sorted(work.glob('svg*.svg'))
    if len(svgs) != 1:
        raise RuntimeError(f'expected one SVG page, got {svgs}')
    return svgs[0], work / 'pdf.pdf', logs['pdf']


TRANSLATE_RE = re.compile(r'translate\(\s*([-\d.eE]+)[\s,]+([-\d.eE]+)\s*\)')


def parse_svg(svg_path):
    """Return (mm per SVG unit, page size in units, tagged groups).  Each group is a dict with
    class, t (Fraction or None), staff, glyphs [(x, y)] (glyph origins), lines and rects, all in
    absolute SVG units (translations accumulated down the tree)."""
    root = ET.parse(svg_path).getroot()
    vb = [float(v) for v in root.get('viewBox').split()]
    mm_per_unit = float(root.get('width').rstrip('m')) / vb[2]
    groups = []

    def local(tag):
        return tag.rsplit('}', 1)[-1]

    def walk(el, ox, oy, cur):
        tr = el.get('transform') or ''
        m = TRANSLATE_RE.search(tr)
        if m:
            ox, oy = ox + float(m.group(1)), oy + float(m.group(2))
        cls = el.get('class')
        if cls in ('nh', 'rest', 'bar', 'staff'):
            t = el.get('data-t')
            cur = {'class': cls, 't': Fraction(t) if t else None, 'staff': el.get('data-staff'),
                   'glyphs': [], 'lines': [], 'rects': []}
            groups.append(cur)
        if cur is not None:
            tag = local(el.tag)
            if tag == 'path' and 'scale' in tr:            # a font glyph drawn at (ox, oy)
                cur['glyphs'].append((ox, oy))
            elif tag == 'line':
                sw = float(el.get('stroke-width', 0))
                cur['lines'].append((ox + float(el.get('x1')), oy + float(el.get('y1')),
                                     ox + float(el.get('x2')), oy + float(el.get('y2')), sw))
            elif tag == 'rect':
                cur['rects'].append((ox + float(el.get('x')), oy + float(el.get('y')),
                                     float(el.get('width')), float(el.get('height'))))
        for ch in el:
            walk(ch, ox, oy, cur)

    walk(root, -vb[0], -vb[1], None)
    return mm_per_unit, (vb[2], vb[3]), groups


def ink_bbox_pt(pdf):
    """Exact ink bounding box of the PDF page in points (x0, y0, x1, y1), origin bottom-left."""
    p = run(['gs', '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=bbox', str(pdf)])
    m = re.search(r'%%HiResBoundingBox:\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)', p.stderr + p.stdout)
    return tuple(float(v) for v in m.groups())


def rasterise(pdf, dpi, out_png):
    run(['gs', '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=png16m', f'-r{dpi:.6f}',
         '-dTextAlphaBits=4', '-dGraphicsAlphaBits=4', '-dBackgroundColor=16#FFFFFF',
         f'-sOutputFile={out_png}', str(pdf)])


# ----------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------

def build_strip(score_path, out_dir, height_px=460, margin_px=10, gap_ss=3.0, keep_work=False):
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    data = json.loads(Path(score_path).read_text())
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix='strip-', dir=out_dir if keep_work else None))
    try:
        base_ly = work / 'base.ly'
        rm.create_lilypond(data, base_ly)
        base_text = base_ly.read_text(encoding='utf-8')

        # A page tall enough for the system (it is never stretched: ragged-bottom).  If LilyPond
        # had to compress the system to fit, double the height and engrave again.
        n = len(staff_voices(data))
        staff_size = float(re.search(r'set-global-staff-size ([\d.]+)', base_text).group(1))
        ss_mm = staff_size / 4 * MM_PER_INCH / PT_PER_INCH
        paper_h = 20 + ss_mm * (24 * n + 30)
        for attempt in range(4):
            ly_text = strip_lilypond(data, base_text, paper_h, gap_ss)
            ly_path = out_dir / 'strip.ly'
            ly_path.write_text(ly_text, encoding='utf-8')
            svg, pdf, log = engrave(ly_path, work)
            x0, y0, x1, y1 = ink_bbox_pt(pdf)
            if 'compress' not in log.lower() and y0 > 5:
                break
            paper_h *= 2
        else:
            raise RuntimeError('system does not fit on the page')

        # Resolution: ink exactly height_px - 2*margin tall, nudged so that the page height is a
        # whole number of pixels (then pixel rows map exactly from the top edge of the page).
        mm_per_unit, (page_w_u, page_h_u), groups = parse_svg(svg)
        page_h_pt = page_h_u * mm_per_unit / MM_PER_INCH * PT_PER_INCH
        dpi = (height_px - 2 * margin_px) * PT_PER_INCH / (y1 - y0)
        dpi = round(page_h_pt * dpi / PT_PER_INCH) * PT_PER_INCH / page_h_pt
        px_per_pt = dpi / PT_PER_INCH
        page_png = work / 'page.png'
        rasterise(pdf, dpi, page_png)
        page = Image.open(page_png).convert('RGB')

        # Crop: ink box plus margin, exactly height_px tall.
        ink_top = page_h_pt - y1                                  # pt from the page top
        cx0 = math.floor(x0 * px_per_pt) - margin_px
        cy0 = round(ink_top * px_per_pt + ((y1 - y0) * px_per_pt - height_px) / 2)
        cx1 = math.ceil(x1 * px_per_pt) + margin_px
        strip = page.crop((cx0, cy0, cx1, cy0 + height_px))
        strip.save(out_dir / 'strip.png', optimize=True)
        width_px = strip.size[0]

        # SVG units -> strip pixels.
        px_per_unit = mm_per_unit / MM_PER_INCH * dpi

        def X(u):
            return u * px_per_unit - cx0

        def Y(u):
            return u * px_per_unit - cy0

        # time_to_x: the left edge of the noteheads at each onset (rests where no note starts).
        heads, rests, bars = {}, {}, {}
        for g in groups:
            if g['class'] in ('nh', 'rest') and g['t'] is not None and g['glyphs']:
                d = heads if g['class'] == 'nh' else rests
                x = min(p[0] for p in g['glyphs'])
                d[g['t']] = min(d.get(g['t'], x), x)
            elif g['class'] == 'bar' and g['t'] is not None and g['rects']:
                x = min(r[0] for r in g['rects'])
                bars[g['t']] = min(bars.get(g['t'], x), x)
        onsets = {**rests, **heads}
        end_t = max(bars) if bars else None
        points = sorted((t, X(x)) for t, x in onsets.items())
        if end_t is not None and end_t > points[-1][0]:
            points.append((end_t, X(bars[end_t])))      # the final bar line closes the strip
        for (ta, xa), (tb, xb) in zip(points, points[1:]):
            if xb <= xa:
                raise RuntimeError(f'time_to_x not monotonic at t={float(tb)}: {xa:.2f} -> {xb:.2f}')

        staff_y = {}
        for g in groups:
            if g['class'] == 'staff' and g['lines']:
                top = min(l[1] - l[4] / 2 for l in g['lines'])
                bot = max(l[1] + l[4] / 2 for l in g['lines'])
                staff_y[int(g['staff'])] = (Y(top), Y(bot))
        staff_y = [staff_y[k] for k in sorted(staff_y)]
        staff_of_voice = {v: s for s, vs in enumerate(staff_voices(data)) for v in vs}
        staff_space = (staff_y[0][1] - staff_y[0][0]) / 4

        def time_to_x(t):
            ts = [p[0] for p in points]
            k = bisect.bisect_right(ts, t) - 1
            if k < 0:
                return points[0][1]
            if k >= len(points) - 1:
                return points[-1][1]
            (ta, xa), (tb, xb) = points[k], points[k + 1]
            return xa + (xb - xa) * float((t - ta) / (tb - ta))

        entries = []
        for e in data.get('subject_entries') or []:
            v, t = int(e['voice']), rm.frac(e['t'])
            entries.append({'voice': v, 't': float(t), 'label': e.get('label', 'Subject'),
                            'x_px': round(time_to_x(t), 2),
                            'y_px': round(staff_y[staff_of_voice[v]][0] - staff_space, 2)})
        info = {'width_px': width_px, 'height_px': height_px,
                'time_to_x': [[float(t), round(x, 2)] for t, x in points],
                'staff_y': [[round(a, 2), round(b, 2)] for a, b in staff_y],
                'entries': entries}
        (out_dir / 'strip.json').write_text(json.dumps(info, indent=1) + '\n')
        return info, {'heads': heads, 'rests': rests, 'X': X, 'Y': Y, 'groups': groups,
                      'staff_space': staff_space, 'dpi': dpi}
    finally:
        if not keep_work:
            shutil.rmtree(work, ignore_errors=True)


# ----------------------------------------------------------------------------------------------
# Self-check: red marks at time_to_x, and a measurement of the raster against the positions
# ----------------------------------------------------------------------------------------------

def check(out_dir, info, extra, crop_w=900):
    import numpy as np
    from PIL import Image, ImageDraw
    Image.MAX_IMAGE_PIXELS = None
    out_dir = Path(out_dir)
    img = Image.open(out_dir / 'strip.png').convert('RGB')
    arr = np.asarray(img).astype(int)
    W, H = img.size

    # Measure: for each notehead, the leftmost column of non-white ink in a narrow window around
    # its predicted left edge, on the rows of the head itself.  (Ink to the left of a head, e.g.
    # an accidental or a ledger line, would bias this, so ledger lines are ignored by requiring
    # coloured pixels and the window starts only 3 px left of the prediction.)
    ss = extra['staff_space']
    errs = []
    for g in extra['groups']:
        if g['class'] != 'nh' or not g['glyphs']:
            continue
        gx, gy = min(g['glyphs'])
        px, py = extra['X'](gx), extra['Y'](gy)
        x0, x1 = int(px) - 3, int(px + 0.8 * ss)
        y0, y1 = int(py - 0.25 * ss), int(py + 0.25 * ss) + 1
        if x0 < 0 or x1 >= W or y0 < 0 or y1 >= H:
            continue
        win = arr[y0:y1, x0:x1]
        sat = win.max(axis=2) - win.min(axis=2)           # chroma: coloured ink only
        cols = np.where((sat > 40).any(axis=0))[0]
        if len(cols):
            # sub-pixel left edge from the anti-aliased coverage of the first coloured column
            c = cols[0]
            cov = sat[:, c].max() / max(1, sat.max())
            errs.append((x0 + c + 1 - cov) - px)
    errs = np.array(errs)
    stats = (f'{len(errs)} noteheads: raster left edge - time_to_x: median {np.median(errs):+.2f} px, '
             f'95% within {np.percentile(np.abs(errs - np.median(errs)), 95):.2f} px of median, '
             f'max |err| {np.abs(errs).max():.2f} px') if len(errs) else 'no noteheads measured'

    # Visual: three crops with a red line at every time_to_x point.
    pts = info['time_to_x']
    marked = img.copy()
    dr = ImageDraw.Draw(marked)
    for t, x in pts:
        xi = int(math.floor(x))
        dr.line([(xi, 0), (xi, H)], fill=(255, 0, 0), width=1)
    starts = [0, max(0, W // 2 - crop_w // 2), max(0, W - crop_w - 1)]
    sheet = Image.new('RGB', (min(crop_w, W), 3 * H + 20), 'white')
    for k, s in enumerate(starts):
        sheet.paste(marked.crop((s, 0, s + min(crop_w, W), H)), (0, k * (H + 10)))
    sheet.save(out_dir / 'check.png')
    return stats


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('score', help='score JSON (render_music.py format)')
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--height-px', type=int, default=460, help='height of strip.png (default 460)')
    ap.add_argument('--margin-px', type=int, default=10, help='white margin around the ink (default 10)')
    ap.add_argument('--gap-ss', type=float, default=3.0,
                    help='staff spaces given to the shortest distance between two onsets (default 3)')
    ap.add_argument('--check', action='store_true', help='also write check.png and measure accuracy')
    ap.add_argument('--keep-work', action='store_true', help='keep the SVG/PDF/page PNG in out-dir')
    a = ap.parse_args()
    info, extra = build_strip(a.score, a.out_dir, a.height_px, a.margin_px, a.gap_ss, a.keep_work)
    print(f'{a.out_dir}/strip.png: {info["width_px"]} x {info["height_px"]} px, '
          f'{len(info["time_to_x"])} time points, {len(info["staff_y"])} staves, '
          f'{len(info["entries"])} entries, {extra["dpi"]:.2f} dpi')
    if a.check:
        print(check(a.out_dir, info, extra))


if __name__ == '__main__':
    main()
