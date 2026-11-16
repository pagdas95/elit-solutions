#!/usr/bin/env python3
"""Phase 1 presentation: per-concept boards, application mocks and the comparison board.

Inputs come from the brand-identity work folder (brand/concepts/elit-solutions): outlined logo SVGs,
palette.json and the identity fonts. Run after `brand.py build`:

    .venv/bin/python brand/concepts/tools/boards.py
"""
import json
import os
import random
import re
import shutil
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CONCEPTS = os.path.join(ROOT, "brand", "concepts")
WORK = os.path.join(CONCEPTS, "elit-solutions")
SKILL = os.path.join(ROOT, ".claude", "skills", "brand-identity", "scripts")
PY = os.path.join(ROOT, ".venv", "bin", "python")
sys.path.insert(0, SKILL)
import site_preview  # noqa: E402  (identity_fonts_css: @font-face with the set's own fonts)

MONO_LINK = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600'
             '&display=block">')


def T(s, **kw):
    for k, v in kw.items():
        s = s.replace("{{" + k + "}}", str(v))
    return s


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(s)


def paint(svg, colors, cls="", style=""):
    """Inline an outlined master SVG, painting every data-color role from `colors`."""
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg)

    def fill(m):
        role = m.group(1)
        return f'data-color="{role}" fill="{colors.get(role, colors.get("*", "#000"))}"'
    svg = re.sub(r'data-color="([^"]+)"', fill, svg)
    svg = re.sub(r"<svg\b", f'<svg class="{cls}" style="{style}" preserveAspectRatio="xMidYMid meet"', svg, count=1)
    return svg


def asset(sid, name):
    return read(os.path.join(WORK, "sets", sid, "logo", "build", name))


def render(html_path, png_path, width, height=None, full=False, scale=1):
    cmd = [PY, os.path.join(SKILL, "render_png.py"), html_path, "-o", png_path, "--width", str(width),
           "--scale", str(scale)]
    if height:
        cmd += ["--height", str(height)]
    if full:
        cmd += ["--full-page"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if r.returncode:
        raise RuntimeError(r.stdout + r.stderr)
    print("  ", os.path.relpath(png_path, ROOT))


# ============================================================================ concept data

def palette(sid):
    return json.load(open(os.path.join(WORK, "sets", sid, "palette.json")))


def fonts(sid):
    d = os.path.join(WORK, "sets", sid)
    css, _ = site_preview.identity_fonts_css(d, json.load(open(os.path.join(d, "identity.json"))))
    return css


A = dict(
    id="A", slug="A-signal", name="Signal", recommended=True,
    one_liner="Precise modules, one live signal.",
    idea=("ElIT is spelled only with straight bars: E, l, I, T. Signal turns that into the whole identity. "
          "The E is built from four bars that never touch, and the middle one is lit in ion cyan. Software is "
          "made of parts that fit precisely; ElIT supplies the signal that makes them run."),
    personality=["Precise", "Nocturnal", "Live", "Confident"],
    fit=("Closest to your stated taste (midnight navy, cyan, a hint of violet), executed with restraint so it reads "
         "premium rather than generic \"tech gradient\". Cyan is rare in software marks (about 2-12% in the "
         "logo-design library's tech categories), so the signal bar can become ownable."),
    bg="#0B1531", bg2="#070D20", surface="#121C3A", line="#22305A", fg="#F1F3F7", muted="#9BA6C2",
    brand="#3DDCF4", accent="#8B7BFF", on_brand="#06101F",
    light_bg="#F6F8FC", light_fg="#141B2E",
    swatches=[("Midnight", "#0B1531", "Ground · app chrome · 60%"), ("Deep Space", "#070D20", "Deepest ground, footers"),
              ("Ion Cyan", "#3DDCF4", "The signal · actions · focus"), ("Aurora Violet", "#8B7BFF", "Glow, charts · never text"),
              ("Cloud", "#F1F3F7", "Type on dark, light surfaces"), ("Slate", "#4D556A", "Secondary text on light")],
    display="BI display a", text="BI text a", mono="'JetBrains Mono', ui-monospace, monospace",
    type_pair=("Moderustic Bold", "Geologica", "JetBrains Mono"),
    type_note=("Moderustic's lowercase l carries a tail, so ElIT never reads as EIIT. Geologica handles running text "
               "and tabular figures; JetBrains Mono is the code and data voice."),
    strengths=["Most on-brief: modern, bold, premium, tech-native.",
               "Symbol is built from the name's own geometry (all-straight letters), so it is not an imported icon.",
               "Works at 16 px; segmentation survives as a crisp E.",
               "Bar module scales into a product alphabet: E, F, L, H, T are all bar letters."],
    weaknesses=["Dark navy plus cyan is the most familiar territory of the three. Distinctiveness relies on the "
                "segmented E and on discipline (no gradients on the mark).",
                "Cyan fails contrast as text on white: on light pages it is a fill colour only, never type.",
                "The symbol and wordmark both start with E, so the horizontal lockup says \"E ElIT\". Use the "
                "symbol alone for app icons and the wordmark alone for small text."],
    scalability=("Every product gets a bar-built initial (F for Flow, L for Ledger, H for Hub) with its own lit bar. "
                 "The family reads as one system while each product owns a letter."),
    products=[("Flow", "automation"), ("Ledger", "invoicing"), ("Hub", "integrations")],
)

B = dict(
    id="B", slug="B-frame", name="Frame", recommended=False,
    one_liner="The frame every product is built in.",
    idea=("ElIT is an umbrella: it builds things and will own products. Frame makes that the logo. Two chamfered "
          "corner brackets hold a single ember core: the brackets are the company, the core is whatever it builds. "
          "Every future product sits in the same frame with its own core."),
    personality=["Engineered", "Direct", "Solid", "Warm-bold"],
    fit=("The most strategic for the umbrella model: the frame is a container system as well as a logo. It deliberately "
         "steps away from navy and cyan, using graphite on concrete with one ember point, so it stands apart from "
         "Linear, Stripe and Vercel."),
    bg="#F1F1EE", bg2="#E7E7E4", surface="#FFFFFF", line="#D1D0CA", fg="#17191F", muted="#5B5D63",
    brand="#17191F", accent="#FF5A1F", on_brand="#FFFFFF",
    light_bg="#F1F1EE", light_fg="#17191F",
    swatches=[("Concrete", "#F1F1EE", "Ground · 55%"), ("Graphite", "#17191F", "Frame, type, dark sections"),
              ("Ember", "#FF5A1F", "The core · one action per screen"), ("Steel", "#70737C", "Secondary text, rules"),
              ("Paper", "#FFFFFF", "Cards, surfaces"), ("Ember Deep", "#B13706", "Ember as text or link on light")],
    display="BI display b", text="BI text b", mono="'JetBrains Mono', ui-monospace, monospace",
    type_pair=("Tektur SemiBold", "Sofia Sans", None),
    type_note=("Tektur's chamfered corners match the symbol and its slab-serifed capital I separates it from the l. "
               "The l is given a tall chamfered ascender in the wordmark. Sofia Sans is a calm, tabular text "
               "face, so the display face can be loud."),
    strengths=["Strongest umbrella logic: products live inside the frame, visibly ElIT-built.",
               "Most distinctive palette against the reference set; ember is energetic but rationed.",
               "Angular chamfer language is consistent across mark, type and UI.",
               "Very robust at 16 px (thick brackets, solid core)."],
    weaknesses=["Corner brackets echo the \"select / expand\" UI glyph, so it needs the chamfer and core to stay ownable.",
                "Tektur is characterful; in long headlines it can feel game-like. Use it for short display lines only.",
                "Ember at 2.8:1 on concrete is a fill colour only; ember text uses Ember Deep #B13706."],
    scalability=("Each product keeps the frame and changes its core: shape stays square, colour changes "
                 "(Flow teal, Ledger violet, Hub amber). Co-branding for client work: the client's logo inside "
                 "ElIT's frame."),
    products=[("Flow", "automation"), ("Ledger", "invoicing"), ("Hub", "integrations")],
)

C = dict(
    id="C", slug="C-edition", name="Edition", recommended=False,
    one_liner="Software, with an editor's hand.",
    idea=("Every reference brand speaks in sans-serif and symbols. Edition speaks like a premium studio: a sharp "
          "high-contrast serif wordmark in cobalt ink, with one solid overline above IT, so the name reads El + IT. "
          "The overline becomes the system's only graphic device: it carries headings, product names and data."),
    personality=["Assured", "Editorial", "Exact", "Quietly bold"],
    fit=("The creative wildcard. It answers \"premium and trustworthy\" through craft and typography rather than "
         "tech tropes, and positions ElIT as a senior partner rather than another startup. It is the furthest from "
         "your stated colours; cobalt replaces navy and cyan."),
    bg="#F7F7F4", bg2="#EDEDEA", surface="#FFFFFF", line="#D6D6D0", fg="#0E1124", muted="#505561",
    brand="#1838C9", accent="#5EF0C0", on_brand="#FFFFFF",
    light_bg="#F7F7F4", light_fg="#0E1124",
    swatches=[("Porcelain", "#F7F7F4", "Ground · 60%"), ("Ink", "#0E1124", "Type, dark sections"),
              ("Cobalt", "#1838C9", "Wordmark, overlines, actions"), ("Cobalt Light", "#6892FB", "Cobalt on dark"),
              ("Signal Mint", "#5EF0C0", "Live data on dark only"), ("Stone", "#D6D6D0", "Hairlines, rules")],
    display="BI display c", text="BI text c", mono="'JetBrains Mono', ui-monospace, monospace",
    type_pair=("Noto Serif Display Bold", "Noto Sans", None),
    type_note=("A superfamily: serif display and sans text share one skeleton. The serif's I has serifs and its l "
               "has a flag, so ElIT reads correctly with no trick. Display sizes only (hairlines vanish below about "
               "24 px); Noto Sans does everything small."),
    strengths=["Most distinctive positioning: no symbol, no tech clichés, an uncommon serif for software.",
               "Feels expensive and senior; strong for consulting-style custom software work.",
               "The overline is a simple, ownable device that extends to every product and heading.",
               "Quiet palette: one hue (cobalt) plus ink and porcelain; mint only for live data."],
    weaknesses=["Weakest at small sizes: hairlines vanish and the 16 px favicon reads as a T. It needs a dedicated "
                "small mark in refinement.",
                "Less \"futuristic\" than requested (closer to 90/10 modern/creative than 70/30).",
                "Serif tech can read as agency or editorial rather than product company if overused."],
    scalability=("Products become editions: each product name is set in the serif under the cobalt overline, "
                 "endorsed \"by ElIT\". Elegant for a portfolio of products, but each product then lacks its own "
                 "icon until one is designed."),
    products=[("Flow", "automation"), ("Ledger", "invoicing"), ("Hub", "integrations")],
)
CONCEPT_LIST = [A, B, C]


# ============================================================================ marks per concept

def marks(c, on="dark"):
    """Return painted SVG strings: symbol, lockup (horizontal), stacked, wordmark, small."""
    sid = c["id"]
    if c is A:
        ink = c["fg"] if on == "dark" else c["light_fg"]
        cols = {"text": ink, "primary": c["brand"], "accent": c["brand"], "*": ink}
    elif c is B:
        ink = c["fg"] if on == "light" else "#F1F1EE"
        cols = {"text": ink, "primary": ink, "accent": c["accent"], "*": ink}
    else:
        ink = c["brand"] if on == "light" else "#F7F7F4"
        cols = {"text": ink, "primary": ink, "accent": ink, "*": ink}
    out = {"wordmark": paint(asset(sid, "master-wordmark.svg"), cols, "wm")}
    if sid in ("A", "B"):
        out["symbol"] = paint(asset(sid, "master-symbol.svg"), cols, "sym")
        out["lockup"] = paint(asset(sid, "master-lockup-horizontal.svg"), cols, "lk")
        out["stacked"] = paint(asset(sid, "master-lockup-stacked.svg"), cols, "st")
    else:
        out["symbol"] = paint(asset(sid, "master-symbol-small.svg"), cols, "sym")
        out["lockup"] = out["wordmark"]
        out["stacked"] = out["wordmark"]
    return out


def mono_marks(c, color):
    sid = c["id"]
    cols = {"*": color}
    if sid == "C":
        return paint(asset(sid, "master-wordmark.svg"), cols, "wm"), paint(asset(sid, "master-symbol-small.svg"), cols, "sym")
    return paint(asset(sid, "master-lockup-horizontal.svg"), cols, "lk"), paint(asset(sid, "master-symbol.svg"), cols, "sym")


# ---------------------------------------------------------------------------- patterns

def pattern_svg(c, w=1200, h=600, seed=7, dense=1.0):
    rnd = random.Random(seed)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    if c is A:
        out.append(f'<defs><radialGradient id="g{seed}" cx="78%" cy="18%" r="70%"><stop offset="0" stop-color="#8B7BFF" '
                   f'stop-opacity=".30"/><stop offset=".55" stop-color="#8B7BFF" stop-opacity="0"/></radialGradient></defs>')
        out.append(f'<rect width="{w}" height="{h}" fill="#0B1531"/><rect width="{w}" height="{h}" fill="url(#g{seed})"/>')
        u, t, g = 26, 12, 8  # unit length, bar thickness, gap
        y = 18
        while y < h:
            x = -rnd.randint(0, 60)
            while x < w:
                n = rnd.choice([1, 1, 2, 2, 3, 5, 8])
                bw = n * u
                r = rnd.random()
                if r < 0.05 * dense:
                    fill, op = "#3DDCF4", 1
                elif r < 0.075 * dense:
                    fill, op = "#8B7BFF", .85
                else:
                    fill, op = "#F1F3F7", rnd.choice([.04, .06, .09])
                out.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{t}" fill="{fill}" fill-opacity="{op}"/>')
                x += bw + g
            y += t + 14
    elif c is B:
        out.append(f'<rect width="{w}" height="{h}" fill="#F1F1EE"/>')
        s = 80
        for gx in range(0, w + s, s):
            for gy in range(0, h + s, s):
                a = 10
                out.append(f'<path d="M{gx-a} {gy}H{gx+a}M{gx} {gy-a}V{gy+a}" stroke="#17191F" stroke-opacity=".18" stroke-width="1.5"/>')
        for _ in range(int(7 * dense)):
            cx, cy = rnd.randrange(0, w // s) * s, rnd.randrange(0, h // s) * s
            sz = rnd.choice([1, 2, 2, 3]) * s
            out.append(bracket_frame(cx, cy, sz, "#17191F", .9))
            if rnd.random() < .45:
                k = sz * .22
                out.append(f'<rect x="{cx + sz/2 - k/2}" y="{cy + sz/2 - k/2}" width="{k}" height="{k}" fill="#FF5A1F"/>')
    else:
        out.append(f'<rect width="{w}" height="{h}" fill="#0E1124"/>')
        y = 40
        while y < h:
            x = 40
            while x < w - 60:
                ln = rnd.choice([60, 120, 180, 240, 360])
                cob = rnd.random() < .18 * dense
                out.append(f'<rect x="{x}" y="{y}" width="{ln}" height="{6 if cob else 1}" fill="{"#6892FB" if cob else "#F7F7F4"}" '
                           f'fill-opacity="{1 if cob else .22}"/>')
                if rnd.random() < .05 * dense:
                    out.append(f'<circle cx="{x + ln + 14}" cy="{y + 1}" r="4" fill="#5EF0C0"/>')
                x += ln + 28
            y += 34
    out.append("</svg>")
    return "".join(out)


def bracket_rect(w, h, k=10, a=90, ch=10, color="#17191F", op=1.0):
    """Two chamfered corner brackets around a w x h box, at true proportions (pixel units)."""
    tl = f"0,{ch} {ch},0 {a},0 {a},{k} {k},{k} {k},{a} 0,{a}"
    br = f"{w},{h-ch} {w-ch},{h} {w-a},{h} {w-a},{h-k} {w-k},{h-k} {w-k},{h-a} {w},{h-a}"
    return (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="position:absolute;left:0;top:0">'
            f'<g fill="{color}" fill-opacity="{op}"><polygon points="{tl}"/><polygon points="{br}"/></g></svg>')


def bracket_frame(x, y, s, color, op=1.0):
    k = s * 0.14   # bracket thickness
    a = s * 0.46   # arm length
    ch = s * 0.12  # chamfer
    tl = f"{x},{y+ch} {x+ch},{y} {x+a},{y} {x+a},{y+k} {x+k},{y+k} {x+k},{y+a} {x},{y+a}"
    X, Y = x + s, y + s
    br = f"{X},{Y-ch} {X-ch},{Y} {X-a},{Y} {X-a},{Y-k} {X-k},{Y-k} {X-k},{Y-a} {X},{Y-a}"
    return f'<g fill="{color}" fill-opacity="{op}"><polygon points="{tl}"/><polygon points="{br}"/></g>'


# ---------------------------------------------------------------------------- explorations & product marks

def bar_letter(letter, lit, ink, signal):
    """Bar-built initials on the Signal grid (stem 18, arms 18, gap 8)."""
    R = lambda x, y, w, h, f: f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{f}"/>'
    parts = {
        "E": [("stem", 12, 10, 18, 80), ("top", 38, 10, 50, 18), ("mid", 38, 41, 36, 18), ("bot", 38, 72, 50, 18)],
        "F": [("stem", 12, 10, 18, 80), ("top", 38, 10, 50, 18), ("mid", 38, 41, 36, 18)],
        "L": [("stem", 12, 10, 18, 80), ("bot", 38, 72, 50, 18)],
        "H": [("stem", 12, 10, 18, 80), ("mid", 38, 41, 24, 18), ("stem2", 70, 10, 18, 80)],
        "T": [("top", 12, 10, 76, 18), ("stem", 41, 36, 18, 54)],
    }[letter]
    return ('<svg viewBox="0 0 100 100" class="pm">' +
            "".join(R(x, y, w, h, signal if n == lit else ink) for n, x, y, w, h in parts) + "</svg>")


def explorations(c):
    """Four symbol/wordmark explorations: (svg_or_html, title, verdict, chosen)."""
    if c is A:
        cy, ink = c["brand"], c["fg"]
        R = lambda x, y, w, h, f: f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{f}"/>'
        e1 = bar_letter("E", "mid", ink, cy)
        e2 = ('<svg viewBox="0 0 100 100" class="pm"><path fill="' + ink +
              '" d="M12 10H88V28H30V72H88V90H12Z"/>' + R(38, 41, 36, 18, cy) + "</svg>")
        e3 = ('<svg viewBox="0 0 100 100" class="pm">' + R(12, 4, 18, 86, ink) + R(38, 26, 50, 16, ink) +
              R(38, 50, 36, 16, cy) + R(38, 74, 50, 16, ink) + "</svg>")
        e4 = ('<svg viewBox="0 0 100 100" class="pm">' + R(24, 8, 20, 84, ink) + R(24, 8, 20, 22, cy) +
              R(56, 26, 20, 66, ink) + "</svg>")
        return [(e1, "Segmented E", "Chosen: four separate bars, one lit. Clear E, ownable gap rhythm.", True),
                (e2, "Joined frame E", "Stronger mass, but reads as a stock E glyph. The gaps carry the idea.", False),
                (e3, "Rising stem", "Echoes the l's ascender; reads as l + ≡ before E.", False),
                (e4, "l·I pair", "Pure name geometry, but close to pause and signal-strength icons.", False)]
    if c is B:
        g, em = c["fg"], c["accent"]

        def frame(core=True, four=False, ecore=False):
            s = '<svg viewBox="0 0 100 100" class="pm">' + bracket_frame(8, 8, 84, g)
            if four:
                s += (f'<g transform="rotate(90 50 50)">{bracket_frame(8, 8, 84, g)}</g>')
            if core:
                s += f'<rect x="39" y="39" width="22" height="22" fill="{em}"/>'
            if ecore:
                s += (f'<g fill="{em}"><rect x="38" y="36" width="6" height="28"/><rect x="46" y="36" width="16" height="6"/>'
                      f'<rect x="46" y="47" width="12" height="6"/><rect x="46" y="58" width="16" height="6"/></g>')
            return s + "</svg>"
        return [(frame(), "Frame + core", "Chosen: two brackets, one core. Container logic, robust at 16 px.", True),
                (frame(core=False, four=True), "Four-corner viewfinder", "Reads as a QR/scan icon, a category cliché.", False),
                (frame(core=False), "Empty frame", "Elegant, but no point of energy; vanishes at 16 px.", False),
                (frame(core=False, ecore=True), "Frame + E core", "Too literal; the E clogs below 32 px.", False)]
    # C: typographic explorations rendered with the identity's display face
    f = c["display"]
    base = f"font-family:'{f}';font-size:64px;line-height:1;color:{c['brand']};position:relative;display:inline-block"
    e1 = paint(asset("C", "master-wordmark.svg"), {"*": c["brand"]}, "wm", "height:76px")
    e2 = (f'<span style="{base}">El<span style="position:relative">IT<span style="position:absolute;left:0;right:0;top:3px;'
          f'height:7px;background:{c["brand"]}"></span></span></span>')
    e3 = f'<span style="{base}">El<span style="color:#0E1124">IT</span></span>'
    e4 = f'<span style="{base}">ElIT</span>'
    return [(e1, "Overline above IT", "Chosen: reads El + IT, survives one colour, gives a system device.", True),
            (e2, "Joined IT beam", "Rendered in round 1: the beam turned the I into a T (\"ElTT\"). Rejected.", False),
            (e3, "Colour split El·IT", "Meaning depends on colour; fails in one-colour use.", False),
            (e4, "Plain serif", "Beautiful but not ownable; any studio could set it.", False)]


def product_marks(c):
    out = []
    if c is A:
        letters = [("E", "ElIT Solutions", "master"), ("F", "ElIT Flow", "automation"), ("L", "ElIT Ledger", "invoicing"),
                   ("H", "ElIT Hub", "integrations")]
        lit = {"E": "mid", "F": "mid", "L": "bot", "H": "mid"}
        for i, (L, name, role) in enumerate(letters):
            sig = c["brand"] if i == 0 else ["#3DDCF4", "#8B7BFF", "#5EF0C0"][i - 1]
            out.append((bar_letter(L, lit[L], "#F1F3F7", sig), name, role))
    elif c is B:
        cores = [("#FF5A1F", "ElIT Solutions", "master"), ("#14B8A6", "ElIT Flow", "automation"),
                 ("#8B7BFF", "ElIT Ledger", "invoicing"), ("#F5B83D", "ElIT Hub", "integrations")]
        for col, name, role in cores:
            out.append(('<svg viewBox="0 0 100 100" class="pm">' + bracket_frame(8, 8, 84, "#17191F") +
                        f'<rect x="39" y="39" width="22" height="22" fill="{col}"/></svg>', name, role))
    else:
        f = c["display"]
        for name, role in [("ElIT", "master"), ("Flow", "automation"), ("Ledger", "invoicing"), ("Hub", "integrations")]:
            html = (f'<div style="display:inline-block;text-align:left"><div style="height:6px;background:#1838C9;margin-bottom:8px"></div>'
                    f'<div style="font-family:\'{f}\';font-size:44px;line-height:1;color:#0E1124">{name}</div>'
                    f'<div style="font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#505561;margin-top:8px">'
                    f'{"Solutions" if name == "ElIT" else "by ElIT"}</div></div>')
            out.append((html, name if name != "ElIT" else "ElIT Solutions", role))
    return out


# ============================================================================ application mocks

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:{{W}}px;height:{{H}}px;overflow:hidden}
body{background:var(--bg);color:var(--fg);font-family:var(--text);-webkit-font-smoothing:antialiased}
.lk,.st{height:var(--lkh,30px);width:auto;display:block}
.sym{width:var(--symw,40px);height:auto;display:block}
.wm{height:var(--wmh,30px);width:auto;display:block}
.mono{font-family:{{MONO}};font-variant-numeric:tabular-nums}
.tnum{font-variant-numeric:tabular-nums}
"""


def vars_css(c, extra=""):
    return (f":root{{--bg:{c['bg']};--bg2:{c['bg2']};--surface:{c['surface']};--line:{c['line']};--fg:{c['fg']};"
            f"--muted:{c['muted']};--brand:{c['brand']};--accent:{c['accent']};--on-brand:{c['on_brand']};"
            f"--display:'{c['display']}',system-ui,sans-serif;--text:'{c['text']}',system-ui,sans-serif;{extra}}}")


def page(c, body, css, W, H, title):
    return (f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>{title}</title>{MONO_LINK}"
            f"<style>{fonts(c['id'])}</style><style>{vars_css(c)}{T(BASE_CSS, W=W, H=H, MONO=c['mono'])}{css}</style>"
            f"</head><body>{body}</body></html>")


SERVICES = [("Websites", "Fast, accessible sites and web platforms."),
            ("Custom software", "Web apps and internal tools built around your process."),
            ("Automation", "Workflows that remove manual, repetitive work."),
            ("Integrations", "Systems that talk to each other, reliably.")]


def website(c):
    m = marks(c, "dark" if c is A else "light")
    if c is A:
        pat = pattern_svg(c, 1440, 900, seed=3, dense=.8)
        body = f"""
<div class="bgpat">{pat}</div><div class="fade"></div>
<header><div style="--lkh:30px">{m['lockup']}</div><nav><a>Services</a><a>Products</a><a>Work</a><a>Company</a></nav>
<div class="cta-s">Start a project</div></header>
<main><div class="eyebrow mono"><i></i>SOFTWARE ENGINEERING · CYPRUS</div>
<h1>Digital solutions,<br><span>engineered.</span></h1>
<p class="lead">Websites, custom software, automation and integrations, designed and built in Cyprus for teams across Europe.</p>
<div class="btns"><div class="b1">Start a project →</div><div class="b2">See our work</div></div></main>
<aside class="term"><div class="bar"><b></b><b></b><b></b><span class="mono">deploy · client-portal</span></div>
<pre class="mono"><span class="d">$</span> elit deploy --env production
<span class="ok">✓</span> build      <span class="d">12.4s</span>
<span class="ok">✓</span> tests      <span class="d">148 passed</span>
<span class="ok">✓</span> migrate    <span class="d">3 changes</span>
<span class="sig">▍</span> live       <span class="c">portal.client.example</span></pre>
<div class="meter">{''.join(f'<i style="width:{w}%;{"background:var(--brand)" if k==3 else ""}"></i>' for k,w in enumerate([92,64,78,40,85]))}</div></aside>
<section class="svc">{''.join(f'<div class="s"><div class="n mono">0{i+1}</div><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(SERVICES))}</section>
<div class="lbl">Concept mock · sample copy</div>"""
        css = """
.bgpat{position:absolute;inset:0;opacity:.9}.bgpat svg{width:100%;height:100%}
.fade{position:absolute;inset:0;background:linear-gradient(90deg,#0B1531 0%,rgba(11,21,49,.92) 45%,rgba(11,21,49,.35) 100%)}
header{position:relative;display:flex;align-items:center;gap:48px;padding:30px 72px}
nav{display:flex;gap:30px;font-size:15px;color:#C9D0E2;margin-left:24px}.cta-s{margin-left:auto;border:1px solid #3DDCF4;color:#3DDCF4;padding:10px 18px;font-size:14px;border-radius:2px}
main{position:relative;padding:92px 72px 0;width:780px}
.eyebrow{font-size:12px;letter-spacing:.18em;color:#9BA6C2;display:flex;align-items:center;gap:12px}.eyebrow i{width:28px;height:4px;background:#3DDCF4}
h1{font-family:var(--display);font-size:84px;line-height:.98;letter-spacing:-.03em;margin-top:26px}h1 span{color:#3DDCF4}
.lead{font-size:20px;line-height:1.55;color:#C9D0E2;margin-top:28px;max-width:600px}
.btns{display:flex;gap:14px;margin-top:40px}.b1{background:#3DDCF4;color:#06101F;padding:16px 26px;font-weight:600;border-radius:2px}.b2{border:1px solid #33416B;padding:16px 26px;border-radius:2px;color:#F1F3F7}
.term{position:absolute;right:72px;top:190px;width:470px;background:rgba(7,13,32,.88);border:1px solid #22305A;border-radius:6px;box-shadow:0 30px 80px -20px rgba(139,123,255,.35)}
.term .bar{display:flex;gap:7px;align-items:center;padding:12px 14px;border-bottom:1px solid #22305A}.term .bar b{width:9px;height:9px;border-radius:50%;background:#33416B}.term .bar span{margin-left:10px;font-size:12px;color:#9BA6C2}
.term pre{padding:20px 22px;font-size:14px;line-height:1.9;color:#F1F3F7}.d{color:#6B7386}.ok{color:#3FC6A0}.sig{color:#3DDCF4}.c{color:#3DDCF4}
.meter{padding:0 22px 22px;display:grid;gap:6px}.meter i{display:block;height:6px;background:#22305A}
.svc{position:absolute;left:72px;right:72px;bottom:56px;display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#22305A;border:1px solid #22305A}
.s{background:#0B1531;padding:22px 22px}.s .n{font-size:12px;color:#3DDCF4}.s h3{font-family:var(--display);font-size:20px;margin:10px 0 6px}.s p{font-size:14px;color:#9BA6C2;line-height:1.45}
.lbl{position:absolute;right:16px;bottom:10px;font-size:11px;color:#4D556A}"""
    elif c is B:
        body = f"""
<header><div style="--lkh:30px">{m['lockup']}</div><nav><a>Services</a><a>Products</a><a>Work</a><a>Company</a></nav><div class="cta-s">Start a project</div></header>
<main><div class="eyebrow">SOFTWARE ENGINEERING — CYPRUS</div>
<h1>Digital solutions,<br>engineered.</h1>
<p class="lead">Websites, custom software, automation and integrations, designed and built in Cyprus for teams across Europe.</p>
<div class="btns"><div class="b1">Start a project</div><div class="b2">See our work →</div></div></main>
<div class="shot"><div class="br">{bracket_rect(612, 472, 10, 96, 10)}</div>
<div class="win"><div class="wb"><span></span><span></span><span></span></div>
<div class="wg"><div class="side">{''.join(f'<i style="width:{w}%"></i>' for w in [70,55,80,45,62])}</div>
<div class="cont"><div class="k">{''.join(f'<div><small>{a}</small><b class="tnum">{b}</b></div>' for a,b in [("Runs today","1,284"),("Success","99.2%"),("Saved","38 h")])}</div>
<div class="chart">{''.join(f'<i style="height:{h}%;{"background:#FF5A1F" if k==9 else ""}"></i>' for k,h in enumerate([40,55,48,62,58,70,66,74,69,88,72,64]))}</div></div></div></div>
<div class="core"></div></div>
<section class="svc">{''.join(f'<div class="s"><svg viewBox="0 0 100 100">{bracket_frame(4,4,92,"#17191F")}</svg><h3>{t}</h3><p>{d}</p></div>' for t,d in SERVICES)}</section>
<div class="lbl">Concept mock · sample data</div>"""
        css = """
header{display:flex;align-items:center;gap:48px;padding:30px 72px;border-bottom:1px solid #D1D0CA}
nav{display:flex;gap:30px;font-size:15px;color:#3B3D44;margin-left:24px}.cta-s{margin-left:auto;background:#17191F;color:#fff;padding:11px 18px;font-size:14px;clip-path:polygon(8px 0,100% 0,100% calc(100% - 8px),calc(100% - 8px) 100%,0 100%,0 8px)}
main{padding:80px 72px 0;width:720px}
.eyebrow{font-family:var(--display);font-size:13px;letter-spacing:.16em;color:#B13706}
h1{font-family:var(--display);font-size:76px;line-height:1.02;letter-spacing:.005em;margin-top:22px;font-weight:600}
.lead{font-size:20px;line-height:1.55;color:#4A4C52;margin-top:26px;max-width:580px}
.btns{display:flex;gap:14px;margin-top:38px;align-items:center}.b1{background:#FF5A1F;color:#120A06;padding:16px 26px;font-weight:600;clip-path:polygon(10px 0,100% 0,100% calc(100% - 10px),calc(100% - 10px) 100%,0 100%,0 10px)}.b2{padding:16px 6px;font-weight:600}
.shot{position:absolute;right:72px;top:150px;width:560px;height:420px}.shot .br{position:absolute;left:-26px;top:-26px;width:612px;height:472px}
.win{position:absolute;inset:0;background:#fff;box-shadow:0 30px 60px -30px rgba(23,25,31,.35)}.wb{display:flex;gap:6px;padding:12px;border-bottom:1px solid #E7E7E4}.wb span{width:9px;height:9px;background:#D1D0CA}
.wg{display:grid;grid-template-columns:120px 1fr;height:calc(100% - 34px)}.side{background:#17191F;padding:18px 14px;display:grid;gap:12px;align-content:start}.side i{display:block;height:7px;background:#44474F}
.cont{padding:20px}.k{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.k div{border:1px solid #E7E7E4;padding:12px}.k small{display:block;font-size:11px;color:#70737C}.k b{font-family:var(--display);font-size:24px;font-weight:600}
.chart{display:flex;align-items:flex-end;gap:8px;height:200px;margin-top:22px;border-bottom:1px solid #D1D0CA}.chart i{flex:1;background:#2B2D33}
.core{position:absolute;right:-60px;bottom:-60px;width:22px;height:22px;background:#FF5A1F}
.svc{position:absolute;left:72px;right:72px;bottom:52px;display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.s{padding:6px 0}.s svg{width:28px;height:28px}.s h3{font-family:var(--display);font-size:19px;font-weight:600;margin:12px 0 6px}.s p{font-size:14px;color:#55575D;line-height:1.45}
.lbl{position:absolute;right:16px;bottom:10px;font-size:11px;color:#8E9199}"""
    else:
        body = f"""
<header><div style="--wmh:34px">{m['lockup']}</div><nav><a>Services</a><a>Products</a><a>Work</a><a>Company</a></nav><div class="cta-s">Start a project</div></header>
<main><div class="ol"></div><div class="eyebrow">Software engineering studio · Cyprus</div>
<h1>Digital solutions,<br><em>engineered</em> to last.</h1>
<p class="lead">Websites, custom software, automation and integrations, designed and built in Cyprus for teams across Europe.</p>
<div class="btns"><div class="b1">Start a project</div><div class="b2">Read our approach</div></div></main>
<aside><div class="case"><div class="ol2"></div><small>Selected work · 2026</small><h3>A client portal that replaced four spreadsheets.</h3>
<div class="row tnum"><div><b>−62%</b><span>manual entry</span></div><div><b>3 wks</b><span>to launch</span></div></div><div class="pat">{pattern_svg(c, 520, 170, seed=5, dense=1.2)}</div></div></aside>
<section class="svc">{''.join(f'<div class="s"><div class="ol3"></div><div class="n">0{i+1}</div><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(SERVICES))}</section>
<div class="lbl">Concept mock · sample copy and figures</div>"""
        css = """
header{display:flex;align-items:center;gap:48px;padding:30px 72px;border-bottom:1px solid #D6D6D0}
nav{display:flex;gap:30px;font-size:15px;color:#3B414D;margin-left:24px}.cta-s{margin-left:auto;background:#1838C9;color:#fff;padding:11px 20px;font-size:14px}
main{padding:70px 72px 0;width:760px}.ol{width:120px;height:7px;background:#1838C9}
.eyebrow{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#505561;margin-top:18px}
h1{font-family:var(--display);font-size:64px;line-height:1.04;letter-spacing:-.012em;margin-top:20px;font-weight:700}h1 em{font-style:normal;color:#1838C9}
.lead{font-size:20px;line-height:1.6;color:#3B414D;margin-top:26px;max-width:600px}
.btns{display:flex;gap:22px;margin-top:38px;align-items:center}.b1{background:#0E1124;color:#fff;padding:16px 26px}.b2{border-bottom:2px solid #1838C9;padding:4px 0;color:#0E1124}
aside{position:absolute;right:72px;top:160px;width:520px}.case{background:#fff;border:1px solid #D6D6D0;padding:30px 0 0}.case>*:not(.pat){margin-left:30px;margin-right:30px}
.ol2{width:60px;height:5px;background:#1838C9}.case small{display:block;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#6E737E;margin-top:14px}
.case h3{font-family:var(--display);font-size:30px;line-height:1.15;margin-top:10px;font-weight:700}.row{display:flex;gap:40px;margin:24px 30px}.row b{font-family:var(--display);font-size:34px;color:#1838C9;display:block}.row span{font-size:13px;color:#505561}
.pat svg{display:block;width:100%;height:auto}
.svc{position:absolute;left:72px;right:72px;bottom:52px;display:grid;grid-template-columns:repeat(4,1fr);gap:28px}
.ol3{height:4px;width:40px;background:#1838C9}.s .n{font-family:var(--display);font-size:15px;color:#1838C9;margin-top:12px}.s h3{font-family:var(--display);font-size:24px;margin:6px 0 6px;font-weight:700}.s p{font-size:14px;color:#505561;line-height:1.5}
.lbl{position:absolute;right:16px;bottom:10px;font-size:11px;color:#9EA1AA}"""
    return page(c, f'<div style="position:relative;width:1440px;height:900px;overflow:hidden">{body}</div>', css, 1440, 900,
                f"ElIT {c['name']} website")


def app(c):
    dark = c is A
    m = marks(c, "dark" if dark else "light")
    sym = m["symbol"]
    if c is A:
        th = dict(bg="#070D20", side="#0B1531", card="#0F1A3A", line="#1D2A52", fg="#F1F3F7", mut="#8F9AB8", act="#3DDCF4",
                  act2="#8B7BFF", onact="#06101F", ok="#3FC6A0", bad="#FE8477", bar="#22305A", radius="6px")
    elif c is B:
        th = dict(bg="#F1F1EE", side="#17191F", card="#FFFFFF", line="#E0DFDA", fg="#17191F", mut="#70737C", act="#FF5A1F",
                  act2="#17191F", onact="#120A06", ok="#0D9373", bad="#B4312F", bar="#2B2D33", radius="0px")
    else:
        th = dict(bg="#F7F7F4", side="#FFFFFF", card="#FFFFFF", line="#E2E2DC", fg="#0E1124", mut="#6E737E", act="#1838C9",
                  act2="#0E1124", onact="#FFFFFF", ok="#08795E", bad="#B4312B", bar="#1838C9", radius="0px")
    side_fg = "#F1F1EE" if c is B else th["fg"]
    side_mark = (marks(c, "dark")["symbol"] if c is B else sym)
    rows = [("Invoice sync → ERP", "Every 15 min", "ok", "1,204", "0.4s"), ("New lead → CRM + Slack", "On event", "ok", "312", "1.1s"),
            ("Monthly VAT export", "Monthly", "ok", "1", "8.2s"), ("Stock levels → webshop", "Hourly", "bad", "18", "—"),
            ("Contract PDF → e-sign", "On event", "ok", "57", "2.3s")]
    bars = [38, 52, 47, 61, 58, 72, 66, 79, 71, 88, 81, 92, 76, 84]
    title = {"A": "ElIT Flow", "B": "ElIT Flow", "C": "Flow"}[c["id"]]
    prod_mark = (bar_letter("F", "mid", th["fg"], "#3DDCF4") if c is A else
                 ('<svg viewBox="0 0 100 100" class="pm">' + bracket_frame(8, 8, 84, "#F1F1EE") +
                  '<rect x="39" y="39" width="22" height="22" fill="#14B8A6"/></svg>') if c is B else
                 '<div class="cprod"><i></i>Flow</div>')
    body = f"""
<div class="app"><aside class="side"><div class="pmark">{prod_mark}<span>{title if c is not C else ''}</span></div>
<div class="grp">Automation</div>{''.join(f'<div class="nav {"on" if i==0 else ""}"><i></i>{n}</div>' for i,n in enumerate(["Workflows","Runs","Connections","Schedules"]))}
<div class="grp">Workspace</div>{''.join(f'<div class="nav"><i></i>{n}</div>' for n in ["Team","Billing","Settings"])}
<div class="by"><div class="bysym">{side_mark}</div><span>by ElIT Solutions</span></div></aside>
<section class="main"><div class="top"><div><small>Workspace · Client Portal</small><h1>Workflows</h1></div><div class="search">Search workflows…</div><div class="btn">New workflow</div></div>
<div class="kpis">{''.join(f'<div class="kpi"><small>{a}</small><b class="tnum">{b}</b><em class="tnum">{d}</em></div>' for a,b,d in [("Runs this week","8,412","+12.4%"),("Success rate","99.2%","+0.3 pt"),("Time saved","38 h","this week"),("Active workflows","24","3 paused")])}</div>
<div class="grid"><div class="card chart"><div class="ch"><b>Runs per day</b><span>Last 14 days</span></div>
<div class="bars">{''.join(f'<i style="height:{h}%"></i>' for h in bars)}</div></div>
<div class="card live"><div class="ch"><b>Live</b><span class="dot">●</span></div>{''.join(f'<div class="ev mono"><span>{t}</span>{e}</div>' for t,e in [("14:02:11","invoice-sync ✓ 48 records"),("14:01:57","lead-router ✓ to CRM"),("14:01:20","stock-levels ✕ timeout"),("14:00:03","invoice-sync ✓ 51 records")])}</div></div>
<div class="card tbl"><div class="tr th"><span>Workflow</span><span>Trigger</span><span>Status</span><span>Runs</span><span>Avg</span></div>
{''.join(f'<div class="tr"><span>{a}</span><span class="mut">{b}</span><span><i class="st {s}"></i>{"Healthy" if s=="ok" else "Failing"}</span><span class="tnum">{r}</span><span class="tnum mut">{d}</span></div>' for a,b,s,r,d in rows)}</div>
<div class="lbl">Concept mock · hypothetical product, sample data</div></section></div>"""
    css = T("""
.app{display:grid;grid-template-columns:248px 1fr;width:1440px;height:900px;background:{{bg}};color:{{fg}}}
.side{background:{{side}};color:{{sfg}};padding:22px 16px;display:flex;flex-direction:column;border-right:1px solid {{line}}}
.pmark{display:flex;align-items:center;gap:10px;font-family:var(--display);font-size:19px;margin:2px 6px 24px}.pmark .pm{width:30px;height:30px}
.cprod{font-family:var(--display);font-size:26px;font-weight:700}.cprod i{display:block;height:5px;width:100%;background:#1838C9;margin-bottom:6px}
.grp{font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.55;margin:16px 8px 8px}
.nav{display:flex;align-items:center;gap:10px;padding:9px 10px;font-size:14px;border-radius:{{radius}};opacity:.85}.nav i{width:14px;height:14px;border:1.5px solid currentColor;opacity:.6}
.nav.on{background:{{navon}};opacity:1;color:{{navonfg}}}.nav.on i{background:{{act}};border-color:{{act}};opacity:1}
.by{margin-top:auto;display:flex;align-items:center;gap:10px;font-size:12px;opacity:.75;padding:8px}.bysym .sym,.bysym .wm{width:20px;height:20px}
.main{padding:28px 36px;position:relative}.top{display:flex;align-items:flex-end;gap:16px}.top small{font-size:12px;color:{{mut}}}.top h1{font-family:var(--display);font-size:34px;margin-top:4px;font-weight:700}
.search{margin-left:auto;width:300px;border:1px solid {{line}};background:{{card}};padding:11px 14px;font-size:14px;color:{{mut}};border-radius:{{radius}}}
.btn{background:{{act}};color:{{onact}};padding:12px 18px;font-weight:600;font-size:14px;border-radius:{{radius}}}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:26px}.kpi{background:{{card}};border:1px solid {{line}};padding:18px;border-radius:{{radius}}}
.kpi small{font-size:12px;color:{{mut}};display:block}.kpi b{font-family:var(--display);font-size:32px;display:block;margin-top:8px;font-weight:700}.kpi em{font-style:normal;font-size:12px;color:{{ok}}}
.grid{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-top:16px}.card{background:{{card}};border:1px solid {{line}};border-radius:{{radius}};padding:18px}
.ch{display:flex;justify-content:space-between;align-items:center;font-size:14px}.ch span{font-size:12px;color:{{mut}}}.dot{color:{{ok}}!important}
.bars{display:flex;align-items:flex-end;gap:10px;height:170px;margin-top:16px;border-bottom:1px solid {{line}}}.bars i{flex:1;background:{{bar}};opacity:.9}.bars i:nth-child(12){background:{{act}};opacity:1}
.ev{font-size:12px;padding:9px 0;border-bottom:1px solid {{line}};display:flex;gap:10px}.ev span{color:{{mut}}}
.tbl{margin-top:16px;padding:6px 18px}.tr{display:grid;grid-template-columns:2.2fr 1.2fr 1fr .7fr .6fr;padding:11px 0;font-size:14px;border-bottom:1px solid {{line}};align-items:center}.tr:last-child{border:0}
.th{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:{{mut}}}.mut{color:{{mut}}}.st{display:inline-block;width:8px;height:8px;margin-right:8px;border-radius:50%}.st.ok{background:{{ok}}}.st.bad{background:{{bad}}}
.lbl{position:absolute;right:16px;bottom:8px;font-size:11px;color:{{mut}};opacity:.7}
""", sfg=side_fg, navon=("#16234A" if c is A else "#2B2D33" if c is B else "#EEF2FF"),
          navonfg=("#F1F3F7" if c is not C else "#1838C9"), **th)
    return page(c, body, css, 1440, 900, f"ElIT {c['name']} app")


def cards(c):
    md, ml = marks(c, "dark"), marks(c, "light")
    person = ("Alex Constantinou", "Founder & Technical Director")
    contact = ["+357 99 000 000", "alex@elitsolutions.cy", "elitsolutions.cy", "Limassol, Cyprus"]
    if c is A:
        front = f'<div class="card f"><div class="pat">{pattern_svg(c, 595, 385, seed=11, dense=.7)}</div><div class="fadeL"></div><div class="ctr" style="--lkh:58px">{md["lockup"]}</div><div class="tg mono">DIGITAL SOLUTIONS, ENGINEERED.</div></div>'
        back = (f'<div class="card b"><div style="--symw:40px">{md["symbol"]}</div><div class="who"><b>{person[0]}</b><span>{person[1]}</span></div>'
                f'<div class="ct mono">{"".join(f"<div>{x}</div>" for x in contact)}</div><i class="sig"></i></div>')
        css = """.f{background:#0B1531}.f .pat{position:absolute;inset:0}.fadeL{position:absolute;inset:0;background:linear-gradient(90deg,#0B1531 0%,rgba(11,21,49,.97) 58%,rgba(11,21,49,.25) 100%)}.f .pat svg{width:100%;height:100%}.ctr{position:absolute;left:52px;top:150px}
.tg{position:absolute;left:52px;bottom:40px;font-size:11px;letter-spacing:.2em;color:#9BA6C2}
.b{background:#0F1A3A;color:#F1F3F7;padding:44px 52px}.who{margin-top:56px}.who b{font-family:var(--display);font-size:26px;display:block}.who span{font-size:14px;color:#9BA6C2}
.ct{position:absolute;right:52px;bottom:40px;text-align:right;font-size:12px;line-height:1.75;color:#C9D0E2}.sig{position:absolute;left:52px;bottom:44px;width:60px;height:8px;background:#3DDCF4}"""
    elif c is B:
        front = (f'<div class="card f"><div class="fr">{bracket_rect(543, 333, 8, 70, 8, "#F1F1EE", .22)}</div>'
                 f'<div class="ctr" style="--lkh:62px">{md["lockup"]}</div></div>')
        back = (f'<div class="card b"><div class="who"><b>{person[0]}</b><span>{person[1]}</span></div><div class="ct">{"".join(f"<div>{x}</div>" for x in contact)}</div>'
                f'<div class="sm" style="--symw:44px">{ml["symbol"]}</div></div>')
        css = """.f{background:#17191F}.fr{position:absolute;left:26px;top:26px;width:543px;height:333px}.ctr{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)}
.b{background:#F1F1EE;color:#17191F;padding:48px 52px}.who b{font-family:var(--display);font-size:26px;display:block;font-weight:600}.who span{font-size:14px;color:#5B5D63}
.ct{position:absolute;left:52px;bottom:44px;font-size:13px;line-height:1.75}.sm{position:absolute;right:48px;bottom:44px}"""
    else:
        front = f'<div class="card f"><div class="ctr" style="--wmh:76px">{ml["wordmark"]}</div><div class="tg">Software engineering studio</div></div>'
        back = (f'<div class="card b"><div class="ol"></div><div class="who"><b>{person[0]}</b><span>{person[1]}</span></div>'
                f'<div class="ct">{"".join(f"<div>{x}</div>" for x in contact)}</div><div class="pat">{pattern_svg(c, 595, 120, seed=2, dense=1.4)}</div></div>')
        css = """.f{background:#F7F7F4}.ctr{position:absolute;left:56px;top:120px}.tg{position:absolute;left:56px;bottom:44px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#505561}
.b{background:#0E1124;color:#F7F7F4;padding:46px 56px}.ol{width:56px;height:6px;background:#6892FB}.who{margin-top:18px}.who b{font-family:var(--display);font-size:28px;display:block}.who span{font-size:14px;color:#9EA1AA}
.ct{margin-top:22px;font-size:13px;line-height:1.7;color:#D2D4D9}.pat{position:absolute;left:0;right:0;bottom:0;height:84px;overflow:hidden}.pat svg{width:100%;display:block}"""
    body = f"""<div class="desk"><div class="lbl1">Front</div><div class="lbl2">Back</div>{front}{back}<div class="foot">Business card · 85 × 55 mm · placeholder name and contact details</div></div>"""
    css += """.desk{width:1440px;height:820px;background:#DCDDE0;position:relative}
.card{position:absolute;width:595px;height:385px;overflow:hidden;box-shadow:0 2px 2px rgba(0,0,0,.08),0 30px 60px -20px rgba(0,0,0,.35)}
.card:nth-of-type(1){left:90px;top:200px}.card:nth-of-type(2){left:755px;top:200px}
.desk>.card:first-of-type{left:90px}.desk .f{left:90px;top:200px}.desk .b{left:755px;top:200px}
.lbl1,.lbl2{position:absolute;top:160px;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#6E737E}.lbl1{left:90px}.lbl2{left:755px}
.foot{position:absolute;left:90px;bottom:120px;font-size:13px;color:#6E737E}"""
    return page(c, body, css, 1440, 820, f"ElIT {c['name']} cards")


# ============================================================================ concept board

BOARD_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1600px;background:#EDEEF0;color:#14161C;font-family:'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.lk,.st{height:var(--lkh,30px);width:auto;display:block}.sym{width:var(--symw,40px);height:auto;display:block}.wm{height:var(--wmh,30px);width:auto;display:block}
.pm{width:100%;height:100%;display:block}
.hero{background:var(--bg);color:var(--fg);padding:56px 72px 64px;position:relative;overflow:hidden}
.hero .pat{position:absolute;inset:0;opacity:.75}.hero .pat svg{width:100%;height:100%}
.hero .shade{position:absolute;inset:0;background:var(--shade)}
.hero>*:not(.pat):not(.shade){position:relative}
.meta{display:flex;justify-content:space-between;font-size:13px;letter-spacing:.14em;text-transform:uppercase;opacity:.7}
.hero .title{display:flex;align-items:flex-end;justify-content:space-between;margin-top:40px}
.hero h1{font-family:var(--display);font-size:120px;line-height:.9;letter-spacing:-.02em}
.hero .ol{font-size:24px;margin-top:18px;opacity:.85}
.hero .big{margin-top:70px;display:flex;justify-content:center;padding:40px 0}
.chips{display:flex;gap:10px;margin-top:28px}.chips span{border:1px solid currentColor;padding:7px 14px;font-size:13px;letter-spacing:.06em;opacity:.8}
.rec{background:var(--brand);color:var(--on-brand);padding:8px 14px;font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:600}
section{padding:56px 72px;background:#F7F7F8;border-top:1px solid #DADBDF}
section:nth-of-type(even){background:#FFFFFF}
h2{font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:#6B6F7A;margin-bottom:26px;display:flex;gap:14px;align-items:center}
h2 b{color:#14161C;font-weight:700}
.two{display:grid;grid-template-columns:1.1fr 1fr;gap:56px}
.lede{font-size:22px;line-height:1.55}
.p{font-size:16px;line-height:1.65;color:#3E424C}
.k{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#6B6F7A;margin:22px 0 8px}
.axes .ax{display:grid;grid-template-columns:110px 1fr 110px;gap:12px;align-items:center;font-size:13px;color:#4A4E58;margin:10px 0}
.axes .ax:first-child{margin-top:0}
.track{position:relative;height:2px;background:#C9CBD1}.track i{position:absolute;top:-6px;width:14px;height:14px;border-radius:50%;background:#14161C;margin-left:-7px}
.tiles{display:grid;grid-template-columns:repeat(6,1fr);gap:16px}
.tile{border:1px solid #DADBDF;background:#fff;min-height:220px;display:flex;align-items:center;justify-content:center;position:relative;padding:30px}
.tile .cap{position:absolute;left:14px;bottom:10px;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#8A8E98}
.tile.dark .cap{color:rgba(255,255,255,.55)}
.span2{grid-column:span 2}.span3{grid-column:span 3}.span4{grid-column:span 4}.span6{grid-column:span 6}
.sizes{display:flex;align-items:flex-end;gap:26px}.sizes figure{display:flex;flex-direction:column;align-items:center;gap:8px;font-size:11px;color:#8A8E98}
.sizes img{image-rendering:pixelated}
.expl{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.ex{border:1px solid #DADBDF;background:#fff}.ex .vis{height:200px;display:flex;align-items:center;justify-content:center;padding:36px}
.ex .vis .pm{width:120px;height:120px}.ex.ch{outline:3px solid var(--mark);outline-offset:-3px}
.ex .t{padding:14px 18px 18px;border-top:1px solid #EEEFF1}.ex .t b{display:block;font-size:15px}.ex .t p{font-size:13px;color:#5A5E68;margin-top:6px;line-height:1.45}
.ex .tag{font-size:10px;letter-spacing:.14em;text-transform:uppercase;padding:3px 7px;margin-left:8px;vertical-align:2px}
.sw{display:grid;grid-template-columns:repeat(6,1fr);gap:0;border:1px solid #DADBDF}
.sw div{height:210px;padding:16px;display:flex;flex-direction:column;justify-content:flex-end;font-size:13px}
.sw b{font-size:16px}.sw code{font-family:'JetBrains Mono',monospace;font-size:14px;margin:4px 0}.sw small{opacity:.75}
.scale{display:grid;grid-template-columns:repeat(11,1fr);margin-top:14px}.scale div{height:44px;font-size:10px;padding:4px;display:flex;align-items:flex-end}
.prop{display:flex;height:22px;margin-top:14px}.prop i{display:block;height:100%}
.spec{display:grid;grid-template-columns:1.3fr 1fr;gap:48px;align-items:start}
.aa{font-family:var(--display);font-size:220px;line-height:.85}
.specline{border-top:1px solid #DADBDF;padding:14px 0;display:grid;grid-template-columns:150px 1fr;gap:20px;align-items:baseline}
.specline small{font-size:12px;color:#6B6F7A;letter-spacing:.08em;text-transform:uppercase}
.pats{display:grid;grid-template-columns:2fr 1fr;gap:16px}.pats .pt{height:330px;overflow:hidden;border:1px solid #DADBDF}.pats svg{width:100%;height:100%;display:block}
.prods{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:16px}
.prod{border:1px solid #DADBDF;padding:26px;display:flex;gap:18px;align-items:center;background:var(--prodbg);color:var(--prodfg)}
.prod .pmw{width:64px;height:64px;flex:none;display:flex;align-items:center}.prod b{font-size:17px;display:block}.prod span{font-size:13px;opacity:.7}
.prod.c{flex-direction:column;align-items:flex-start}
.shot{border:1px solid #DADBDF;background:#fff}.shot img{display:block;width:100%}.shot .cap{padding:12px 16px;font-size:13px;color:#5A5E68;border-top:1px solid #EEEFF1}
.apps{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}
.assess{display:grid;grid-template-columns:repeat(3,1fr);gap:32px}
.assess ul{list-style:none}.assess li{font-size:15px;line-height:1.55;padding:12px 0;border-top:1px solid #DADBDF;color:#30333B}
.assess h3{font-size:15px;margin-bottom:10px}
.foot{padding:26px 72px;font-size:12px;color:#8A8E98;display:flex;justify-content:space-between;background:#EDEEF0}
"""


def axes_html(sid):
    ident = json.load(open(os.path.join(WORK, "sets", sid, "identity.json")))
    poles = {"warm_cool": ("Warm", "Cool"), "classic_contemporary": ("Classic", "Contemporary"),
             "quiet_loud": ("Quiet", "Loud")}
    out = []
    for k, (a, b) in poles.items():
        v = (ident.get("axes") or {}).get(k, 0)
        out.append(f'<div class="ax"><span>{a}</span><div class="track"><i style="left:{(v + 2) * 25}%"></i></div>'
                   f'<span style="text-align:right">{b}</span></div>')
    return '<div class="axes">' + "".join(out) + "</div>"


def checks_line(sid):
    ident = json.load(open(os.path.join(WORK, "sets", sid, "identity.json")))
    a = ident.get("audit") or {}
    return a


def board(c, rel):
    sid = c["id"]
    md, ml = marks(c, "dark"), marks(c, "light")
    pal = palette(sid)
    # hero
    hero_dark = c is A
    hm = md if hero_dark else ml
    shade = ("linear-gradient(180deg,rgba(11,21,49,.55),rgba(11,21,49,.92))" if c is A else
             "linear-gradient(180deg,rgba(241,241,238,.6),rgba(241,241,238,.92))" if c is B else
             "linear-gradient(180deg,rgba(247,247,244,1),rgba(247,247,244,1))")
    pat_hero = pattern_svg(c, 1600, 900, seed=21, dense=1.0) if c is not C else ""
    big = (f'<div style="--lkh:170px">{hm["lockup"]}</div>' if sid != "C" else f'<div style="--wmh:230px">{hm["wordmark"]}</div>')
    rec = '<span class="rec">Recommended</span>' if c["recommended"] else ""
    hero = f"""<div class="hero" style="--shade:{shade}"><div class="pat">{pat_hero}</div><div class="shade"></div>
<div class="meta"><span>ElIT Solutions · Brand identity · Phase 1 exploration</span><span>Concept {sid} of 3 · v0.1 · 16 Nov 2026</span></div>
<div class="title"><div><h1>{c['name']}</h1><div class="ol">{c['one_liner']}</div><div class="chips">{''.join(f'<span>{p}</span>' for p in c['personality'])}</div></div>{rec}</div>
<div class="big">{big}</div></div>"""
    # strategy
    strat = f"""<section><h2><b>01</b> Concept, strategy and personality</h2><div class="two"><div><p class="lede">{c['idea']}</p>
<div class="k">Why it fits ElIT</div><p class="p">{c['fit']}</p></div><div><div class="k" style="margin-top:0">Position on the brief's axes</div>{axes_html(sid)}
<div class="k">Typography rationale</div><p class="p">{c['type_note']}</p></div></div></section>"""
    # logo system
    ink_l = c["light_fg"] if c is not C else c["brand"]
    mono_l, mono_sym_l = mono_marks(c, "#111111")
    mono_d, mono_sym_d = mono_marks(c, "#FFFFFF")
    b = os.path.join(WORK, "sets", sid, "logo", "build")
    sizes = "".join(f'<figure><img src="{os.path.relpath(os.path.join(b, f"favicon-{s}.png"), rel)}" width="{s*2}" height="{s*2}"><span>{s} px ×2</span></figure>'
                    for s in (16, 32, 48))
    app_icon = os.path.relpath(os.path.join(b, "app-icon-512.png"), rel)
    dbg = c["bg"] if c is A else "#17191F" if c is B else "#0E1124"
    lbg = "#FFFFFF" if c is A else c["bg"]
    if sid != "C":
        logo_tiles = f"""
<div class="tile span4" style="background:{dbg};min-height:300px"><div style="--lkh:96px">{md['lockup']}</div><span class="cap">Primary lockup · on {"midnight" if c is A else "graphite"}</span></div>
<div class="tile span2" style="background:{lbg}"><div style="--lkh:120px">{ml['stacked']}</div><span class="cap">Stacked</span></div>
<div class="tile span2" style="background:{lbg}"><div style="--symw:130px">{ml['symbol']}</div><span class="cap">Symbol</span></div>
<div class="tile span2" style="background:{lbg}"><div style="--wmh:70px">{ml['wordmark']}</div><span class="cap">Wordmark</span></div>
<div class="tile span2" style="background:{lbg}"><div style="display:flex;align-items:center;gap:18px"><div style="--lkh:50px">{ml['lockup']}</div><span style="font-family:var(--text);font-size:27px;color:{ink_l};opacity:.75;border-left:1px solid #C9CBD1;padding-left:18px">Solutions</span></div><span class="cap">Full name lockup</span></div>"""
    else:
        logo_tiles = f"""
<div class="tile span4" style="background:{lbg};min-height:300px"><div style="--wmh:130px">{ml['wordmark']}</div><span class="cap">Primary wordmark · cobalt on porcelain</span></div>
<div class="tile span2 dark" style="background:{dbg}"><div style="--wmh:76px">{md['wordmark']}</div><span class="cap">Reversed</span></div>
<div class="tile span2" style="background:#fff"><div style="text-align:center"><div style="--wmh:72px;display:inline-block">{ml['wordmark']}</div><div style="font-family:var(--text);font-size:15px;letter-spacing:.32em;text-transform:uppercase;color:#0E1124;margin-top:12px">Solutions</div></div><span class="cap">Full name lockup</span></div>
<div class="tile span2" style="background:{lbg}"><div style="--symw:110px">{ml['symbol']}</div><span class="cap">Small mark (needs work)</span></div>
<div class="tile span2" style="background:#1838C9"><div style="--wmh:70px">{paint(asset('C','master-wordmark.svg'),{'*':'#FFFFFF'},'wm')}</div><span class="cap" style="color:rgba(255,255,255,.6)">On cobalt</span></div>"""
    logo = f"""<section><h2><b>02</b> Logo system: wordmark and symbol</h2><div class="tiles">{logo_tiles}
<div class="tile span2" style="background:#fff"><div style="--lkh:44px;--wmh:44px">{mono_l}</div><span class="cap">One colour · black</span></div>
<div class="tile span2 dark" style="background:#111"><div style="--lkh:44px;--wmh:44px">{mono_d}</div><span class="cap">One colour · white</span></div>
<div class="tile span2" style="background:#fff"><div class="sizes">{sizes}<figure><img src="{app_icon}" width="96" height="96" style="image-rendering:auto"><span>App icon</span></figure></div><span class="cap">Favicon and app icon renders</span></div>
</div></section>"""
    # explorations
    ex = explorations(c)
    exbg = "#0B1531" if c is A else "#FFFFFF"
    expl = "".join(f"""<div class="ex {'ch' if chosen else ''}"><div class="vis" style="background:{exbg}">{svg}</div>
<div class="t"><b>{t}<span class="tag" style="background:{'var(--mark)' if chosen else '#ECEDEF'};color:{'#fff' if chosen else '#5A5E68'}">{'Chosen' if chosen else 'Explored'}</span></b><p>{v}</p></div></div>""" for svg, t, v, chosen in ex)
    explore = f'<section><h2><b>03</b> Symbol and wordmark exploration</h2><div class="expl" style="--mark:{"#0C8C9D" if c is A else "#FF5A1F" if c is B else "#1838C9"}">{expl}</div></section>'
    # colour
    def txt_on(h):
        h = h.lstrip("#")
        r, g, bb = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        return "#111" if (0.2126 * r + 0.7152 * g + 0.0722 * bb) > .5 else "#fff"
    sw = "".join(f'<div style="background:{h};color:{txt_on(h)}"><b>{n}</b><code>{h.upper()}</code><small>{u}</small></div>' for n, h, u in c["swatches"])
    scales = ""
    for key in ("primary", "accent", "neutral"):
        st = pal["scales"][key]["steps"]
        scales += f'<div class="k">{key} scale (OKLCH, 50–950)</div><div class="scale">' + "".join(
            f'<div style="background:{v};color:{txt_on(v)}">{k}</div>' for k, v in st.items()) + "</div>"
    prop_cols = {"A": [("#0B1531", 58), ("#121C3A", 18), ("#F1F3F7", 14), ("#3DDCF4", 7), ("#8B7BFF", 3)],
                 "B": [("#F1F1EE", 55), ("#FFFFFF", 18), ("#17191F", 22), ("#70737C", 2), ("#FF5A1F", 3)],
                 "C": [("#F7F7F4", 60), ("#FFFFFF", 12), ("#0E1124", 20), ("#1838C9", 7), ("#5EF0C0", 1)]}[sid]
    prop = '<div class="k">Proportion of use</div><div class="prop">' + "".join(f'<i style="background:{h};width:{w}%;border:1px solid #DADBDF"></i>' for h, w in prop_cols) + "</div>"
    a = checks_line(sid)
    colour = f"""<section><h2><b>04</b> Colour palette</h2><div class="sw">{sw}</div>{prop}
<div class="two" style="margin-top:8px"><div>{scales}</div><div><div class="k">Measured (palette_audit)</div><p class="p">{pal.get('direction','')}<br>
All text roles pass WCAG AA in light and dark mode. The pipeline gates (contrast, glyph coverage, licences, logo renders) all pass.
{'Ion Cyan is 1.65:1 on white, so on light pages it is used as a fill with dark text, never as text.' if c is A else 'Ember is 2.76:1 on concrete, so it is a fill colour only; ember text uses #B13706.' if c is B else 'Signal Mint is 1.33:1 on porcelain, so it is used only on Ink or other dark surfaces.'}</p></div></div></section>"""
    # type
    tp = c["type_pair"]
    greek = "Ιστοσελίδες, λογισμικό και αυτοματισμοί, σχεδιασμένα να διαρκούν."
    typ = f"""<section><h2><b>05</b> Typography</h2><div class="spec"><div>
<div class="specline"><small>Display · {tp[0]}</small><div style="font-family:var(--display);font-size:64px;line-height:1.02">Digital solutions, engineered.</div></div>
<div class="specline"><small>Headline</small><div style="font-family:var(--display);font-size:34px;line-height:1.1">Custom software for teams that outgrew spreadsheets.</div></div>
<div class="specline"><small>Text · {tp[1]}</small><div style="font-family:var(--text);font-size:18px;line-height:1.6;color:#30333B">We design and build websites, web applications and automations, then keep them running. One team from first workshop to production support.</div></div>
<div class="specline"><small>Greek</small><div style="font-family:var(--text);font-size:18px;line-height:1.6">{greek}</div></div>
<div class="specline"><small>Figures</small><div style="font-family:var(--text);font-size:22px;font-variant-numeric:tabular-nums">€ 12,480.00 · 99.2% · 08:45 · 1,204 runs</div></div>
{f'<div class="specline"><small>Code · {tp[2]}</small><div style="font-family:{c["mono"]};font-size:16px;color:#0C8C9D">await elit.deploy({{ env: "production" }})</div></div>' if tp[2] else ''}
</div><div><div class="aa">Aa</div><p class="p" style="margin-top:20px">{c['type_note']}</p><div class="k">Licences</div><p class="p">All faces are open-source (SIL OFL 1.1, Google Fonts): free for logo outlining, web, apps and PDF embedding.</p></div></div></section>"""
    # visual language
    pt1 = pattern_svg(c, 1000, 330, seed=31)
    pt2 = pattern_svg(c, 500, 330, seed=44, dense=1.6)
    prods = product_marks(c)
    pbg, pfg = ("#0B1531", "#F1F3F7") if c is A else ("#FFFFFF", "#17191F")
    prod_html = "".join(f'<div class="prod {"c" if c is C else ""}"><div class="pmw" style="{"width:auto;height:auto" if c is C else ""}">{svg}</div><div><b>{n}</b><span>{r}</span></div></div>' if c is not C else
                        f'<div class="prod c"><div>{svg}</div><span style="margin-top:6px">{r}</span></div>' for svg, n, r in prods)
    vis_note = {"A": "Segment field: rows of bars on the symbol's own grid (bar 18, gap 8). Mostly faint, a few lit cyan and violet: data in motion, never decoration for its own sake. Violet appears only as a soft glow.",
                "B": "Frames and registration marks: a construction grid of crop marks, with chamfered brackets framing content (screens, photos, case studies). The ember core marks one focal point per layout.",
                "C": "Editorial rules: hairline rules on a baseline grid, cobalt overlines marking sections, and mint dots for live data. Typography and rules do all the work; no illustration is needed."}[sid]
    vis = f"""<section><h2><b>06</b> Supporting graphics, patterns and visual language</h2><div class="pats"><div class="pt">{pt1}</div><div class="pt">{pt2}</div></div>
<p class="p" style="margin-top:16px;max-width:1100px">{vis_note}</p>
<div class="k" style="margin-top:30px">Umbrella scalability · product sub-brands (hypothetical names)</div><div class="prods" style="--prodbg:{pbg};--prodfg:{pfg}">{prod_html}</div>
<p class="p" style="margin-top:14px;max-width:1100px">{c['scalability']}</p></section>"""
    # applications
    apps = f"""<section><h2><b>07</b> The identity in use</h2>
<div class="shot"><img src="website.png"><div class="cap">Website · homepage hero (concept mock, not the website build)</div></div>
<div class="apps"><div class="shot"><img src="app.png"><div class="cap">Software application · ElIT Flow dashboard (hypothetical product, sample data)</div></div>
<div class="shot"><img src="business-card.png"><div class="cap">Business card · front and back, 85 × 55 mm (placeholder details)</div></div></div></section>"""
    assess = f"""<section><h2><b>08</b> Assessment</h2><div class="assess">
<div><h3>Strengths</h3><ul>{''.join(f'<li>{x}</li>' for x in c['strengths'])}</ul></div>
<div><h3>Weaknesses and risks</h3><ul>{''.join(f'<li>{x}</li>' for x in c['weaknesses'])}</ul></div>
<div><h3>Scalability</h3><ul><li>{c['scalability']}</li><li>Measured by the brand-identity pipeline: all gates pass (contrast, glyph coverage for English and Greek, font licences, logo renders at 16/32 px).</li></ul></div>
</div></section>"""
    body = hero + strat + logo + explore + colour + typ + vis + apps + assess + \
        f'<div class="foot"><span>ElIT Solutions · Concept {sid} · {c["name"]}</span><span>Draft for review, not final artwork</span></div>'
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>ElIT {c["name"]} board</title>{MONO_LINK}'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=block">'
            f'<style>{fonts(sid)}</style><style>{vars_css(c)}{BOARD_CSS}</style></head><body>{body}</body></html>')


# ============================================================================ comparison board

def comparison():
    cols = []
    for c in CONCEPT_LIST:
        sid = c["id"]
        hm = marks(c, "dark" if c is A else "light")
        md = marks(c, "dark")
        hbg = c["bg"]
        big = (f'<div style="--lkh:64px">{hm["lockup"]}</div>' if sid != "C" else f'<div style="--wmh:86px">{hm["wordmark"]}</div>')
        sw = "".join(f'<i style="background:{h}" title="{n}"></i>' for n, h, _ in c["swatches"][:5])
        swl = " · ".join(f"{n} {h}" for n, h, _ in c["swatches"][:4])
        sym = md["symbol"] if sid != "C" else marks(c, "light")["symbol"]
        symbg = "#0B1531" if c is A else "#17191F" if c is B else "#F7F7F4"
        cols.append(f"""<div class="col {'rec' if c['recommended'] else ''}">
<div class="hd" style="background:{hbg};color:{c['fg']}"><div class="lt">{sid}{' · Recommended' if c['recommended'] else ''}</div><h3 style="font-family:'{c['display']}'">{c['name']}</h3><div class="big">{big}</div></div>
<div class="row"><small>Idea</small><p>{c['one_liner']} {c['idea'].split('. ')[0]}.</p></div>
<div class="row"><small>Symbol · 16 px · app icon</small><div class="syms"><div class="sb" style="background:{symbg};--symw:70px">{sym}</div>
<img src="../elit-solutions/sets/{sid}/logo/build/favicon-16.png" width="32" height="32" style="image-rendering:pixelated"><img src="../elit-solutions/sets/{sid}/logo/build/app-icon-512.png" width="72" height="72"></div></div>
<div class="row"><small>Palette</small><div class="sw">{sw}</div><p class="mini">{swl}</p></div>
<div class="row"><small>Type · {c['type_pair'][0]} / {c['type_pair'][1]}</small><div style="font-family:'{c['display']}';font-size:34px;line-height:1.05">Digital solutions, engineered.</div><p style="font-family:'{c['text']}';margin-top:8px">Websites, custom software and automation, engineered to last.</p></div>
<div class="row"><small>Pattern</small><div class="pt">{pattern_svg(c, 460, 120, seed=9, dense=(.3 if c is B else 1))}</div></div>
<div class="row"><small>In use</small><img class="shot" src="../{c['slug']}/website.png"><img class="shot" src="../{c['slug']}/app.png"><img class="shot" src="../{c['slug']}/business-card.png"></div>
<div class="row"><small>Personality</small><p>{', '.join(c['personality'])}</p></div>
<div class="row"><small>Strongest at</small><p>{c['strengths'][0]}</p></div>
<div class="row"><small>Main risk</small><p>{c['weaknesses'][0]}</p></div>
<div class="row"><small>Umbrella scalability</small><p>{c['scalability'].split('. ')[0]}.</p></div></div>""")
    css = """*{box-sizing:border-box;margin:0;padding:0}body{width:1600px;background:#EDEEF0;font-family:'Inter',system-ui,sans-serif;color:#14161C;-webkit-font-smoothing:antialiased}
.top{padding:44px 56px 30px;display:flex;justify-content:space-between;align-items:flex-end}.top h1{font-size:44px;letter-spacing:-.02em}.top p{font-size:15px;color:#5A5E68;margin-top:8px;max-width:900px;line-height:1.5}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;padding:0 56px 56px}
.col{background:#fff;border:1px solid #DADBDF}.col.rec{outline:3px solid #0C8C9D;outline-offset:-1px}
.hd{padding:24px 26px 30px;min-height:290px}.lt{font-size:12px;letter-spacing:.16em;text-transform:uppercase;opacity:.7}.hd h3{font-size:44px;margin-top:10px;font-weight:700}
.big{margin-top:44px}.lk{height:var(--lkh);width:auto;display:block}.wm{height:var(--wmh);width:auto;display:block}.sym{width:var(--symw);height:auto;display:block}
.row{padding:16px 26px;border-top:1px solid #EEEFF1}.row small{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#8A8E98;margin-bottom:10px}.row p{font-size:14px;line-height:1.5;color:#30333B}
.syms{display:flex;gap:18px;align-items:center}.sb{padding:14px;display:flex}.sw{display:flex;height:40px}.sw i{flex:1;border:1px solid #E3E4E7}.mini{font-family:'JetBrains Mono',monospace;font-size:11px!important;margin-top:8px;color:#5A5E68!important}
.pt svg{width:100%;height:auto;display:block}.shot{width:100%;display:block;border:1px solid #E3E4E7;margin-bottom:8px}
.foot{padding:0 56px 40px;font-size:12px;color:#8A8E98}"""
    allfonts = "".join(fonts(c["id"]) for c in CONCEPT_LIST)
    body = (f'<div class="top"><div><h1>ElIT Solutions · Three identity directions</h1><p>Phase 1 exploration, three genuinely different routes. '
            f'A Signal is the closest to the brief\'s taste, B Frame is the strongest umbrella system, C Edition is the creative wildcard. '
            f'Nothing is final: pick a direction (or parts of several) to refine.</p></div><div style="font-size:13px;color:#5A5E68">v0.1 · 16 Nov 2026</div></div>'
            f'<div class="grid">{"".join(cols)}</div><div class="foot">All three pass the brand-identity pipeline gates (contrast, English and Greek glyph coverage, OFL licences, 16/32 px logo renders). Mocks use sample copy and data.</div>')
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>ElIT concepts comparison</title>{MONO_LINK}'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=block">'
            f'<style>{allfonts}</style><style>{css}</style></head><body>{body}</body></html>')


# ============================================================================ main

def export_logo_files(c, out):
    d = os.path.join(out, "logo")
    os.makedirs(d, exist_ok=True)
    b = os.path.join(WORK, "sets", c["id"], "logo", "build")
    for f in os.listdir(b):
        if f.endswith((".svg", ".png")) and not f.startswith("master-symbol-small") or f == "master-symbol-small.svg":
            shutil.copy(os.path.join(b, f), os.path.join(d, f))
    write(os.path.join(out, "pattern.svg"), pattern_svg(c, 1600, 900, seed=21))
    shutil.copy(os.path.join(WORK, "sets", c["id"], "palette.json"), os.path.join(out, "palette.json"))


def main():
    only = sys.argv[1:]
    for c in CONCEPT_LIST:
        if only and c["id"] not in only and "cmp" not in only:
            continue
        if only and c["id"] not in only:
            continue
        out = os.path.join(CONCEPTS, c["slug"])
        os.makedirs(out, exist_ok=True)
        print(c["id"], c["name"])
        export_logo_files(c, out)
        for name, fn, w, h in (("website", website, 1440, 900), ("app", app, 1440, 900), ("business-card", cards, 1440, 820)):
            p = os.path.join(out, f"{name}.html")
            write(p, fn(c))
            render(p, os.path.join(out, f"{name}.png"), w, h)
        p = os.path.join(out, "board.html")
        write(p, board(c, out))
        render(p, os.path.join(out, "board.png"), 1600, 1000, full=True)
    if not only or "cmp" in only:
        p = os.path.join(CONCEPTS, "comparison", "comparison.html")
        write(p, comparison())
        render(p, os.path.join(CONCEPTS, "comparison", "comparison.png"), 1600, 1000, full=True)


if __name__ == "__main__":
    main()
