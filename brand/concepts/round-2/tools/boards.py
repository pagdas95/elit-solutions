#!/usr/bin/env python3
"""Round 2 presentation: Forward and Layers logo directions on the client palette.

Builds outlined lockups (symbol | ElIT / SOLUTIONS), variants, app icons, mocks, a board per direction and a
comparison board. Run after `brand.py logos` for brand/concepts/round-2/elit-solutions:

    .venv/bin/python brand/concepts/round-2/tools/boards.py
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
R2 = os.path.join(ROOT, "brand", "concepts", "round-2")
WORK = os.path.join(R2, "elit-solutions")
SKILL = os.path.join(ROOT, ".claude", "skills", "brand-identity", "scripts")
PY = os.path.join(ROOT, ".venv", "bin", "python")
sys.path.insert(0, SKILL)
import logolib  # noqa: E402
import site_preview  # noqa: E402

# Client palette (exploratory)
MID, NAVY, CYAN, VIOLET, ICE = "#080D1B", "#17243B", "#36D9FF", "#9174FF", "#F4F7FF"
BLUE = "#5FA2FF"                       # computed middle step of the ramp (Layers only)
# Light-ground ("deep") versions, chosen to reach >= 3:1 on Ice White (checked below)
DCYAN, DBLUE, DVIOLET = "#0A86B0", "#2F6BE0", "#6A4BEB"


def lum(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def cr(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + .05) / (lb + .05)


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(s)


def render(html, png, w, h=None, full=False):
    cmd = [PY, os.path.join(SKILL, "render_png.py"), html, "-o", png, "--width", str(w)]
    cmd += ["--height", str(h)] if h else []
    cmd += ["--full-page"] if full else []
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if r.returncode:
        raise RuntimeError(r.stdout + r.stderr)
    print("  ", os.path.relpath(png, ROOT))


# ============================================================================ geometry

def build_dir(sid):
    return os.path.join(WORK, "sets", sid, "logo", "build")


def symbol_parts(sid):
    """[(role, d)] of the resolved symbol on its own viewBox."""
    svg = open(os.path.join(build_dir(sid), "master-symbol.svg")).read()
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    parts = re.findall(r'<path[^>]*data-color="([^"]+)"[^>]*\sd="([^"]+)"', svg)
    return vb, parts


def wordmark_split():
    """El and IT path data from the outlined wordmark (identical in both sets), plus its viewBox."""
    svg = open(os.path.join(build_dir("A"), "master-wordmark.svg")).read()
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    d = " ".join(re.findall(r'\sd="([^"]+)"', svg))
    glyphs = json.load(open(os.path.join(build_dir("A"), "wordmark-glyphs.json")))["glyphs"]
    cut = (glyphs[1]["x1"] + glyphs[2]["x0"]) / 2
    el, it = [], []
    for sub in re.findall(r"M[^M]+", d):
        xs = [float(v) for v in re.findall(r"-?\d+\.?\d*", sub)[0::2]]
        (el if min(xs) < cut else it).append(sub.strip())
    return vb, " ".join(el), " ".join(it)


def solutions_d():
    ident = json.load(open(os.path.join(WORK, "sets.json")))["sets"][0]["identity"]
    font = logolib.font_for(ident, os.path.join(WORK, "sets", "A"), "display", {"wght": 300})
    return logolib.text_path("SOLUTIONS", font, {"wght": 300}, cap=100, x=0, baseline=100, tracking=420)


def path_box(d):
    nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", d)]
    xs, ys = nums[0::2], nums[1::2]
    return min(xs), min(ys), max(xs), max(ys)


VB_W, EL, IT = wordmark_split()
SOL = solutions_d()
SOL_BOX = path_box(SOL)


def colors(sid, ground, mode="flat"):
    """role -> fill for the symbol on a ground: dark | light | mono-dark | mono-light."""
    if ground == "mono-light":
        return {"*": MID}
    if ground == "mono-dark":
        return {"*": ICE}
    if ground == "light":
        return {"brand-1": DCYAN, "brand-2": DVIOLET, "ext-2": DBLUE, "text": NAVY, "*": NAVY}
    return {"brand-1": CYAN, "brand-2": VIOLET, "ext-2": BLUE, "text": ICE, "*": ICE}


def symbol_svg(sid, ground="dark", gradient=False, size=None, cls="sym", uid="g"):
    vb, parts = symbol_parts(sid)
    col = colors(sid, ground)
    defs = ""
    if gradient and ground == "dark":
        x0, y0, w, h = [float(v) for v in vb.split()]
        defs = (f'<defs><linearGradient id="{uid}" gradientUnits="userSpaceOnUse" x1="{x0}" y1="{y0}" x2="{x0 + w}" '
                f'y2="{y0 + h}"><stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{BLUE}"/>'
                f'<stop offset="1" stop-color="{VIOLET}"/></linearGradient></defs>')
    paths = ""
    for role, d in parts:
        fill = f"url(#{uid})" if gradient and ground == "dark" and role != "text" else col.get(role, col["*"])
        if gradient and sid == "A" and role == "brand-2":
            fill = VIOLET
        paths += f'<path d="{d}" fill="{fill}"/>'
    sz = f' width="{size}" height="{size}"' if size else ""
    return f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{sz}>{defs}{paths}</svg>'


def lockup_svg(sid, ground="dark", kind="primary", gradient=False, uid="lg"):
    """Outlined lockup. kind: primary (symbol | divider | ElIT over SOLUTIONS), compact (symbol + ElIT),
    stacked (symbol over ElIT over SOLUTIONS), wordmark (ElIT over SOLUTIONS)."""
    vb, parts = symbol_parts(sid)
    sx0, sy0, sw, sh = [float(v) for v in vb.split()]
    mono = ground.startswith("mono")
    ink = {"dark": ICE, "light": NAVY, "mono-dark": ICE, "mono-light": MID}[ground]
    itc = ink if mono else (CYAN if ground == "dark" else DCYAN)
    col = colors(sid, ground)
    wx0, wy0, ww, wh = VB_W
    cap = 100.0
    sol_w = SOL_BOX[2] - SOL_BOX[0]
    word_w = ww
    sol_scale = word_w / sol_w                      # SOLUTIONS spans the ElIT width
    sol_h = (SOL_BOX[3] - SOL_BOX[1]) * sol_scale
    gap_v = 26
    block_h = cap + gap_v + sol_h
    out, defs = [], ""

    def sym(x, y, h):
        nonlocal defs
        s = h / sh
        if gradient and not mono and ground == "dark":
            defs = (f'<linearGradient id="{uid}" gradientUnits="userSpaceOnUse" x1="{sx0}" y1="{sy0}" x2="{sx0 + sw}" y2="{sy0 + sh}">'
                    f'<stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{BLUE}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>')
        g = f'<g transform="translate({x - sx0 * s:.3f} {y - sy0 * s:.3f}) scale({s:.5f})">'
        for role, d in parts:
            fill = col.get(role, col["*"])
            if defs and role != "text" and not (sid == "A" and role == "brand-2"):
                fill = f"url(#{uid})"
            g += f'<path d="{d}" fill="{fill}"/>'
        return g + "</g>"

    def word(x, y, with_sol=True):
        g = f'<g transform="translate({x - wx0:.3f} {y:.3f})"><path d="{EL}" fill="{ink}"/><path d="{IT}" fill="{itc}"/></g>'
        if with_sol:
            g += (f'<g transform="translate({x:.3f} {y + cap + gap_v:.3f}) scale({sol_scale:.5f}) translate({-SOL_BOX[0]:.3f} {-SOL_BOX[1]:.3f})">'
                  f'<path d="{SOL}" fill="{ink}" fill-opacity="{1 if mono else .92}"/></g>')
        return g

    if kind == "primary":
        sh_ = block_h * 1.0
        sw_ = sw * sh_ / sh
        out.append(sym(0, 0, sh_))
        dx = sw_ + 46
        out.append(f'<rect x="{dx:.2f}" y="{-6}" width="3" height="{block_h + 12:.2f}" fill="{ink}" fill-opacity=".55"/>')
        out.append(word(dx + 50, 0))
        W, H, X0, Y0 = dx + 50 + word_w, block_h + 12, 0, -6
    elif kind == "compact":
        sh_ = cap * 1.25
        sw_ = sw * sh_ / sh
        out.append(sym(0, -(sh_ - cap) / 2, sh_))
        out.append(word(sw_ + 34, 0, with_sol=False))
        W, H, X0, Y0 = sw_ + 34 + word_w, sh_, 0, -(sh_ - cap) / 2
    elif kind == "stacked":
        sh_ = block_h * 1.1
        sw_ = sw * sh_ / sh
        out.append(sym((word_w - sw_) / 2, 0, sh_))
        out.append(word(0, sh_ + 60))
        W, H, X0, Y0 = max(word_w, sw_), sh_ + 60 + block_h, 0, 0
    else:
        out.append(word(0, 0))
        W, H, X0, Y0 = word_w, block_h, 0, 0
    pad = 4
    return (f'<svg class="lk" xmlns="http://www.w3.org/2000/svg" viewBox="{X0 - pad:.2f} {Y0 - pad:.2f} {W + 2 * pad:.2f} {H + 2 * pad:.2f}">'
            f'{"<defs>" + defs + "</defs>" if defs else ""}{"".join(out)}</svg>')


def app_icon(sid, style):
    """Rounded-square app tile (the tile is the platform's container, not part of the mark)."""
    bg = {"midnight": MID, "white": "#FFFFFF", "gradient": "url(#tg)", "outline": "#0B1224"}[style]
    ground = {"midnight": "dark", "white": "mono-light", "gradient": "mono-dark", "outline": "mono-dark"}[style]
    vb, parts = symbol_parts(sid)
    sx0, sy0, sw, sh = [float(v) for v in vb.split()]
    s = 62 / max(sw, sh)
    col = colors(sid, ground)
    if style == "white":
        col = {"brand-1": MID, "brand-2": VIOLET if sid == "A" else MID, "ext-2": MID, "text": MID, "*": MID}
    g = "".join(f'<path d="{d}" fill="{col.get(r, col["*"])}"/>' for r, d in parts)
    tx = 50 - (sx0 + sw / 2) * s
    ty = 48.5 - (sy0 + sh / 2) * s
    stroke = ' stroke="#2A3A66" stroke-width="1.2"' if style == "outline" else ""
    return (f'<svg class="ai" viewBox="0 0 100 100"><defs><linearGradient id="tg" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient></defs>'
            f'<rect x="1" y="1" width="98" height="98" rx="22" fill="{bg}"{stroke}/>'
            f'<g transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})">{g}</g></svg>')


def _square_vb(vb):
    x, y, w, h = [float(v) for v in vb.split()]
    side = max(w, h) * 1.08
    return f'viewBox="{x + w / 2 - side / 2:.3f} {y + h / 2 - side / 2:.3f} {side:.3f} {side:.3f}"'


def save_logo_files(d, sid):
    os.makedirs(d, exist_ok=True)
    files = {}
    for ground in ("dark", "light", "mono-dark", "mono-light"):
        for kind in ("primary", "compact", "stacked", "wordmark"):
            files[f"elit-{kind}-{ground}.svg"] = lockup_svg(sid, ground, kind)
        files[f"elit-symbol-{ground}.svg"] = symbol_svg(sid, ground)
    files["elit-primary-dark-gradient.svg"] = lockup_svg(sid, "dark", "primary", gradient=True)
    files["elit-symbol-dark-gradient.svg"] = symbol_svg(sid, "dark", gradient=True)
    for st in ("midnight", "white", "gradient", "outline"):
        files[f"app-icon-{st}.svg"] = app_icon(sid, st)
    for name, s in files.items():
        s = re.sub(r'^<svg class="[^"]*"', '<svg', s)
        write(os.path.join(d, name), s)
    import cairosvg
    sq = re.sub(r'viewBox="([^"]+)"', lambda m: _square_vb(m.group(1)), files["elit-symbol-dark.svg"], count=1)
    write(os.path.join(d, "favicon.svg"), re.sub(r'^<svg class="[^"]*"', '<svg', sq))
    for px in (16, 32, 48, 180):
        cairosvg.svg2png(url=os.path.join(d, "favicon.svg"), write_to=os.path.join(d, f"favicon-{px}.png"),
                         output_width=px, output_height=px)
    subprocess.run([PY, os.path.join(ROOT, ".claude", "skills", "logo-design", "scripts", "render_png.py"),
                    os.path.join(d, "favicon.svg"), "--ico", os.path.join(d, "favicon.ico")], check=True, capture_output=True)
    for name in ("elit-primary-dark.svg", "elit-primary-light.svg", "elit-symbol-dark.svg", "app-icon-midnight.svg"):
        cairosvg.svg2png(url=os.path.join(d, name), write_to=os.path.join(d, name[:-4] + ".png"), output_width=1600 if "primary" in name else 512)


# ============================================================================ pages

def fonts_css():
    d = os.path.join(WORK, "sets", "A")
    css, _ = site_preview.identity_fonts_css(d, json.load(open(os.path.join(d, "identity.json"))))
    return css   # 'BI display a' = Lexend (logo face), 'BI text a' = Geologica


HEAD = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Sora:wght@700'
        '&family=Moderustic:wght@700&display=block">')
BASE = """*{box-sizing:border-box;margin:0;padding:0}body{background:#080D1B;color:#F4F7FF;font-family:'BI text a',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.lk{display:block;height:var(--h,60px);width:auto}.sym{display:block;width:var(--w,60px);height:auto}.ai{display:block;width:var(--w,96px);height:var(--w,96px)}
.mono{font-family:'JetBrains Mono',monospace}"""


def website(sid):
    glow = symbol_svg(sid, "dark", gradient=True, uid="wg")
    return f"""<!doctype html><html><head><meta charset="utf-8">{HEAD}<style>{fonts_css()}{BASE}
html,body{{width:1440px;height:900px;overflow:hidden}}
.w{{position:relative;width:1440px;height:900px;background:radial-gradient(900px 600px at 82% 40%,rgba(145,116,255,.22),transparent 60%),radial-gradient(700px 500px at 70% 75%,rgba(54,217,255,.12),transparent 60%),#080D1B;overflow:hidden}}
header{{display:flex;align-items:center;padding:30px 72px;gap:40px}}nav{{display:flex;gap:30px;font-size:15px;color:#B8C2DB;margin-left:auto}}
.cta{{background:#36D9FF;color:#080D1B;padding:11px 18px;border-radius:999px;font-weight:600;font-size:14px;margin-left:16px}}
main{{position:absolute;left:72px;top:230px;width:640px}}.eb{{font-size:13px;letter-spacing:.2em;color:#8E9AB8}}
h1{{font-family:'BI text a';font-weight:700;font-size:72px;line-height:1.02;letter-spacing:-.03em;margin-top:22px}}h1 span{{color:#36D9FF}}
p{{font-size:19px;line-height:1.6;color:#B8C2DB;margin-top:24px;max-width:540px}}.b{{display:flex;gap:14px;margin-top:36px}}
.b1{{background:#36D9FF;color:#080D1B;padding:15px 24px;border-radius:999px;font-weight:600}}.b2{{border:1px solid #33456E;padding:15px 24px;border-radius:999px}}
.art{{position:absolute;right:120px;top:200px;--w:440px;filter:drop-shadow(0 0 40px rgba(54,217,255,.35)) drop-shadow(0 0 90px rgba(145,116,255,.35))}}
.svc{{position:absolute;left:72px;right:72px;bottom:54px;display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
.s{{background:#17243B;border:1px solid #22345A;border-radius:14px;padding:20px}}.s b{{display:block;font-size:17px}}.s span{{font-size:14px;color:#9AA6C4}}
.lbl{{position:absolute;right:14px;bottom:10px;font-size:11px;color:#46557A}}</style></head><body><div class="w">
<header><div style="--h:46px">{lockup_svg(sid, "dark", "primary")}</div><nav><a>Services</a><a>Products</a><a>Work</a><a>Company</a></nav><div class="cta">Start a project</div></header>
<main><div class="eb mono">SOFTWARE ENGINEERING · CYPRUS</div><h1>Digital solutions,<br><span>engineered.</span></h1>
<p>Websites, custom software, automation and integrations, designed and built in Cyprus for teams across Europe.</p>
<div class="b"><div class="b1">Start a project →</div><div class="b2">See our work</div></div></main>
<div class="art">{glow}</div>
<div class="svc">{''.join(f'<div class="s"><b>{a}</b><span>{b}</span></div>' for a, b in [("Websites","Fast, accessible web platforms"),("Custom software","Web apps and internal tools"),("Automation","Workflows without busywork"),("Integrations","Systems that talk reliably")])}</div>
<div class="lbl">Concept mock · sample copy</div></div></body></html>"""


def cards(sid):
    return f"""<!doctype html><html><head><meta charset="utf-8">{HEAD}<style>{fonts_css()}{BASE}
html,body{{width:1440px;height:820px;overflow:hidden;background:#1A1F2B}}
.desk{{position:relative;width:1440px;height:820px;background:radial-gradient(800px 500px at 50% 40%,#252C3C,#141824)}}
.c{{position:absolute;width:595px;height:385px;border-radius:10px;overflow:hidden;box-shadow:0 40px 80px -30px rgba(0,0,0,.7)}}
.f{{left:90px;top:190px;background:#080D1B}}.bk{{left:755px;top:190px;background:#F4F7FF;color:#17243B;padding:46px 52px}}
.f .lg{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);--h:120px}}
.edge{{position:absolute;right:0;top:0;bottom:0;width:6px;background:linear-gradient(#36D9FF,#9174FF)}}
.bk b{{font-size:26px;display:block;font-weight:600}}.bk span{{font-size:14px;color:#5A6688}}.ct{{position:absolute;left:52px;bottom:42px;font-size:13px;line-height:1.75}}
.bk .sm{{position:absolute;right:48px;bottom:42px;--w:54px}}.lb{{position:absolute;top:150px;font-size:12px;letter-spacing:.14em;color:#7A869F}}
.foot{{position:absolute;left:90px;bottom:120px;font-size:13px;color:#7A869F}}</style></head><body><div class="desk">
<div class="lb" style="left:90px">FRONT</div><div class="lb" style="left:755px">BACK</div>
<div class="c f"><div class="lg">{lockup_svg(sid, "dark", "primary")}</div><div class="edge"></div></div>
<div class="c bk"><b>Alex Constantinou</b><span>Founder &amp; Technical Director</span>
<div class="ct mono">+357 99 000 000<br>alex@elitsolutions.cy<br>elitsolutions.cy<br>Limassol, Cyprus</div><div class="sm">{symbol_svg(sid, "light")}</div></div>
<div class="foot">Business card · 85 × 55 mm · placeholder details · cyan-to-violet edge paint</div></div></body></html>"""


def construction(sid):
    """Construction drawing on the 100-unit grid."""
    vb, parts = symbol_parts(sid)
    grid = "".join(f'<path d="M{i} 0V100M0 {i}H100" stroke="#22345A" stroke-width=".25"/>' for i in range(0, 101, 10))
    shapes = "".join(f'<path d="{d}" fill="{c}" fill-opacity=".9"/>' for (r, d), c in zip(parts, [CYAN, VIOLET, BLUE, ICE] if sid == "A" else [ICE, CYAN, BLUE, VIOLET]))
    if sid == "A":
        notes = ('<text x="50" y="7" fill="#8E9AB8" font-size="3.2">stroke 12 · round joins</text>'
                 '<text x="40" y="40" fill="#8E9AB8" font-size="3.2">open apex</text>'
                 '<text x="2" y="62" fill="#8E9AB8" font-size="3.2">bar 12 · r 6</text>'
                 '<path d="M38 33L58 14" stroke="#36D9FF" stroke-width=".4" stroke-dasharray="1 1"/>')
    else:
        notes = ('<text x="12" y="24" fill="#8E9AB8" font-size="3.2">spine 13</text>'
                 '<text x="58" y="96" fill="#8E9AB8" font-size="3.2">slab 16 · gap 7 · slope 0.30</text>')
    return (f'<svg class="sym" viewBox="0 0 100 100" style="--w:100%;font-family:JetBrains Mono,monospace">'
            f'<rect width="100" height="100" fill="#0B1224"/>{grid}<g transform="translate(0 0)">{shapes}</g>{notes}</svg>')


INFO = {
    "A": dict(slug="forward", name="Forward", line="An E that becomes an arrow.",
              idea=("Your Forward reference, rebuilt as a letter. The two chevron arms are the E's top and bottom arms, and "
                    "the violet bar is its middle arm, running through an open apex. One stroke weight, round joins, "
                    "computed parallels. It says delivery and progress, and it still says E."),
              pros=["Clearest, most memorable silhouette of the two; very strong at 16 px.",
                    "Two colours with distinct jobs: cyan structure, violet motion.",
                    "Natural motion device for the website (the bar slides in) and for UI (next, deploy, ship)."],
              cons=["Arrows are a common category motif. Ownability rests on the open apex and the E reading, so keep "
                    "those exact and never redraw it as a plain arrow icon.",
                    "Directional: always points right, so it needs care in RTL layouts or when mirrored."],
              scale=("Products keep the chevron and change the bar colour, or the bar becomes the product's own shape. "
                     "The bar alone is a strong standalone graphic (progress lines, loaders, dividers).")),
    "B": dict(slug="layers", name="Layers", line="A system built in layers.",
              idea=("Your Layered-E reference, rebuilt on Phase 1's segmented E: a neutral spine, then three separate slabs "
                    "sheared upward for depth, stepping cyan → blue → violet. The gradient is three flat steps, so the "
                    "master prints, embroiders and works in one colour; a smooth gradient is a digital-only treatment."),
              pros=["Reads as both E and stack: an engineering, platform feel suited to a future SaaS portfolio.",
                    "The colour ramp is the identity's colour story in one mark.",
                    "Continuity with Phase 1's Signal (the same E with gaps)."],
              cons=["Busier at 16 px: four parts. The favicon holds, but it is less punchy than Forward.",
                    "Stacked or isometric layers are common in cloud and dev tools; the spine and short middle slab carry "
                    "the difference.",
                    "Three mark colours (plus neutral) need discipline in print."],
              scale=("Each product takes one slab colour or its own three-step ramp. The slab is a modular graphic "
                     "for diagrams, section dividers and charts.")),
}


BOARD_CSS = """body{width:1600px;background:#EEF0F4;color:#141A2A;font-family:'BI text a',system-ui,sans-serif}
.hero{background:radial-gradient(900px 500px at 75% 30%,rgba(145,116,255,.20),transparent 60%),#080D1B;color:#F4F7FF;padding:52px 72px 70px}
.meta{display:flex;justify-content:space-between;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#8E9AB8}
.hero h1{font-weight:700;font-size:96px;letter-spacing:-.03em;margin-top:30px}.hero .l{font-size:22px;color:#B8C2DB;margin-top:8px}
.hero .big{display:flex;justify-content:center;margin-top:64px;--h:230px}
section{padding:52px 72px;background:#fff;border-top:1px solid #DDE1EA}section:nth-of-type(odd){background:#F7F8FB}
h2{font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:#6A7590;margin-bottom:24px}h2 b{color:#141A2A;margin-right:10px}
.p{font-size:17px;line-height:1.65;color:#3A4560}.lede{font-size:22px;line-height:1.55}
.g{display:grid;gap:16px}.g2{grid-template-columns:1fr 1fr}.g3{grid-template-columns:repeat(3,1fr)}.g4{grid-template-columns:repeat(4,1fr)}
.t{border:1px solid #DDE1EA;border-radius:6px;display:flex;align-items:center;justify-content:center;min-height:230px;position:relative;padding:34px}
.t .cap{position:absolute;left:14px;bottom:10px;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#7C879F}
.dk{background:#080D1B}.nv{background:#17243B}.lt{background:#F4F7FF}.wh{background:#fff}
.dk .cap,.nv .cap{color:#7C8AAD}
.sizes{display:flex;gap:28px;align-items:flex-end}.sizes figure{display:flex;flex-direction:column;align-items:center;gap:8px;font-size:11px;color:#7C8AAD}
.sw{display:grid;grid-template-columns:repeat(6,1fr);border-radius:6px;overflow:hidden}.sw div{height:200px;padding:16px;display:flex;flex-direction:column;justify-content:flex-end;font-size:13px}
.sw b{font-size:16px}.sw code{font-family:'JetBrains Mono',monospace;margin:3px 0}
table{width:100%;border-collapse:collapse;font-size:14px;margin-top:18px}td,th{padding:9px 10px;border-bottom:1px solid #E3E6EE;text-align:left}th{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#6A7590}
.ok{color:#08795E;font-weight:600}.no{color:#B4312B;font-weight:600}
.wmx{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.wmx .t{flex-direction:column;gap:14px}
.shot{border:1px solid #DDE1EA;border-radius:6px;overflow:hidden;background:#fff}.shot img{display:block;width:100%}.shot div{padding:10px 14px;font-size:13px;color:#5A6688}
ul{list-style:none}li{font-size:15px;line-height:1.55;padding:11px 0;border-top:1px solid #DDE1EA}
.foot{padding:24px 72px;font-size:12px;color:#7C879F;display:flex;justify-content:space-between}"""


def palette_section():
    sw = [("Midnight", MID, "#F4F7FF", "Ground"), ("Navy", NAVY, "#F4F7FF", "Surfaces, cards"),
          ("Cyan", CYAN, MID, "Mark, actions"), ("Violet", VIOLET, MID, "Motion, glow"), ("Ice White", ICE, MID, "Type on dark"),
          ("Layer Blue*", BLUE, MID, "Ramp middle (computed)")]
    cells = "".join(f'<div style="background:{h};color:{fg}"><b>{n}</b><code>{h}</code><small>{u}</small></div>' for n, h, fg, u in sw)
    pairs = [("Ice White on Midnight", ICE, MID, 4.5), ("Ice White on Navy", ICE, NAVY, 4.5), ("Cyan on Midnight", CYAN, MID, 4.5),
             ("Violet on Midnight", VIOLET, MID, 4.5), ("Midnight on Cyan (button)", MID, CYAN, 4.5), ("Midnight on Violet", MID, VIOLET, 4.5),
             ("Cyan on Ice White", CYAN, ICE, 3.0), ("Violet on Ice White", VIOLET, ICE, 3.0),
             ("Deep Cyan #0A86B0 on Ice White", DCYAN, ICE, 3.0), ("Deep Violet #6A4BEB on Ice White", DVIOLET, ICE, 3.0)]
    rows = "".join(f'<tr><td>{n}</td><td class="mono">{cr(a, b):.2f}:1</td><td>{"text ≥ 4.5" if t == 4.5 else "graphic ≥ 3"}</td>'
                   f'<td class="{"ok" if cr(a, b) >= t else "no"}">{"pass" if cr(a, b) >= t else "fails: fill only, or use the deep version"}</td></tr>'
                   for n, a, b, t in pairs)
    return (f'<section><h2><b>04</b>Your palette, measured</h2><div class="sw">{cells}</div>'
            f'<table><tr><th>Pair</th><th>Contrast (WCAG 2)</th><th>Needs</th><th>Result</th></tr>{rows}</table>'
            f'<p class="p" style="margin-top:16px">Kept exactly as you specified. *Layer Blue is the only colour I added: the computed '
            f'midpoint of Cyan → Violet, used only inside the Layers mark and charts. On light grounds the mark switches to deep '
            f'versions of Cyan and Violet, because the bright ones cannot reach 3:1 on Ice White.</p></section>')


def wordmark_section():
    fam = [("Lexend Bold · proposed", "BI display a", "Slab-serifed capital I: ElIT reads correctly even in one colour."),
           ("Sora Bold · your reference", "Sora", "Flagged l reads as a 1 (\"E1IT\"). No Greek. A common AI-startup face."),
           ("Moderustic Bold · Phase 1 A", "Moderustic", "Tailed l solves it too, but it is softer and narrower than your reference.")]
    tiles = "".join(f'<div class="t dk"><div style="font-family:\'{f}\';font-weight:700;font-size:96px;line-height:1;letter-spacing:-.01em;color:#F4F7FF">'
                    f'<span>El</span><span style="color:{CYAN}">IT</span></div>'
                    f'<div style="font-family:\'{f}\';font-weight:700;font-size:96px;line-height:1;color:#F4F7FF;opacity:.9;filter:grayscale(1)">ElIT</div>'
                    f'<span class="cap">{n}</span></div>' for n, f, _ in fam)
    notes = "".join(f"<li><b>{n}:</b> {t}</li>" for n, _, t in fam)
    return (f'<section><h2><b>03</b>Wordmark: fixing "EIIT"</h2><p class="p" style="max-width:1150px;margin-bottom:22px">In your '
            f'references the name reads <b>EIIT</b>: in most geometric fonts a lowercase l and a capital I are the same bar. '
            f'Colouring IT cyan helps in colour, but the logo also has to work in one colour (stamps, engraving, fax, favicons). '
            f'Each tile shows the colour version above and the one-colour version below.</p>'
            f'<div class="wmx">{tiles}</div><ul style="margin-top:18px">{notes}</ul>'
            f'<p class="p" style="margin-top:12px">Lexend is the logo face only (outlined, Latin letters). Headlines and UI use '
            f'Geologica, which covers Greek and has tabular figures; JetBrains Mono is for code.</p></section>')


def board(sid):
    i = INFO[sid]
    out = os.path.join(R2, i["slug"])
    b = build_dir(sid)
    sizes = "".join(f'<figure><img src="logo/favicon-{s}.png" width="{s * 3}" height="{s * 3}" style="image-rendering:pixelated"><span>{s} px (×3)</span></figure>' for s in (16, 32))
    body = f"""
<div class="hero"><div class="meta"><span>ElIT Solutions · Round 2 · logo refinement on Concept A</span><span>Direction {sid} · v0.2 · 16 Nov 2026</span></div>
<h1>{i['name']}</h1><div class="l">{i['line']}</div><div class="big">{lockup_svg(sid, "dark", "primary", gradient=False)}</div></div>
<section><h2><b>01</b>Idea and construction</h2><div class="g g2" style="align-items:start"><div><p class="lede">{i['idea']}</p>
<p class="p" style="margin-top:18px">Built from primitives on a 100-unit grid and outlined with the brand-identity logo engine (no live text, no filters). Pipeline checks: 16 and 32 px renders, overlaps removed, one-colour variants.</p></div>
<div style="max-width:520px;justify-self:end;width:100%">{construction(sid)}</div></div></section>
<section><h2><b>02</b>Logo system</h2><div class="g g3">
<div class="t dk" style="grid-column:span 2"><div style="--h:150px">{lockup_svg(sid, "dark", "primary")}</div><span class="cap">Primary · on Midnight</span></div>
<div class="t dk"><div style="--w:170px">{symbol_svg(sid, "dark", gradient=True, uid="sg1")}</div><span class="cap">Symbol · digital gradient treatment</span></div>
<div class="t lt" style="grid-column:span 2"><div style="--h:150px">{lockup_svg(sid, "light", "primary")}</div><span class="cap">Primary · on Ice White (deep cyan / violet)</span></div>
<div class="t nv"><div style="--h:200px">{lockup_svg(sid, "dark", "stacked")}</div><span class="cap">Stacked · on Navy</span></div>
<div class="t dk"><div style="--h:70px">{lockup_svg(sid, "dark", "compact")}</div><span class="cap">Compact · headers</span></div>
<div class="t wh"><div style="--h:110px">{lockup_svg(sid, "mono-light", "primary")}</div><span class="cap">One colour · Midnight</span></div>
<div class="t dk"><div style="--h:110px">{lockup_svg(sid, "mono-dark", "primary")}</div><span class="cap">One colour · Ice White</span></div>
<div class="t dk"><div style="display:flex;gap:18px">{''.join(f'<div style="--w:96px">{app_icon(sid, st)}</div>' for st in ("midnight", "white", "gradient", "outline"))}</div><span class="cap">App icons</span></div>
<div class="t dk"><div class="sizes">{sizes}<figure><div style="--w:96px">{symbol_svg(sid, "dark")}</div><span>flat master</span></figure></div><span class="cap">Favicon renders (16 / 32 px, from the master)</span></div>
<div class="t lt"><div style="--w:150px">{symbol_svg(sid, "light")}</div><span class="cap">Symbol · light ground</span></div>
</div></section>
{wordmark_section()}{palette_section()}
<section><h2><b>05</b>In use</h2><div class="shot"><img src="website.png"><div>Website hero · concept mock (not the website build)</div></div>
<div class="g g2" style="margin-top:16px"><div class="shot"><img src="business-card.png"><div>Business card · front and back</div></div>
<div class="shot" style="background:#080D1B;display:flex;align-items:center;justify-content:center;gap:26px;min-height:360px"><div style="--w:120px">{app_icon(sid, "midnight")}</div><div style="--w:120px">{app_icon(sid, "gradient")}</div><div style="color:#B8C2DB;font-size:15px;line-height:1.6;max-width:220px">App icon on a device grid. The tile is the platform's container, not part of the logo.</div></div></div></section>
<section><h2><b>06</b>Assessment</h2><div class="g g3"><div><h3>Strengths</h3><ul>{''.join(f'<li>{x}</li>' for x in i['pros'])}</ul></div>
<div><h3>Risks</h3><ul>{''.join(f'<li>{x}</li>' for x in i['cons'])}</ul></div><div><h3>Umbrella scalability</h3><ul><li>{i['scale']}</li></ul></div></div></section>
<div class="foot"><span>ElIT Solutions · Round 2 · {i['name']}</span><span>Draft for review, not final artwork</span></div>"""
    return f'<!doctype html><html><head><meta charset="utf-8">{HEAD}<style>{fonts_css()}{BASE}{BOARD_CSS}</style></head><body>{body}</body></html>'


def comparison():
    cols = ""
    for sid in ("A", "B"):
        i = INFO[sid]
        cols += f"""<div class="col"><div class="hd"><span>{sid} · {i['name']}</span><small>{i['line']}</small></div>
<div class="big">{lockup_svg(sid, "dark", "primary")}</div>
<div class="row">{''.join(f'<div style="--w:110px">{app_icon(sid, st)}</div>' for st in ("midnight", "white", "gradient", "outline"))}</div>
<div class="row2"><div class="lt"><div style="--h:70px">{lockup_svg(sid, "light", "compact")}</div></div><div class="mn"><div style="--h:70px">{lockup_svg(sid, "mono-dark", "compact")}</div></div>
<div class="fv"><img src="../{i['slug']}/logo/favicon-16.png" width="48" height="48" style="image-rendering:pixelated"><span>16 px</span></div></div>
<img class="shot" src="../{i['slug']}/website.png"><img class="shot" src="../{i['slug']}/business-card.png">
<ul>{''.join(f'<li>+ {x}</li>' for x in i['pros'][:2])}{''.join(f'<li>− {x}</li>' for x in i['cons'][:1])}</ul></div>"""
    sw = "".join(f'<div style="background:{h}"><b>{n}</b><code>{h}</code></div>' for n, h in [("Midnight", MID), ("Navy", NAVY), ("Cyan", CYAN), ("Violet", VIOLET), ("Ice White", ICE)])
    css = """body{width:1600px;background:#080D1B}.top{padding:44px 60px 26px;color:#F4F7FF}.top h1{font-size:40px;letter-spacing:-.02em}.top p{color:#9AA6C4;font-size:16px;margin-top:8px;max-width:1100px;line-height:1.5}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:0 60px}.col{border:1px solid #1F2C4A;border-radius:14px;padding:28px;background:#0B1224}
.hd{display:flex;align-items:baseline;gap:16px;color:#F4F7FF}.hd span{background:#36D9FF;color:#080D1B;padding:6px 14px;border-radius:999px;font-weight:700;font-size:15px}.hd small{color:#9AA6C4;font-size:15px}
.big{padding:48px 10px;display:flex;justify-content:center;--h:150px}.row{display:flex;gap:18px;justify-content:center;padding:6px 0 22px}
.row2{display:grid;grid-template-columns:1.3fr 1.3fr .6fr;gap:12px;margin-bottom:16px}.row2>div{border-radius:10px;display:flex;align-items:center;justify-content:center;padding:22px;min-height:120px}
.row2 .lt{background:#F4F7FF}.row2 .mn{background:#17243B}.fv{flex-direction:column;gap:8px;background:#080D1B;border:1px solid #1F2C4A;color:#7C8AAD;font-size:11px}
.shot{width:100%;display:block;border-radius:8px;margin-top:12px;border:1px solid #1F2C4A}ul{list-style:none;margin-top:14px}li{color:#C9D1E6;font-size:14px;line-height:1.5;padding:8px 0;border-top:1px solid #1F2C4A}
.pal{display:grid;grid-template-columns:repeat(5,1fr);margin:24px 60px 0;border-radius:10px;overflow:hidden}.pal div{height:90px;padding:12px;display:flex;flex-direction:column;justify-content:flex-end;font-size:13px;color:#F4F7FF}
.pal div:nth-child(n+3){color:#080D1B}.pal code{font-family:'JetBrains Mono',monospace;font-size:12px}.foot{padding:22px 60px 40px;color:#5D6A8A;font-size:12px}"""
    return (f'<!doctype html><html><head><meta charset="utf-8">{HEAD}<style>{fonts_css()}{BASE}{css}</style></head><body>'
            f'<div class="top"><h1>ElIT Solutions · Round 2 · Forward vs Layers</h1><p>Concept A\'s system with your palette and your two reference '
            f'ideas, rebuilt as precise, original marks. The wordmark is fixed so ElIT never reads as EIIT. Both are proposals; nothing is final.</p></div>'
            f'<div class="grid">{cols}</div><div class="pal">{sw}</div><div class="foot">Outlined with the brand-identity logo engine; favicons rendered by the pipeline. '
            f'Mocks use sample copy and placeholder contact details.</div></body></html>')


def main():
    for sid in ("A", "B"):
        i = INFO[sid]
        out = os.path.join(R2, i["slug"])
        print(sid, i["name"])
        save_logo_files(os.path.join(out, "logo"), sid)
        for name, fn, w, h in (("website", website, 1440, 900), ("business-card", cards, 1440, 820)):
            p = os.path.join(out, f"{name}.html")
            write(p, fn(sid))
            render(p, os.path.join(out, f"{name}.png"), w, h)
        p = os.path.join(out, "board.html")
        write(p, board(sid))
        render(p, os.path.join(out, "board.png"), 1600, 1000, full=True)
    p = os.path.join(R2, "comparison", "comparison.html")
    write(p, comparison())
    render(p, os.path.join(R2, "comparison", "comparison.png"), 1600, 1000, full=True)


if __name__ == "__main__":
    main()
