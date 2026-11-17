#!/usr/bin/env python3
"""The ElIT layered-E mark, rebuilt on a true isometric lattice (refined from the client's kit, Nov 2026).

Lattice: a point is a*U + b*V with U = (cos30, -1/2) (up-right) and V = (cos30, +1/2) (down-right); every edge is
vertical or at +/-30 degrees. One gap (G) between all slabs; both fold notches equal N.
"""
import math

C = math.cos(math.radians(30))
G = 2.0                                   # the one gap between slabs, in lattice units
N = 1.5                                   # both fold notches
PIECES = {                                # (a, b) lattice corners, clockwise
    "layer-top": [(0, 0), (4, -4), (14, -4), (14, N), (10, N), (10, 0)],
    "layer-mid": [(-G, G), (8, G), (8, 6), (-4.5, 6), (-4.5, 4.5)],
    "layer-bottom": [(-4.5, 6 + G), (-0.5, 6 + G), (-0.5, 6 + G + N), (3, 6 + G + N), (3, 13.5), (-4.5, 13.5)],
}


def xy(a, b):
    return ((a + b) * C, (b - a) * 0.5)


def bbox():
    pts = [xy(*p) for ps in PIECES.values() for p in ps]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def symbol_svg(colors=None, size=100.0, pad=0.0):
    """Polygons on a size x size viewBox, the mark centred and scaled to fit (pipeline symbol format)."""
    colors = colors or {"layer-top": "brand-1", "layer-mid": "ext-2", "layer-bottom": "brand-2"}
    x0, y0, x1, y1 = bbox()
    k = (size - 2 * pad) / max(x1 - x0, y1 - y0)
    ox = (size - (x1 - x0) * k) / 2 - x0 * k
    oy = (size - (y1 - y0) * k) / 2 - y0 * k
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size:g} {size:g}">']
    for pid, ps in PIECES.items():
        pts = " ".join(f"{xy(*p)[0] * k + ox:.3f},{xy(*p)[1] * k + oy:.3f}" for p in ps)
        out.append(f'<polygon id="{pid}" data-color="{colors[pid]}" points="{pts}"/>')
    return "\n".join(out + ["</svg>"])


if __name__ == "__main__":
    print(symbol_svg())
