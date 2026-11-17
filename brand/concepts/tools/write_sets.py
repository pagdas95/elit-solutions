#!/usr/bin/env python3
"""Writes the three Phase 1 concepts into the brand-identity work folder (sets.json).

Re-run after editing: python3 brand/concepts/tools/write_sets.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "..", "elit-solutions")


def face(family, weights, location, case="as-is", tracking=0, fallback="system-ui, sans-serif", features=None):
    return {"family": family, "source": "google", "license": "OFL-1.1", "weights": weights, "location": location,
            "features": features or [], "case": case, "tracking": tracking, "fallback": fallback, "file": None}


def brand(i, name, hexv, usage):
    return {"id": f"brand-{i}", "name": name, "hex": hexv, "source": "chosen", "locked": False, "usage": usage}


def logo(kind, concept, wordmark_tracking, colors, tags, symbol=True, min_px=20):
    return {"type": kind, "concept": concept, "symbol": "logo/symbol.svg" if symbol else None,
            "wordmark": {"text": "ElIT", "role": "display", "location": None, "tracking": wordmark_tracking,
                         "case": "as-is"},
            "monogram": None, "lockups": ["horizontal", "stacked"] if symbol else ["horizontal"],
            "colors": colors, "tags": tags,
            "clear_space": {"unit": "cap-height", "multiple": 1, "inferred": True},
            "min_size": {"px": min_px, "mm": 7}}


# ------------------------------------------------------------------ A · Signal
A_SYMBOL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<g id="frame" data-color="text">
<rect id="stem" x="12" y="10" width="18" height="80"/>
<rect id="arm-top" x="38" y="10" width="50" height="18"/>
<rect id="arm-bottom" x="38" y="72" width="50" height="18"/>
</g>
<rect id="arm-signal" x="38" y="41" width="36" height="18" data-color="primary"/>
</svg>"""

A = {
    "identity": {
        "set": {"id": "A", "name": "Signal", "recommended": True,
                "mechanism": "An E assembled from four separate bars, with the middle bar lit in cyan: precise modules plus one live signal. The same bar-and-gap rule sets the grid, the type and the glow.",
                "expression_move": "The cyan signal bar is the only bright thing, glowing on midnight.",
                "differs_by": "The references (Linear, Stripe) own indigo and violet; Vercel owns black and white. Signal holds midnight navy with cyan, a hue only about 2-12% of software marks use, and keeps violet to a faint glow."},
        "axes": {"warm_cool": 2, "classic_contemporary": 1, "quiet_loud": 1},
        "type": {"pairing_mode": "data-face",
                 "display": face("Moderustic", [700], {"wght": 700}, tracking=-25),
                 "text": face("Geologica", [400, 600], {"wght": 400}, features=["tnum"]),
                 "mono": face("JetBrains Mono", [400, 600], {"wght": 400}, fallback="ui-monospace, monospace",
                              features=["tnum"])},
        "logo": logo("symbol+wordmark",
                     "A segmented E: three arms and a stem that never touch, the middle arm lit. Software is built from parts that fit precisely; ElIT supplies the signal that makes them run.",
                     -25, {"frame": "text", "arm-signal": "primary", "wordmark": "text"}, ["abstract-geometric"]),
        "palette_build": {"strategy": None, "accent": None, "light_bg": None, "dark_bg": "#0B1531",
                          "neutral_tint": "#1B2A5C", "neutral_chroma": 0.04, "extra": []},
        "card": {"ground": "dark"},
        "defaults_used": [
            {"id": "navy-primary", "why": "The user asked for midnight navy. It is a dark ground here, not a finance-style primary, and cyan does the identifying."},
            {"id": "tech-indigo-violet", "why": "The user asked for a subtle violet. It is kept as a glow and chart colour only, never a primary or text colour, so it stays apart from Linear's and Stripe's indigo."}],
        "rationale": [
            {"claim": "Moderustic has no tabular figures, so Geologica carries running text and numbers, and JetBrains Mono carries code, which is native territory for a software company.", "evidence": "measured", "source": "brand.py build gate"},
            {"claim": "Every letter of ElIT (E, l, I, T) is made of straight bars, so a bar module is native to the name rather than imposed on it.", "evidence": "judgement"},
            {"claim": "Moderustic's lowercase l has a tail, so ElIT can't be misread as EIIT. Most geometric sans faces draw l and I identically.", "evidence": "measured", "source": "type specimen render"},
            {"claim": "Cyan is used in about 2-12% of marks in the logo library's developer, cloud and productivity categories; blue in 19-28%.", "evidence": "measured", "source": "logo-design search_library --summary"}],
    },
    "palette": {"schema": "brand-identity/palette@1", "name": "Signal",
                "direction": "Midnight navy grounds (#0B1531), one ion-cyan signal, a faint aurora violet glow.",
                "brand": [brand(1, "Ion Cyan", "#3DDCF4", "the signal bar, key actions, focus; never body text on white"),
                          brand(2, "Aurora Violet", "#8B7BFF", "glows, gradients, charts and secondary highlights; never a primary")],
                "feels": ["precise", "nocturnal", "live"]},
    "symbol_svg": A_SYMBOL, "symbol_small_svg": None, "wordmark_detail_svg": None,
}

A["identity"]["logo"]["misuse"] = [{"do": "stretch"}, {"do": "rotate"}, {"do": "effects"}, {"do": "low-contrast"},
                                  {"svg": "logo/misuse-1.svg", "label": "Do not close the gaps between the bars"},
                                  {"svg": "logo/misuse-2.svg", "label": "Do not light a different bar"}]
A["misuse_svgs"] = {
    "misuse-1": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><g data-color="text"><rect x="12" y="10" width="18" height="80"/><rect x="30" y="10" width="58" height="18"/><rect x="30" y="72" width="58" height="18"/></g><rect x="30" y="41" width="44" height="18" data-color="primary"/></svg>""",
    "misuse-2": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><g data-color="text"><rect x="12" y="10" width="18" height="80"/><rect x="38" y="41" width="36" height="18"/><rect x="38" y="72" width="50" height="18"/></g><rect x="38" y="10" width="50" height="18" data-color="primary"/></svg>""",
}

# ------------------------------------------------------------------ B · Frame
B_SYMBOL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<g id="brackets" data-color="text">
<polygon id="corner-tl" points="8,20 20,8 54,8 54,22 22,22 22,54 8,54"/>
<polygon id="corner-br" points="92,80 80,92 46,92 46,78 78,78 78,46 92,46"/>
</g>
<rect id="core" x="39" y="39" width="22" height="22" data-color="accent"/>
</svg>"""

B = {
    "identity": {
        "set": {"id": "B", "name": "Frame", "recommended": False,
                "mechanism": "Two chamfered corner brackets hold one ember core: ElIT is the frame that every product is built inside. The chamfer is cut from Tektur's angled corners, and the frame becomes the container for every future product.",
                "expression_move": "The ember core square is the only colour; everything else is graphite on concrete.",
                "differs_by": "The references are dark or blue-violet with soft gradients. Frame is light concrete with graphite and a single hot ember point, angular and engineered rather than glowing."},
        "axes": {"warm_cool": -1, "classic_contemporary": 2, "quiet_loud": -1},
        "type": {"pairing_mode": "contrast",
                 "display": face("Tektur", [600], {"wght": 600, "wdth": 100}, tracking=10),
                 "text": face("Sofia Sans", [400, 600], {"wght": 400}, features=["tnum"]),
                 "mono": None},
        "logo": logo("symbol+wordmark",
                     "Two chamfered brackets frame a core: the frame is the company, the core is whatever it builds. Each future product sits in the same frame with its own core colour.",
                     10, {"brackets": "text", "core": "accent", "wordmark": "text"}, ["abstract-geometric"]),
        "palette_build": {"strategy": None, "accent": None, "light_bg": "#F1F1EE", "dark_bg": None,
                          "neutral_tint": None, "neutral_chroma": None, "extra": []},
        "defaults_used": [],
        "rationale": [
            {"claim": "Tektur's capital I has slab serifs, so ElIT stays legible: the l is a plain stem, the I is serifed.", "evidence": "measured", "source": "type specimen render"},
            {"claim": "An umbrella brand needs a container: product marks reuse the brackets with their own core colour, so every product is visibly ElIT-built without sharing a name.", "evidence": "judgement"},
            {"claim": "Concrete grey plus graphite keeps the ground neutral; ember is the only hue (a single-accent structure).", "evidence": "judgement"}],
    },
    "palette": {"schema": "brand-identity/palette@1", "name": "Frame",
                "direction": "Graphite on concrete, one ember core.",
                "brand": [brand(1, "Graphite", "#17191F", "the frame, type, dark surfaces"),
                          brand(2, "Ember", "#FF5A1F", "the core, one action per screen")],
                "feels": ["engineered", "solid", "direct"]},
    "symbol_svg": B_SYMBOL, "symbol_small_svg": None, "wordmark_detail_svg": None,
}

# ------------------------------------------------------------------ C · Edition
C = {
    "identity": {
        "set": {"id": "C", "name": "Edition", "recommended": False,
                "mechanism": "A sharp high-contrast serif wordmark in cobalt ink, with one cobalt-weight overline floating above IT: software presented with an editorial, premium hand, and the IT inside the name underlined from above.",
                "expression_move": "The overline above IT in the serif wordmark; everything else stays porcelain, ink and cobalt.",
                "differs_by": "Every reference uses a sans-serif and a symbol. Edition is wordmark-only and serif, a rare position (wordmarks are 3-15% of the library's software marks), reading as studio and partner rather than another startup."},
        "axes": {"warm_cool": 1, "classic_contemporary": -1, "quiet_loud": -1},
        "type": {"pairing_mode": "superfamily",
                 "display": face("Noto Serif Display", [700], {"wght": 700, "wdth": 100}, tracking=-10,
                                 fallback="Georgia, serif"),
                 "text": face("Noto Sans", [400, 600], {"wght": 400, "wdth": 100}, features=["tnum"]),
                 "mono": None},
        "logo": logo("wordmark",
                     "ElIT set in a cut serif with a solid overline above IT: the name read as El + IT, a rule that later carries product names.",
                     -10, {"wordmark": "primary"}, [], symbol=False),
        "palette_build": {"strategy": None, "accent": None, "light_bg": "#F7F7F4", "dark_bg": None,
                          "neutral_tint": None, "neutral_chroma": None,
                          "extra": ["#5EF0C0:Signal Mint:status and data highlights on dark surfaces only"]},
        "defaults_used": [
            {"id": "navy-primary", "why": "Flagged on Ink #0E1124, a near-black text colour with a blue tint so it sits with cobalt. It is not used as a navy brand colour; cobalt is the identifying colour."}],
        "rationale": [
            {"claim": "Serifs distinguish the I from the l, so ElIT reads correctly in a serif without any trick.", "evidence": "measured", "source": "type specimen render"},
            {"claim": "Wordmark-only marks are 3-15% of the library's developer, cloud and productivity logos, so this is an open position on the shelf.", "evidence": "measured", "source": "logo-design search_library --summary"},
            {"claim": "A single deep cobalt as ink (rather than as a large surface) keeps the palette quiet so the type can speak.", "evidence": "judgement"}],
    },
    "palette": {"schema": "brand-identity/palette@1", "name": "Edition",
                "direction": "Cobalt ink on porcelain, with a small signal mint for live data.",
                "brand": [brand(1, "Cobalt", "#1838C9", "wordmark, links, primary actions"),
                          brand(2, "Ink", "#0E1124", "type, dark sections")],
                "feels": ["assured", "editorial", "exact"]},
    "symbol_svg": None,
    "symbol_small_svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path id="initial" data-glyphs="E" data-cap="70" data-x="50" data-baseline="85" data-anchor="middle" data-color="primary"/></svg>""",
    "wordmark_detail_svg": None,
}

if __name__ == "__main__":
    sets = [A, B, C]
    detail = os.path.join(HERE, "details.json")
    if os.path.isfile(detail):  # wordmark details measured from wordmark-glyphs.json after the first logos run
        with open(detail) as fh:
            d = json.load(fh)
        for s in sets:
            sid = s["identity"]["set"]["id"]
            for k, v in (d.get(sid) or {}).items():
                s[k] = v
    with open(os.path.join(WORK, "sets.json"), "w", encoding="utf-8") as fh:
        json.dump({"schema": "brand-identity/sets@1", "sets": sets}, fh, indent=2, ensure_ascii=False)
    print("wrote", os.path.normpath(os.path.join(WORK, "sets.json")))
