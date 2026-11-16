#!/usr/bin/env python3
"""Round 2 (logo refinement on Concept A's system): two symbol directions on the client palette.

Client palette (exploratory): Midnight #080D1B, Navy #17243B, Cyan #36D9FF, Violet #9174FF, Ice White #F4F7FF.
Run: .venv/bin/python brand/concepts/round-2/tools/write_sets.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "..", "elit-solutions")


def face(family, weights, location, tracking=0, fallback="system-ui, sans-serif", features=None):
    return {"family": family, "source": "google", "license": "OFL-1.1", "weights": weights, "location": location,
            "features": features or [], "case": "as-is", "tracking": tracking, "fallback": fallback, "file": None}


TYPE = {"pairing_mode": "contrast",
        "display": face("Lexend", [700], {"wght": 700}, tracking=-10),
        "text": face("Geologica", [400, 600], {"wght": 400}, features=["tnum"]),
        "mono": face("JetBrains Mono", [400], {"wght": 400}, fallback="ui-monospace, monospace", features=["tnum"])}

PALETTE_BUILD = {"strategy": None, "accent": None, "light_bg": "#F4F7FF", "dark_bg": "#080D1B",
                 "neutral_tint": "#17243B", "neutral_chroma": 0.04,
                 "extra": ["#17243B:Navy:dark surfaces and cards on Midnight",
                           "#5FA2FF:Layer Blue:middle step of the cyan-to-violet ramp (marks and charts only)"]}


def palette(name, direction):
    return {"schema": "brand-identity/palette@1", "name": name, "direction": direction,
            "brand": [{"id": "brand-1", "name": "Cyan", "hex": "#36D9FF", "source": "chosen", "locked": False,
                       "usage": "the mark, key actions, highlights; fill only on light grounds"},
                      {"id": "brand-2", "name": "Violet", "hex": "#9174FF", "source": "chosen", "locked": False,
                       "usage": "the second voice of the mark, glows, charts"}],
            "feels": ["precise", "forward", "premium"]}


def logo(concept, colors, tags):
    return {"type": "symbol+wordmark", "concept": concept, "symbol": "logo/symbol.svg",
            "wordmark": {"text": "ElIT", "role": "display", "location": None, "tracking": -10, "case": "as-is"},
            "monogram": None, "lockups": ["horizontal", "stacked"], "colors": colors, "tags": tags,
            "clear_space": {"unit": "cap-height", "multiple": 1, "inferred": True},
            "min_size": {"px": 20, "mm": 7}}


# ------------------------------------------------------------------ Forward: an E that becomes an arrow
# Stroked outline of a chevron, open at the inner apex; the violet middle bar runs through the opening.
# Stroke 12 on the 100 grid; inner diagonals parallel to the outer ones (computed, not eyeballed).
W = 12
TL, TR, TIP = (20.0, 14.0), (58.0, 14.0), (92.0, 50.0)
dx, dy = TIP[0] - TR[0], TIP[1] - TR[1]
k = (33.0 - TL[1]) / dy                     # inner diagonal ends at y = 33, leaving a gap above the bar
IN_T = (TL[0] + dx * k, TL[1] + dy * k)
IN_B = (IN_T[0], 100 - IN_T[1])
f = lambda p: f"{p[0]:.2f} {p[1]:.2f}"
FORWARD = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<path id="chevron" data-color="brand-1" fill="none" stroke="#000" stroke-width="{W}" stroke-linejoin="round" stroke-linecap="butt"
 d="M{f(IN_T)} L{f(TL)} L{f(TR)} L{f(TIP)} L{f((TR[0], 100 - TR[1]))} L{f((TL[0], 100 - TL[1]))} L{f(IN_B)}"/>
<rect id="bar" data-color="brand-2" x="4" y="44" width="60" height="12" rx="6"/>
</svg>"""

# ------------------------------------------------------------------ Layers: the segmented E, sheared into depth
m, t, g, x0 = 0.30, 16.0, 7.0, 12.0     # slope, slab thickness, gap, left edge


def slab(y_left_top, x1):
    rise = m * (x1 - x0)
    return (f"{x0},{y_left_top:.2f} {x1},{y_left_top - rise:.2f} {x1},{y_left_top - rise + t:.2f} "
            f"{x0},{y_left_top + t:.2f}")


x0 = 32.0                               # arms start after the spine (x 12-24) and a gap of 8
y = 28.0
LAYERS = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<rect id="spine" data-color="text" x="12" y="{y:.2f}" width="13" height="{3 * t + 2 * g:.2f}"/>
<polygon id="layer-top" data-color="brand-1" points="{slab(y, 90)}"/>
<polygon id="layer-mid" data-color="ext-2" points="{slab(y + t + g, 76)}"/>
<polygon id="layer-bottom" data-color="brand-2" points="{slab(y + 2 * (t + g), 90)}"/>
</svg>"""

SETS = [
    {"identity": {
        "set": {"id": "A", "name": "Forward", "recommended": False,
                "mechanism": "An E that turns into an arrow: the top and bottom arms fold into a chevron, and the violet middle bar runs through the opening. The company delivers, and the letter shows the motion.",
                "expression_move": "The violet bar crossing into the cyan chevron.",
                "differs_by": "Arrows are common, so this one is drawn as a letter first (E arms plus bar), with an open inner apex no stock arrow icon has."},
        "axes": {"warm_cool": 2, "classic_contemporary": 2, "quiet_loud": 1},
        "type": TYPE,
        "logo": logo("The E in motion: arms become a chevron, the middle arm becomes the shaft.",
                     {"chevron": "brand-1", "bar": "brand-2", "wordmark": "text"}, ["abstract-geometric"]),
        "palette_build": PALETTE_BUILD,
        "card": {"ground": "dark"},
        "defaults_used": [{"id": "tech-indigo-violet", "why": "Client palette: violet is requested and used as the second voice of the mark, not as a primary."}],
        "rationale": [{"claim": "Client direction from reference images: forward-movement mark, cyan plus violet on midnight.", "evidence": "practice", "source": "client references, 16 Nov 2026"},
                      {"claim": "Lexend's slab-serifed capital I keeps ElIT from reading as EIIT, even in one colour.", "evidence": "measured", "source": "wordmark specimen render"}]},
     "palette": palette("Forward", "Client palette: midnight and navy grounds, cyan mark, violet second voice."),
     "symbol_svg": FORWARD, "symbol_small_svg": None, "wordmark_detail_svg": None},
    {"identity": {
        "set": {"id": "B", "name": "Layers", "recommended": False,
                "mechanism": "Phase 1's segmented E, given depth: a neutral spine and three separate slabs, sheared upward and stepping from cyan through blue to violet. Layers of a system, built one on another, with the gradient made of flat steps.",
                "expression_move": "The three-step colour ramp across the slabs.",
                "differs_by": "Isometric layer marks are common in cloud and dev tools; this one keeps the gaps and the short middle arm, so it reads as E first and stack second."},
        "axes": {"warm_cool": 2, "classic_contemporary": 2, "quiet_loud": 1},
        "type": TYPE,
        "logo": logo("Three slabs of a system stacked into an E, cyan to violet in flat steps.",
                     {"spine": "text", "layer-top": "brand-1", "layer-mid": "ext-2", "layer-bottom": "brand-2", "wordmark": "text"},
                     ["abstract-geometric"]),
        "palette_build": PALETTE_BUILD,
        "card": {"ground": "dark"},
        "defaults_used": [{"id": "tech-indigo-violet", "why": "Client palette: violet is requested and used as the last step of the mark's ramp, not as a primary."}],
        "rationale": [{"claim": "Client direction from reference images: layered E, cyan-to-violet.", "evidence": "practice", "source": "client references, 16 Nov 2026"},
                      {"claim": "The gradient is quantised into three flat steps, so the master works in print, embroidery and one colour; a smooth gradient is an optional digital treatment.", "evidence": "judgement"}]},
     "palette": palette("Layers", "Client palette: midnight and navy grounds, cyan-to-violet ramp in three steps."),
     "symbol_svg": LAYERS, "symbol_small_svg": None, "wordmark_detail_svg": None},
]

if __name__ == "__main__":
    with open(os.path.join(WORK, "sets.json"), "w", encoding="utf-8") as fh:
        json.dump({"schema": "brand-identity/sets@1", "sets": SETS}, fh, indent=2, ensure_ascii=False)
    print("inner apex ends:", IN_T, IN_B)
