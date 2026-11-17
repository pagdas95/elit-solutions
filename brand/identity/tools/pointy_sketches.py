#!/usr/bin/env python3
"""Exploration: 'more pointy, shows it goes up' variants of the Layered E (client request, Nov 2026).

Same construction as mark.py (three slabs on an isometric lattice: a = up-right, b = down-right) with a variable
lattice angle. Writes brand/identity/explore-pointy/sketches.png. Nothing here replaces the approved files.
    .venv/bin/python brand/identity/tools/pointy_sketches.py
"""
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import package as P  # noqa: E402  (outlined wordmark, colours, renderer)

OUT = os.path.join(P.ID, "explore-pointy")
COLS = (P.CYAN, P.BLUE, P.VIOLET)

BASE = {  # the refined mark (v1.0-rc) for reference
    "top": [(0, 0), (4, -4), (14, -4), (14, 1.5), (10, 1.5), (10, 0)],
    "mid": [(-2, 2), (8, 2), (8, 6), (-4.5, 6), (-4.5, 4.5)],
    "bot": [(-4.5, 8), (-0.5, 8), (-0.5, 9.5), (3, 9.5), (3, 13.5), (-4.5, 13.5)],
}
# 1 · Blades: every slab ends in a sharp tip pointing up-right; the fold notches stay
BLADES = {
    "top": [(0, 0), (4, -4), (17, -4), (11, 1.5), (10, 1.5), (10, 0)],
    "mid": [(-2, 2), (12, 2), (6, 6), (-4.5, 6), (-4.5, 4.5)],
    "bot": [(-4.5, 8), (-0.5, 8), (-0.5, 9.5), (8, 9.5), (2, 13.5), (-4.5, 13.5)],
}
# 3 · Climb: tips step further out the higher the slab sits, like a rising chart
CLIMB = {
    "top": [(0, 0), (4, -4), (19, -4), (13, 1.5), (10, 1.5), (10, 0)],
    "mid": [(-2, 2), (12, 2), (6, 6), (-4.5, 6), (-4.5, 4.5)],
    "bot": [(-4.5, 8), (-0.5, 8), (-0.5, 9.5), (5, 9.5), (-1, 13.5), (-4.5, 13.5)],
}
# 4 · Wings: each slab tapers to a needle point (top and bottom edges converge)
WINGS = {
    "top": [(0, 0), (4, -4), (18, -4), (8, 0)],
    "mid": [(-2, 2), (14, 2), (4, 6), (-4.5, 6), (-4.5, 4.5)],
    "bot": [(-4.5, 8), (10, 8), (0, 12.5), (-4.5, 12.5)],
}
# 5 · Peak: one combined arrowhead; the top slab rises into a point, the others echo it
PEAK = {
    "top": [(0, 0), (4, -4), (12, -4), (17, -6.5), (14, 1.5), (10, 1.5), (10, 0)],
    "mid": [(-2, 2), (12, 2), (6, 6), (-4.5, 6), (-4.5, 4.5)],
    "bot": [(-4.5, 8), (-0.5, 8), (-0.5, 9.5), (8, 9.5), (2, 13.5), (-4.5, 13.5)],
}

VARIANTS = [
    ("0", "Current (v1.0-rc)", "For comparison: square ends, calm.", BASE, 30),
    ("1", "Blades", "Every slab ends in a sharp tip pointing up and to the right. Closest to the current mark.", BLADES, 30),
    ("2", "Blades · steeper", "Same blades on a steeper 40° angle: more lift, more speed.", BLADES, 40),
    ("3", "Climb", "Tips step further out from bottom to top, like a rising chart: growth.", CLIMB, 34),
    ("4", "Wings", "Each slab tapers to a needle point, like stacked wings or blades: the sharpest and most dynamic.", WINGS, 32),
    ("5", "Peak", "The top slab rises into a point above the others, like an arrow taking off.", PEAK, 32),
]


def xy(a, b, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return ((a + b) * c, (b - a) * s)


def symbol(pieces, deg, h, way="dark"):
    pts = [xy(a, b, deg) for ps in pieces.values() for a, b in ps]
    x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
    x1, y1 = max(p[0] for p in pts), max(p[1] for p in pts)
    k = h / (y1 - y0)
    cols = COLS if way == "dark" else ("#F4F7FF",) * 3
    polys = "".join(
        f'<polygon points="{" ".join(f"{(xy(a, b, deg)[0] - x0) * k:.2f},{(xy(a, b, deg)[1] - y0) * k:.2f}" for a, b in ps)}" fill="{c}"/>'
        for ps, c in zip(pieces.values(), cols))
    return polys, (x1 - x0) * k


def svg_symbol(pieces, deg, h, way="dark"):
    g, w = symbol(pieces, deg, h, way)
    return f'<svg viewBox="0 0 {w:.2f} {h}" style="height:{h}px;width:auto;display:block">{g}</svg>'


def svg_lockup(pieces, deg, way="dark"):
    """Symbol + ElIT over SOLUTIONS (same proportions as package.lockup primary)."""
    _, _, _, el_c, it_c, sol_c = P.WAYS["dark" if way == "dark" else "mono-white"]
    wx0, wy0, ww, wh = P.WVB
    cap, gap = 100.0, 30.0
    s_scale = ww / (P.SB[2] - P.SB[0])
    block = cap + gap + (P.SB[3] - P.SB[1]) * s_scale
    mh = block * 1.06
    g, mw = symbol(pieces, deg, mh, way)
    x = mw + 52
    word = (f'<g transform="translate({x - wx0:.2f} 0)"><path d="{P.EL}" fill="{el_c}"/><path d="{P.IT}" fill="{it_c}"/></g>'
            f'<g transform="translate({x:.2f} {cap + gap:.2f}) scale({s_scale:.5f}) translate({-P.SB[0]:.2f} {-P.SB[1]:.2f})">'
            f'<path d="{P.SOL}" fill="{sol_c}"/></g>')
    oy = -(mh - block) / 2
    return (f'<svg viewBox="0 {oy:.2f} {x + ww:.2f} {mh:.2f}" style="height:64px;width:auto;display:block">'
            f'<g transform="translate(0 {oy:.2f})">{g}</g>{word}</svg>')


def small_png(pieces, deg, px, name):
    g, w = symbol(pieces, deg, 100)
    side = max(w, 100) * 1.08
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{w / 2 - side / 2:.2f} {50 - side / 2:.2f} {side:.2f} {side:.2f}">'
           f'<rect x="-1000" y="-1000" width="3000" height="3000" fill="{P.MID}"/>{g}</svg>')
    p = os.path.join(OUT, f"{name}-{px}.png")
    P.cairosvg.svg2png(bytestring=svg.encode(), write_to=p, output_width=px, output_height=px)
    return os.path.basename(p)


def main():
    os.makedirs(OUT, exist_ok=True)
    cards = []
    for num, title, note, pieces, deg in VARIANTS:
        f16 = small_png(pieces, deg, 16, f"v{num}")
        f32 = small_png(pieces, deg, 32, f"v{num}")
        cards.append(f"""<div class="c{' cur' if num == '0' else ''}"><div class="n">{num}</div><div class="big">{svg_symbol(pieces, deg, 210)}</div>
<div class="row"><img src="{f32}" style="width:64px;height:64px"><img src="{f16}" style="width:48px;height:48px"><span>32 px · 16 px<br>(enlarged pixels)</span>
<div class="mono">{svg_symbol(pieces, deg, 56, "mono")}</div></div>
<div class="lk">{svg_lockup(pieces, deg)}</div><h3>{title}</h3><p>{note}</p></div>""")
    css = """.top{padding:40px 56px 10px}.top h1{font-size:40px;letter-spacing:-.02em}.top p{color:#9AA6C4;font-size:17px;margin-top:8px;max-width:1150px;line-height:1.55}
.g{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;padding:22px 56px 50px}
.c{position:relative;background:#0B1224;border:1px solid #1C2946;border-radius:18px;padding:26px}.c.cur{opacity:.72}
.n{position:absolute;left:20px;top:18px;width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,#36D9FF,#9174FF);color:#080D1B;font-weight:700;font-size:19px;display:flex;align-items:center;justify-content:center}
.big{height:250px;display:flex;align-items:center;justify-content:center}
.row{display:flex;align-items:center;gap:16px;margin-top:10px;color:#7C8AAD;font-size:11px;line-height:1.4}.row img{image-rendering:pixelated;border-radius:6px}
.mono{margin-left:auto;background:#17243B;border-radius:10px;padding:10px 14px}
.lk{margin-top:18px;padding:18px;background:#080D1B;border:1px solid #1C2946;border-radius:12px;display:flex;justify-content:center}
h3{font-size:22px;margin-top:18px}.c p{color:#B8C2DB;font-size:15px;line-height:1.55;margin-top:6px}"""
    body = (f'<div class="top"><h1>"More pointy, going up": five directions</h1><p>Same idea as before: three slabs, cyan to violet, '
            f'the same wordmark. What changes is the shape of the ends and the angle of the rise. Number 0 is the current '
            f'mark for comparison. Pick a number, or mix ("the tips of 4 with the angle of 2").</p></div><div class="g">{"".join(cards)}</div>')
    html = os.path.join(OUT, "sketches.html")
    P.write(html, P.page(body, css, 1600))
    P.render(html, os.path.join(OUT, "sketches.png"), 1600, 1000, full=True)


if __name__ == "__main__":
    main()
