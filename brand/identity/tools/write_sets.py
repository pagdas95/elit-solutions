#!/usr/bin/env python3
"""ElIT Solutions identity v1.0 (release candidate): the client's Layered E, refined.

Writes brand/identity/elit-solutions/sets.json for the brand-identity pipeline. The wordmark detail (IT in cyan) is
read from the first `logos` run, so run: write_sets.py -> brand.py logos -> write_sets.py -> brand.py logos/build/kit.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "..", "elit-solutions")
sys.path.insert(0, HERE)
import mark  # noqa: E402


def face(family, weights, location, tracking=0, fallback="system-ui, sans-serif", features=None):
    return {"family": family, "source": "google", "license": "OFL-1.1", "weights": weights, "location": location,
            "features": features or [], "case": "as-is", "tracking": tracking, "fallback": fallback, "file": None}


def it_detail():
    """'IT' outlines from the built wordmark, re-added as a cyan coloured detail (same coordinates)."""
    p = os.path.join(WORK, "sets", "A", "logo", "build", "master-wordmark.svg")
    g = os.path.join(WORK, "sets", "A", "logo", "build", "wordmark-glyphs.json")
    cache = os.path.join(HERE, "it-detail.svg")
    if os.path.isfile(cache):               # measured once from the plain wordmark; later builds knock IT out
        return open(cache).read()
    if not (os.path.isfile(p) and os.path.isfile(g)):
        return None
    svg = open(p).read()
    glyphs = json.load(open(g))["glyphs"]
    cut = (glyphs[1]["x1"] + glyphs[2]["x0"]) / 2
    d = " ".join(re.findall(r'<path(?![^>]*data-parts="wordmark-detail)[^>]*\sd="([^"]+)"', svg))
    it = [s.strip() for s in re.findall(r"M[^M]+", d)
          if min(float(v) for v in re.findall(r"-?\d+\.?\d*", s)[0::2]) > cut]
    if not it:
        return None
    out = '<svg xmlns="http://www.w3.org/2000/svg"><path id="it" data-color="ext-3" d="' + " ".join(it) + '"/></svg>'
    with open(cache, "w") as fh:
        fh.write(out)
    return out


MARK = {"layer-top": "ext-3", "layer-mid": "ext-4", "layer-bottom": "ext-5"}
SYMBOL = mark.symbol_svg(MARK)

# Misuses only this mark can suffer (drawn from the real geometry)


def misuse_gapless():
    """The gaps closed: slabs pushed together so the E reads as one blob."""
    saved = {k: list(v) for k, v in mark.PIECES.items()}
    try:
        mark.PIECES["layer-mid"] = [(a, b - 1.6) for a, b in saved["layer-mid"]]
        mark.PIECES["layer-bottom"] = [(a, b - 3.2) for a, b in saved["layer-bottom"]]
        return mark.symbol_svg(MARK)
    finally:
        mark.PIECES.update(saved)


def misuse_reordered():
    """Colour ramp reversed (violet on top): the light-to-deep order is part of the mark."""
    return mark.symbol_svg({"layer-top": "ext-5", "layer-mid": "ext-4", "layer-bottom": "ext-3"})


SET = {
    "identity": {
        "set": {"id": "A", "name": "Layered E", "recommended": True,
                "mechanism": "An isometric E folded from three slabs, stepping cyan to blue to violet: a system built in layers. Every edge sits on the 30-degree isometric grid, with one gap between all slabs.",
                "expression_move": "The three-step colour ramp across the slabs; everything else is midnight, navy and ice white.",
                "differs_by": "Software-studio marks are mostly flat glyphs or arrows; the isometric fold gives depth with flat colour, and the IT in cyan says what the company does."},
        "axes": {"warm_cool": 2, "classic_contemporary": 2, "quiet_loud": 1},
        "type": {"pairing_mode": "contrast",
                 "display": face("Lexend", [700], {"wght": 700}, tracking=-10),
                 "text": face("Geologica", [400, 600], {"wght": 400}, features=["tnum"]),
                 "mono": face("JetBrains Mono", [400], {"wght": 400}, fallback="ui-monospace, monospace", features=["tnum"])},
        "logo": {"type": "symbol+wordmark",
                 "concept": "The client's layered E, regularised on an isometric lattice: three slabs, one gap, two equal fold notches.",
                 "symbol": "logo/symbol.svg",
                 "wordmark": {"text": "ElIT", "role": "display", "location": None, "tracking": -10, "case": "as-is"},
                 "monogram": None, "lockups": ["horizontal", "stacked"],
                 "colors": {"layer-top": "ext-3", "layer-mid": "ext-4", "layer-bottom": "ext-5", "wordmark": "text", "it": "ext-3"},
                 "tags": ["abstract-geometric"],
                 "clear_space": {"unit": "cap-height", "multiple": 1, "inferred": True},
                 "min_size": {"px": 20, "mm": 7},
                 "misuse": [{"do": "stretch"}, {"do": "rotate"}, {"do": "effects"}, {"do": "low-contrast"},
                            {"svg": "logo/misuse-1.svg", "label": "Do not close the gaps between the slabs"},
                            {"svg": "logo/misuse-2.svg", "label": "Do not reverse the colour order"}]},
        "palette_build": {"strategy": None, "accent": None, "light_bg": "#F4F7FF", "dark_bg": "#080D1B",
                          "neutral_tint": "#17243B", "neutral_chroma": 0.04,
                          "extra": ["#080D1B:Midnight:the brand ground (60% of every dark layout)",
                                    "#17243B:Navy:surfaces and cards on Midnight",
                                    "#0A86B0:Deep Cyan:mark and IT on light grounds (Cyan #36D9FF on dark)",
                                    "#2F6BE0:Deep Blue:middle slab on light grounds (Layer Blue #5FA2FF on dark)",
                                    "#6A4BEB:Deep Violet:bottom slab on light grounds (Violet #9174FF on dark)"]},
        "card": {"ground": "dark"},
        "defaults_used": [
            {"id": "tech-indigo-violet", "why": "Client palette and client mark: violet is the last step of the mark's ramp, never a UI primary."},
            {"id": "navy-primary", "why": "Client palette: Midnight and Navy are grounds; Cyan is the identifying colour."}],
        "rationale": [
            {"claim": "Mark refined from the client's own kit (Nov 2026): same silhouette, rebuilt on a true isometric lattice with one gap (2 units) and equal fold notches (1.5 units). The original had gaps from 0.5 to 2 units.", "evidence": "measured", "source": "contour extraction of the client's one-colour logo"},
            {"claim": "Lexend's slab-serifed capital I keeps ElIT from reading as EIIT in one colour; the client kit's wordmark read EIIT.", "evidence": "measured", "source": "wordmark specimen render"},
            {"claim": "Lexend is the logo face only (outlined, Latin letters); Geologica covers Greek and tabular figures for all running text.", "evidence": "measured", "source": "brand.py fonts audit"}],
    },
    "palette": {"schema": "brand-identity/palette@1", "name": "Layered E",
                "direction": "Client palette: Midnight #080D1B and Navy #17243B grounds, Cyan #36D9FF to Violet #9174FF, Ice White #F4F7FF type.",
                "brand": [{"id": "brand-1", "name": "Cyan", "hex": "#36D9FF", "source": "chosen", "locked": True,
                           "usage": "top slab, IT, key actions; a fill on light grounds, never text"},
                          {"id": "brand-2", "name": "Violet", "hex": "#9174FF", "source": "chosen", "locked": True,
                           "usage": "bottom slab, glows, secondary highlights"}],
                "feels": ["precise", "layered", "premium"]},
    "symbol_svg": SYMBOL, "symbol_small_svg": None,
    "wordmark_detail_svg": None,
    "misuse_svgs": {"misuse-1": misuse_gapless(), "misuse-2": misuse_reordered()},
}

if __name__ == "__main__":
    SET["wordmark_detail_svg"] = it_detail()
    with open(os.path.join(WORK, "sets.json"), "w", encoding="utf-8") as fh:
        json.dump({"schema": "brand-identity/sets@1", "sets": [SET]}, fh, indent=2, ensure_ascii=False)
    print("wrote sets.json · IT detail:", "yes" if SET["wordmark_detail_svg"] else "not yet (run logos, then again)")
