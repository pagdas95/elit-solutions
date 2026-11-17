#!/usr/bin/env python3
"""ElIT Solutions identity v1.0-rc: logo package, brand board, refinement sheet and mocks (dark-first).

Uses the regularised mark (mark.py), the outlined wordmark from the brand-identity build and outlined Lexend Light
for SOLUTIONS. Run after write_sets.py / brand.py build / patch_palette.py / brand.py kit:

    .venv/bin/python brand/identity/tools/package.py
"""
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ID = os.path.join(ROOT, "brand", "identity")
WORK = os.path.join(ID, "elit-solutions")
BUILD = os.path.join(WORK, "sets", "A", "logo", "build")
OUT = os.path.join(ID, "logo")
SKILL = os.path.join(ROOT, ".claude", "skills", "brand-identity", "scripts")
PY = os.path.join(ROOT, ".venv", "bin", "python")
REFS = os.path.join(ROOT, "brand", "identity", "reference")   # the client's original kit images
sys.path.insert(0, HERE)
sys.path.insert(0, SKILL)
import mark  # noqa: E402
import logolib  # noqa: E402
import site_preview  # noqa: E402
import cairosvg  # noqa: E402

# ----------------------------------------------------------------------------- colour
MID, NAVY, CYAN, BLUE, VIOLET, ICE = "#080D1B", "#17243B", "#36D9FF", "#5FA2FF", "#9174FF", "#F4F7FF"
DCYAN, DBLUE, DVIOLET, INK = "#0A86B0", "#2F6BE0", "#6A4BEB", "#111C2E"
WAYS = {   # colourway -> (top, mid, bottom, "El", "IT", SOLUTIONS)
    "dark": (CYAN, BLUE, VIOLET, ICE, CYAN, ICE),
    "light": (DCYAN, DBLUE, DVIOLET, INK, DCYAN, INK),
    "mono-white": (ICE,) * 6,
    "mono-midnight": (MID,) * 6,
    "mono-black": ("#000000",) * 6,
}


def lum(h):
    c = [int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def cr(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True)
    return (x + .05) / (y + .05)


# ----------------------------------------------------------------------------- outlines
def _wordmark():
    svg = open(os.path.join(BUILD, "master-wordmark.svg")).read()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    el = re.search(r'<path d="([^"]+)"', svg).group(1)
    it = re.search(r'data-parts="wordmark-detail-it" d="([^"]+)"', svg).group(1)
    return vb, el, it


def _solutions():
    ident = json.load(open(os.path.join(WORK, "sets.json")))["sets"][0]["identity"]
    font = logolib.font_for(ident, os.path.join(WORK, "sets", "A"), "display", {"wght": 300})
    d = logolib.text_path("SOLUTIONS", font, {"wght": 300}, cap=100, x=0, baseline=100, tracking=430)
    n = [float(v) for v in re.findall(r"-?\d+\.?\d*", d)]
    return d, (min(n[0::2]), min(n[1::2]), max(n[0::2]), max(n[1::2]))


WVB, EL, IT = _wordmark()
SOL, SB = _solutions()
MX0, MY0, MX1, MY1 = mark.bbox()


def mark_g(x, y, h, way, gradient=False, uid="gr"):
    """The symbol, height h, top-left at (x, y)."""
    k = h / (MY1 - MY0)
    cols = WAYS[way][:3]
    out, defs = [], ""
    if gradient:
        defs = (f'<linearGradient id="{uid}" gradientUnits="userSpaceOnUse" x1="{x}" y1="{y}" x2="{x}" y2="{y + h}">'
                f'<stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{BLUE}"/>'
                f'<stop offset="1" stop-color="{VIOLET}"/></linearGradient>')
    for (pid, ps), c in zip(mark.PIECES.items(), cols):
        pts = " ".join(f"{x + (mark.xy(*p)[0] - MX0) * k:.3f},{y + (mark.xy(*p)[1] - MY0) * k:.3f}" for p in ps)
        out.append(f'<polygon id="{pid}" points="{pts}" fill="{f"url(#{uid})" if gradient else c}"/>')
    return "".join(out), defs, (MX1 - MX0) * k


def lockup(kind="primary", way="dark", gradient=False, pad=None):
    """primary: symbol + ElIT over SOLUTIONS · compact: symbol + ElIT · stacked · wordmark · symbol."""
    _, _, _, el_c, it_c, sol_c = WAYS[way]
    wx0, wy0, ww, wh = WVB
    cap, gap = 100.0, 30.0
    s_scale = ww / (SB[2] - SB[0])
    s_h = (SB[3] - SB[1]) * s_scale
    block = cap + gap + s_h
    parts, defs = [], []

    def word(x, y, sol=True):
        g = (f'<g transform="translate({x - wx0:.3f} {y:.3f})"><path d="{EL}" fill="{el_c}"/>'
             f'<path d="{IT}" fill="{it_c}"/></g>')
        if sol:
            g += (f'<g transform="translate({x:.3f} {y + cap + gap:.3f}) scale({s_scale:.5f}) '
                  f'translate({-SB[0]:.3f} {-SB[1]:.3f})"><path d="{SOL}" fill="{sol_c}"/></g>')
        return g

    if kind == "primary":
        mh = block * 1.06
        g, d, mw = mark_g(0, -(mh - block) / 2, mh, way, gradient)
        parts += [g, word(mw + 52, 0)]
        defs.append(d)
        W, H, X0, Y0 = mw + 52 + ww, mh, 0, -(mh - block) / 2
    elif kind == "compact":
        mh = cap * 1.42
        g, d, mw = mark_g(0, -(mh - cap) / 2, mh, way, gradient)
        parts += [g, word(mw + 40, 0, sol=False)]
        defs.append(d)
        W, H, X0, Y0 = mw + 40 + ww, mh, 0, -(mh - cap) / 2
    elif kind == "stacked":
        mh = block * 1.25
        k = mh / (MY1 - MY0)
        mw = (MX1 - MX0) * k
        g, d, _ = mark_g((ww - mw) / 2, 0, mh, way, gradient)
        parts += [g, word(0, mh + 64)]
        defs.append(d)
        W, H, X0, Y0 = ww, mh + 64 + block, 0, 0
    elif kind == "wordmark":
        parts.append(word(0, 0))
        W, H, X0, Y0 = ww, block, 0, 0
    else:  # symbol
        g, d, mw = mark_g(0, 0, 100, way, gradient)
        parts.append(g)
        defs.append(d)
        W, H, X0, Y0 = mw, 100, 0, 0
    p = pad if pad is not None else 0.0
    dd = "".join(x for x in defs if x)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{X0 - p:.2f} {Y0 - p:.2f} {W + 2 * p:.2f} {H + 2 * p:.2f}">'
            + (f"<defs>{dd}</defs>" if dd else "") + "".join(parts) + "</svg>")


def app_icon(style="midnight"):
    bg = {"midnight": MID, "navy": NAVY, "white": "#FFFFFF", "gradient": "url(#tile)"}[style]
    way = {"midnight": "dark", "navy": "dark", "white": "light", "gradient": "mono-white"}[style]
    g, _, mw = mark_g(0, 0, 60, way)
    tx, ty = 50 - mw / 2, 20.5
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><linearGradient id="tile" x1="0" y1="0" '
            f'x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient></defs>'
            f'<rect width="100" height="100" rx="22.37" fill="{bg}"/><g transform="translate({tx:.3f} {ty:.3f})">{g}</g></svg>')


def favicon_svg():
    g, _, mw = mark_g(0, 0, 100, "dark")
    side = 108.0
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{mw / 2 - side / 2:.2f} -4 {side} {side}">'
            f'<style>@media (prefers-color-scheme: light){{#layer-top{{fill:{DCYAN}}}#layer-mid{{fill:{DBLUE}}}#layer-bottom{{fill:{DVIOLET}}}}}</style>{g}</svg>')


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(s)


def png(svg_path, png_path, w=None, h=None, bg=None):
    os.makedirs(os.path.dirname(png_path), exist_ok=True)
    kw = {"output_width": w} if w else {}
    if h:
        kw["output_height"] = h
    if bg:
        kw["background_color"] = bg
    cairosvg.svg2png(url=svg_path, write_to=png_path, **kw)


def build_package():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    files = []
    for kind in ("primary", "compact", "stacked", "wordmark", "symbol"):
        for way in WAYS:
            if kind == "symbol" and way == "mono-black":
                pass
            p = os.path.join(OUT, "svg", f"elit-{kind}-{way}.svg")
            write(p, lockup(kind, way))
            files.append(p)
        p = os.path.join(OUT, "svg", f"elit-{kind}-dark-gradient.svg")
        if kind != "wordmark":
            write(p, lockup(kind, "dark", gradient=True))
            files.append(p)
    for st in ("midnight", "navy", "white", "gradient"):
        write(os.path.join(OUT, "app-icon", f"app-icon-{st}.svg"), app_icon(st))
        png(os.path.join(OUT, "app-icon", f"app-icon-{st}.svg"), os.path.join(OUT, "app-icon", f"app-icon-{st}-1024.png"), 1024, 1024)
    fav = os.path.join(OUT, "favicon", "favicon.svg")
    write(fav, favicon_svg())
    for px in (16, 32, 48, 180, 192, 512):
        png(fav, os.path.join(OUT, "favicon", f"favicon-{px}.png"), px, px)
    subprocess.run([PY, os.path.join(ROOT, ".claude", "skills", "logo-design", "scripts", "render_png.py"), fav, "--ico",
                    os.path.join(OUT, "favicon", "favicon.ico"), "--ico-sizes", "16", "32", "48"], check=True,
                   capture_output=True)
    for p in files:   # PNG exports, transparent, 2000 px wide (symbol 1024)
        name = os.path.basename(p)[:-4]
        w = 1024 if "-symbol-" in name else 2000
        png(p, os.path.join(OUT, "png", name + ".png"), w)
    print("  logo package:", sum(len(f) for _, _, f in os.walk(OUT)), "files")


# ----------------------------------------------------------------------------- pages
def fonts_css():
    d = os.path.join(WORK, "sets", "A")
    css, _ = site_preview.identity_fonts_css(d, json.load(open(os.path.join(d, "identity.json"))))
    return css


HEAD = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=block">'
BASE = """*{box-sizing:border-box;margin:0;padding:0}body{background:#080D1B;color:#F4F7FF;font-family:'BI text a',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.mono{font-family:'JetBrains Mono',monospace}svg.l{display:block;height:var(--h);width:auto}svg.a{display:block;width:var(--w);height:var(--w)}"""


def L(kind="primary", way="dark", h=60, gradient=False):
    return lockup(kind, way, gradient).replace("<svg ", f'<svg class="l" style="--h:{h}px" ', 1)


def A(style, w=96):
    return app_icon(style).replace("<svg ", f'<svg class="a" style="--w:{w}px" ', 1)


def page(body, css, w, h=None):
    size = f"html,body{{width:{w}px;height:{h}px;overflow:hidden}}" if h else f"body{{width:{w}px}}"
    return f'<!doctype html><html><head><meta charset="utf-8">{HEAD}<style>{fonts_css()}{BASE}{size}{css}</style></head><body>{body}</body></html>'


def slabs_pattern(w, h, seed=3, lit=True):
    """Supporting graphic: isometric slabs on the mark's lattice, faint, with one lit ramp."""
    import random
    rnd = random.Random(seed)
    U = max(w, h) / 64.0
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice">']
    for _ in range(26):
        a0, b0 = rnd.randint(-30, 50), rnd.randint(-10, 50)
        la, lb = rnd.choice([6, 8, 10, 14]), rnd.choice([3, 4, 5])
        pts = [(a0, b0), (a0 + la, b0), (a0 + la, b0 + lb), (a0, b0 + lb)]
        xy = [(mark.xy(a, b)[0] * U, mark.xy(a, b)[1] * U + h * .45) for a, b in pts]
        r = rnd.random()
        col, op = (CYAN, .9) if lit and r < .06 else (VIOLET, .8) if lit and r < .1 else (BLUE, .14) if r < .35 else ("#F4F7FF", .035)
        out.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in xy)}" fill="{col}" fill-opacity="{op}"/>')
    out.append("</svg>")
    return "".join(out)


def website():
    body = f"""<div class="w"><div class="pat">{slabs_pattern(1440, 900)}</div>
<header>{L("primary", "dark", 50)}<nav><a>Services</a><a>Products</a><a>Work</a><a>Company</a></nav><div class="cta">Start a project</div></header>
<main><div class="eb mono">SOFTWARE ENGINEERING · CYPRUS</div><h1>Digital solutions,<br><span>engineered.</span></h1>
<p>Websites, custom software, automation and integrations, designed and built in Cyprus for teams across Europe.</p>
<div class="b"><div class="b1">Start a project →</div><div class="b2">See our work</div></div></main>
<div class="art">{L("symbol", "dark", 470, gradient=True)}</div>
<div class="svc">{''.join(f'<div class="s"><i></i><b>{a}</b><span>{b}</span></div>' for a, b in [("Websites", "Fast, accessible web platforms"), ("Custom software", "Web apps and internal tools"), ("Automation", "Workflows without busywork"), ("Integrations", "Systems that talk reliably")])}</div>
<div class="lbl">Concept mock · sample copy · not the website build</div></div>"""
    css = """.w{position:relative;width:1440px;height:900px;background:radial-gradient(900px 620px at 80% 38%,rgba(145,116,255,.24),transparent 62%),radial-gradient(700px 500px at 66% 80%,rgba(54,217,255,.12),transparent 60%),#080D1B;overflow:hidden}
.pat{position:absolute;inset:0}.pat svg{width:100%;height:100%}
header{position:relative;display:flex;align-items:center;padding:30px 72px;gap:40px}nav{display:flex;gap:30px;font-size:15px;color:#B8C2DB;margin-left:auto}
.cta{background:#36D9FF;color:#080D1B;padding:11px 18px;border-radius:999px;font-weight:600;font-size:14px;margin-left:16px}
main{position:absolute;left:72px;top:220px;width:650px}.eb{font-size:13px;letter-spacing:.2em;color:#8E9AB8}
h1{font-weight:700;font-size:74px;line-height:1.02;letter-spacing:-.03em;margin-top:22px}h1 span{color:#36D9FF}
p{font-size:19px;line-height:1.6;color:#B8C2DB;margin-top:24px;max-width:540px}.b{display:flex;gap:14px;margin-top:36px}
.b1{background:#36D9FF;color:#080D1B;padding:15px 24px;border-radius:999px;font-weight:600}.b2{border:1px solid #33456E;padding:15px 24px;border-radius:999px}
.art{position:absolute;right:150px;top:170px;filter:drop-shadow(0 0 50px rgba(54,217,255,.30)) drop-shadow(0 0 110px rgba(145,116,255,.35))}
.svc{position:absolute;left:72px;right:72px;bottom:54px;display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.s{background:rgba(23,36,59,.88);border:1px solid #22345A;border-radius:14px;padding:20px}.s i{display:block;width:28px;height:4px;background:linear-gradient(90deg,#36D9FF,#9174FF);margin-bottom:14px}
.s b{display:block;font-size:17px}.s span{font-size:14px;color:#9AA6C4}.lbl{position:absolute;right:14px;bottom:10px;font-size:11px;color:#46557A}"""
    return page(body, css, 1440, 900)


def cards():
    body = f"""<div class="desk"><div class="lb" style="left:90px">FRONT</div><div class="lb" style="left:755px">BACK</div>
<div class="c f"><div class="pat">{slabs_pattern(595, 385, 9)}</div><div class="lg">{L("primary", "dark", 112)}</div></div>
<div class="c bk"><b>Alex Constantinou</b><span>Founder &amp; Technical Director</span><i class="rule"></i>
<div class="ct mono">+357 99 000 000<br>alex@elitsolutions.cy<br>elitsolutions.cy<br>Limassol, Cyprus</div><div class="sm">{L("symbol", "light", 64)}</div></div>
<div class="foot">Business card · 85 × 55 mm · placeholder name and contact details · Midnight front, Ice White back</div></div>"""
    css = """.desk{position:relative;width:1440px;height:820px;background:radial-gradient(800px 500px at 50% 40%,#232A3B,#11151F)}
.c{position:absolute;width:595px;height:385px;border-radius:10px;overflow:hidden;box-shadow:0 40px 80px -30px rgba(0,0,0,.75)}
.f{left:90px;top:190px;background:#080D1B}.f .pat{position:absolute;inset:0;opacity:.8}.f .lg{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)}
.bk{left:755px;top:190px;background:#F4F7FF;color:#111C2E;padding:46px 52px}.bk b{font-size:26px;display:block;font-weight:600}.bk span{font-size:14px;color:#4A566A}
.rule{display:block;width:56px;height:4px;margin-top:18px;background:linear-gradient(90deg,#0A86B0,#6A4BEB)}
.ct{position:absolute;left:52px;bottom:42px;font-size:13px;line-height:1.75}.sm{position:absolute;right:50px;bottom:40px}
.lb{position:absolute;top:150px;font-size:12px;letter-spacing:.14em;color:#7A869F}.foot{position:absolute;left:90px;bottom:120px;font-size:13px;color:#7A869F}"""
    return page(body, css, 1440, 820)


def phone():
    body = f"""<div class="ph"><div class="scr"><div class="pat">{slabs_pattern(390, 844, 5)}</div><div class="mk">{L("stacked", "dark", 250)}</div>
<div class="tag">Digital solutions, engineered.</div></div></div>"""
    css = """html,body{background:#11151F}.ph{width:430px;height:884px;margin:0 auto;border-radius:58px;background:#05070D;padding:20px;box-shadow:inset 0 0 0 2px #2A3245}
.scr{position:relative;height:100%;border-radius:40px;overflow:hidden;background:radial-gradient(400px 400px at 50% 40%,rgba(145,116,255,.28),transparent 70%),#080D1B}
.pat{position:absolute;inset:0;opacity:.7}.mk{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%)}.tag{position:absolute;bottom:70px;width:100%;text-align:center;color:#9AA6C4;font-size:15px}"""
    return page(body, css, 430, 884)


def brand_board():
    sw = [("Midnight", MID, ICE, "Ground · 60%"), ("Navy", NAVY, ICE, "Surfaces, cards"), ("Cyan", CYAN, MID, "Top slab, IT, actions"),
          ("Layer Blue", BLUE, MID, "Middle slab, charts"), ("Violet", VIOLET, MID, "Bottom slab, glow"), ("Ice White", ICE, MID, "Type on dark")]
    deep = [("Deep Cyan", DCYAN), ("Deep Blue", DBLUE), ("Deep Violet", DVIOLET), ("Ink", INK)]
    vars_ = [("Primary · dark", L("primary", "dark", 64), MID), ("Primary · light", L("primary", "light", 64), ICE),
             ("One colour · white", L("primary", "mono-white", 64), NAVY), ("One colour · midnight", L("primary", "mono-midnight", 64), "#FFFFFF"),
             ("Compact", L("compact", "dark", 52), MID), ("Symbol · gradient (digital)", L("symbol", "dark", 96, True), MID)]
    body = f"""
<div class="top"><span>ELIT SOLUTIONS — BRAND IDENTITY</span><span class="badge">v1.0 · final</span></div>
<div class="hero"><div class="pat">{slabs_pattern(1600, 620, 12, lit=False)}</div><div class="hl">{L("primary", "dark", 230)}</div>
<div class="hc"><h2>Layered E</h2><p>An isometric E folded from three slabs, cyan to blue to violet: a system built in layers. Your mark, rebuilt on a true 30° grid with one gap and two equal notches, so it is exact at every size.</p></div></div>
<div class="row3">
<div class="cell"><h3>Colour</h3><div class="sw">{''.join(f'<div style="background:{h};color:{f}"><b>{n}</b><code>{h}</code><small>{u}</small></div>' for n, h, f, u in sw)}</div>
<div class="deep"><span>On light grounds</span>{''.join(f'<i style="background:{h}"></i><code>{n} {h}</code>' for n, h in deep)}</div>
<div class="grad"><i style="background:linear-gradient(90deg,{CYAN},{BLUE},{VIOLET})"></i><span>Brand ramp · Cyan → Layer Blue → Violet (digital surfaces only)</span></div></div>
<div class="cell"><h3>Typography</h3><div class="ty"><div class="t1">Lexend</div><small>Logo only · outlined · Bold 700 / Light 300</small>
<div class="t2">Geologica</div><small>Headings and UI · English + Greek · tabular figures</small><div class="t3 mono">JetBrains Mono</div><small>Code and data</small>
<p class="gk">Ιστοσελίδες, λογισμικό και αυτοματισμοί.</p></div></div>
<div class="cell"><h3>Visual language</h3><div class="vl"><div class="v1">{slabs_pattern(300, 200, 21)}</div><div class="v2"></div><div class="v3">{L("symbol", "mono-white", 120)}</div></div>
<small class="vn">Isometric slabs on the mark's lattice · ramp surfaces · large crop of the symbol</small></div></div>
<div class="apps"><div class="web"><img src="mock-website.png"></div><div class="phone"><img src="mock-phone.png"></div>
<div class="icons"><div class="ai">{A("navy", 150)}</div><span>App icon</span><div class="fv"><img src="../logo/favicon/favicon-48.png" width="48"><img src="../logo/favicon/favicon-32.png" width="32"><img src="../logo/favicon/favicon-16.png" width="16"></div><span>Favicon 48 / 32 / 16 (actual pixels)</span></div>
<div class="card"><img src="mock-business-card.png"></div></div>
<div class="vars">{''.join(f'<div class="vv"><div class="vb" style="background:{bg}">{svg}</div><span>{n}</span></div>' for n, svg, bg in vars_)}</div>
<div class="foot"><span>Refined from the client kit · mark on an isometric lattice · wordmark fixed so ElIT never reads EIIT</span><span>Sample copy and placeholder details in mocks</span></div>"""
    css = """body{background:#080D1B}.top{display:flex;justify-content:space-between;align-items:center;padding:30px 56px;font-size:14px;letter-spacing:.22em;color:#C9D1E6}
.badge{background:linear-gradient(90deg,#36D9FF,#9174FF);color:#080D1B;padding:8px 16px;border-radius:8px;font-weight:700;letter-spacing:.06em}
.hero{position:relative;height:430px;margin:0 56px;border-radius:18px;overflow:hidden;background:radial-gradient(800px 420px at 25% 40%,rgba(145,116,255,.22),transparent 65%),#0B1224;border:1px solid #1C2946;display:flex;align-items:center;padding:0 60px}
.hero .pat{position:absolute;inset:0;opacity:.7}.hero .pat svg{width:100%;height:100%}.hl{position:relative}
.hc{position:relative;margin-left:auto;width:430px;border-left:1px solid #2A3A62;padding-left:40px}.hc h2{font-size:44px;letter-spacing:-.02em}.hc p{color:#B8C2DB;font-size:17px;line-height:1.6;margin-top:14px}
.row3{display:grid;grid-template-columns:1.15fr .85fr 1fr;gap:22px;margin:22px 56px}.cell{background:#0B1224;border:1px solid #1C2946;border-radius:16px;padding:24px}
h3{font-size:13px;letter-spacing:.2em;text-transform:uppercase;color:#8E9AB8;margin-bottom:16px;font-weight:600}
.sw{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.sw div{height:96px;border-radius:10px;padding:11px;display:flex;flex-direction:column;justify-content:flex-end;font-size:12px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.08)}
.sw b{font-size:14px}.sw code{font-family:'JetBrains Mono',monospace}.sw small{opacity:.75}
.deep{display:grid;grid-template-columns:18px 1fr 18px 1fr;align-items:center;gap:8px;margin-top:14px;font-size:12px;color:#9AA6C4}.deep span{grid-column:1/-1;letter-spacing:.12em;text-transform:uppercase;font-size:11px}
.deep i{width:18px;height:18px;border-radius:5px}.deep code{font-family:'JetBrains Mono',monospace;margin-right:10px}
.grad{margin-top:14px}.grad i{display:block;height:22px;border-radius:8px}.grad span{display:block;font-size:12px;color:#9AA6C4;margin-top:8px}
.ty .t1{font-family:'BI display a';font-weight:700;font-size:46px}.ty .t2{font-family:'BI text a';font-weight:700;font-size:40px;margin-top:14px}.ty .t3{font-size:28px;margin-top:14px;color:#36D9FF}
.ty small{display:block;color:#9AA6C4;font-size:13px;margin-top:4px}.gk{margin-top:16px;font-size:17px;color:#C9D1E6}
.vl{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;height:200px}.vl>div{border-radius:12px;overflow:hidden;border:1px solid #1C2946}.v1 svg{width:100%;height:100%;background:#080D1B}
.v2{background:linear-gradient(150deg,#36D9FF 0%,#5FA2FF 45%,#9174FF 100%)}.v3{background:#17243B;display:flex;align-items:center;justify-content:center}.vn{display:block;color:#9AA6C4;font-size:12px;margin-top:10px}
.apps{display:grid;grid-template-columns:1.55fr .42fr .5fr 1fr;gap:22px;margin:0 56px;align-items:center}.apps img{display:block;width:100%;border-radius:12px}
.web img,.card img{border:1px solid #1C2946}.icons{display:flex;flex-direction:column;align-items:center;gap:10px;color:#9AA6C4;font-size:12px}.fv{display:flex;align-items:flex-end;gap:14px;margin-top:10px}.fv img{width:auto!important;border-radius:0!important;image-rendering:pixelated}
.vars{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;margin:22px 56px}.vv span{display:block;color:#9AA6C4;font-size:12px;margin-top:8px;text-align:center}
.vb{height:130px;border-radius:12px;display:flex;align-items:center;justify-content:center;border:1px solid #1C2946}
.foot{display:flex;justify-content:space-between;padding:14px 56px 36px;color:#5D6A8A;font-size:12px}"""
    return page(body, css, 1600)


def refinement_sheet():
    refs = REFS if REFS and os.path.isdir(REFS) else None
    orig_mono = os.path.join(refs, "client-logo-mono.png") if refs else None
    orig_dark = os.path.join(refs, "client-logo-dark.webp") if refs else None
    # overlay at the original's scale (lattice unit 30 px, origin at the top slab's lower-left corner)
    U, ox, oy = 30.0, 228, 489
    over = "".join(f'<polygon points="{" ".join(f"{ox + mark.xy(*p)[0] * U:.1f},{oy + mark.xy(*p)[1] * U:.1f}" for p in ps)}" '
                   f'fill="#FF2D55" fill-opacity=".28" stroke="#FF2D55" stroke-width="2.5"/>' for ps in mark.PIECES.values())
    lattice = "".join(f'<path d="M{ox + mark.xy(a, -8)[0] * U:.1f} {oy + mark.xy(a, -8)[1] * U:.1f}L{ox + mark.xy(a, 16)[0] * U:.1f} {oy + mark.xy(a, 16)[1] * U:.1f}" stroke="#36D9FF" stroke-opacity=".25"/>' for a in range(-8, 18, 1)) + \
        "".join(f'<path d="M{ox + mark.xy(-8, b)[0] * U:.1f} {oy + mark.xy(-8, b)[1] * U:.1f}L{ox + mark.xy(18, b)[0] * U:.1f} {oy + mark.xy(18, b)[1] * U:.1f}" stroke="#36D9FF" stroke-opacity=".25"/>' for b in range(-8, 18, 1))
    def img(p, extra=""):
        return f'<img src="{os.path.relpath(p, os.path.join(ID, "board"))}" style="{extra}">' if p else '<div class="na">client image not available</div>'
    body = f"""<div class="top"><h1>Refining your kit</h1><p>Same idea, same silhouette, same palette. What changed, and why.</p></div>
<div class="g2"><div class="cell"><h3>1 · The mark: one gap, one lattice</h3><div class="cmp">
<div class="ov"><svg viewBox="180 180 520 610">{f'<image href="{os.path.relpath(orig_mono, os.path.join(ID, "board"))}" x="0" y="0" width="1672" height="941"/>' if orig_mono else ''}{lattice}{over}</svg><span>Your original (black) vs refined (red outline) on the 30° lattice</span></div>
<div class="nb"><div class="b"><b>Before</b><p>Gaps vary from 0.5 to 2 lattice units: the gap between the middle and bottom slabs narrows to a 11 px sliver that clogs at small sizes and in print.</p></div>
<div class="b"><b>After</b><p>Every edge on the 30° isometric grid. One gap (2 units) between all slabs, both fold notches 1.5 units, and the left edges of the middle and bottom slabs aligned. Top and middle slabs are unchanged; the bottom slab moves down one unit.</p></div>
<div class="sz">{''.join(f'<div><img src="../logo/favicon/favicon-{s}.png" style="width:{s * 3}px;height:{s * 3}px;image-rendering:pixelated"><span>{s} px ×3</span></div>' for s in (16, 32))}</div></div></div></div>
<div class="cell"><h3>2 · The wordmark: ElIT, not EIIT</h3><div class="wm"><div class="before">{img(orig_dark, "width:100%;border-radius:10px")}<span>Your kit: l and I are identical bars, so it reads "EIIT" (and only colour separates El from IT)</span></div>
<div class="after">{L("primary", "dark", 120)}<div style="height:18px"></div>{L("primary", "mono-white", 70)}<span>Refined: Lexend's slab-serifed I keeps ElIT readable in colour and in one colour; SOLUTIONS in Lexend Light, outlined</span></div></div></div></div>
<div class="g2"><div class="cell"><h3>3 · Colour: your palette, plus a light-ground set</h3><table>
<tr><th>Your kit</th><th>Refined</th><th>Why</th></tr>
<tr><td><code>#0A0F1F</code> Midnight</td><td><code>{MID}</code> Midnight</td><td>Your typed palette (the kit swatches were near-identical)</td></tr>
<tr><td><code>#06B6D4</code> Electric Cyan</td><td><code>{CYAN}</code> Cyan</td><td>#06B6D4 is Tailwind's stock cyan-500; your #36D9FF is brighter and yours</td></tr>
<tr><td><code>#8B5CF6</code> Violet</td><td><code>{VIOLET}</code> Violet</td><td>#8B5CF6 is Tailwind's stock violet-500</td></tr>
<tr><td><code>#F8FAFC</code> Ice White</td><td><code>{ICE}</code> Ice White</td><td>#F8FAFC is Tailwind's slate-50; yours has the brand's blue tint</td></tr>
<tr><td>—</td><td><code>{NAVY}</code> Navy · <code>{BLUE}</code> Layer Blue</td><td>Surfaces; the middle slab's exact midpoint</td></tr>
<tr><td>—</td><td><code>{DCYAN}</code> <code>{DBLUE}</code> <code>{DVIOLET}</code></td><td>Mark on light grounds: Cyan is {cr(CYAN, ICE):.2f}:1 on Ice White; the deep set reaches {min(cr(DCYAN, ICE), cr(DBLUE, ICE), cr(DVIOLET, ICE)):.2f}:1 or more</td></tr></table></div>
<div class="cell"><h3>4 · Typography and reproduction</h3><ul>
<li><b>Sora + Inter → Lexend (logo) + Geologica + JetBrains Mono.</b> Sora and Lexend have no Greek; Geologica covers Greek for a Cyprus company and has tabular figures. Inter is the most common AI default; Geologica is less generic.</li>
<li><b>Gradients become a flat master.</b> Your kit's shaded, glowing mark cannot be printed, embroidered or cut in vinyl. The master is three flat colours; the gradient and glow stay as digital treatments.</li>
<li><b>White-on-transparent files.</b> Two of your exports (white logo on transparent) look empty on white backgrounds. The package names every file by its ground.</li>
<li><b>Measured, not assumed.</b> The brand-identity pipeline checks contrast, glyph coverage, licences, 16/32 px renders and every logo-on-ground in the guidelines.</li></ul></div></div>"""
    css = """body{background:#080D1B}.top{padding:40px 56px 18px}.top h1{font-size:44px;letter-spacing:-.02em}.top p{color:#9AA6C4;font-size:17px;margin-top:6px}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin:0 56px 22px}.cell{background:#0B1224;border:1px solid #1C2946;border-radius:16px;padding:26px}
h3{font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:#C9D1E6;margin-bottom:18px}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:20px}.ov svg{width:100%;background:#fff;border-radius:12px}.ov span,.wm span{display:block;color:#9AA6C4;font-size:12px;margin-top:8px;line-height:1.5}
.b{border-top:1px solid #1C2946;padding:12px 0}.b b{color:#36D9FF}.b p{color:#C9D1E6;font-size:14px;line-height:1.55;margin-top:6px}.sz{display:flex;gap:24px;align-items:flex-end;margin-top:10px;color:#9AA6C4;font-size:11px}.sz div{display:flex;flex-direction:column;gap:6px;align-items:center}
.wm{display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:start}.after{background:#080D1B;border-radius:10px;padding:24px;border:1px solid #1C2946}.na{color:#5D6A8A;font-size:13px;padding:40px;border:1px dashed #2A3A62;border-radius:10px}
table{width:100%;border-collapse:collapse;font-size:13px}td,th{padding:9px 8px;border-bottom:1px solid #1C2946;text-align:left;vertical-align:top;color:#C9D1E6}th{color:#8E9AB8;font-size:11px;letter-spacing:.12em;text-transform:uppercase}code{font-family:'JetBrains Mono',monospace;color:#F4F7FF}
ul{list-style:none}li{color:#C9D1E6;font-size:14px;line-height:1.6;padding:10px 0;border-top:1px solid #1C2946}li b{color:#F4F7FF}"""
    return page(body, css, 1600)


def render(html, png_path, w, h=None, full=False):
    cmd = [PY, os.path.join(SKILL, "render_png.py"), html, "-o", png_path, "--width", str(w)]
    cmd += ["--height", str(h)] if h else []
    cmd += ["--full-page"] if full else []
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if r.returncode:
        raise RuntimeError(r.stdout + r.stderr)
    print("  ", os.path.relpath(png_path, ROOT))


def main():
    build_package()
    bd = os.path.join(ID, "board")
    for name, fn, w, h in (("mock-website", website, 1440, 900), ("mock-business-card", cards, 1440, 820), ("mock-phone", phone, 430, 884)):
        write(os.path.join(bd, name + ".html"), fn())
        render(os.path.join(bd, name + ".html"), os.path.join(bd, name + ".png"), w, h)
    write(os.path.join(bd, "brand-board.html"), brand_board())
    render(os.path.join(bd, "brand-board.html"), os.path.join(bd, "brand-board.png"), 1600, 1000, full=True)
    write(os.path.join(bd, "refinement.html"), refinement_sheet())
    render(os.path.join(bd, "refinement.html"), os.path.join(bd, "refinement.png"), 1600, 1000, full=True)


if __name__ == "__main__":
    main()
