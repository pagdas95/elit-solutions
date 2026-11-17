# ElIT Solutions: final brand identity (v1.0)

**Chosen: Layered E**, the client's layered E refined on an isometric lattice. Approved by the client on
17 Nov 2026 by confirming the guidelines PDF in this folder, with no further design changes. This folder is the source
of truth; everything else under `brand/` is exploration or source material.

## The identity

- **Symbol:** an isometric E of three slabs stepping Cyan → Layer Blue → Violet. Every edge is on the 30° grid, there
  is one gap (2 lattice units) between all slabs, and both fold notches are 1.5 units.
- **Wordmark:** "ElIT" in Lexend Bold, outlined, with "IT" in Cyan. Its slab-serifed capital I keeps it from reading
  "EIIT". "SOLUTIONS" is outlined Lexend Light.
- **Colour:** Midnight `#080D1B`, Navy `#17243B`, Cyan `#36D9FF`, Layer Blue `#5FA2FF`, Violet `#9174FF`, Ice White
  `#F4F7FF`. On light grounds the mark uses Deep Cyan `#0A86B0`, Deep Blue `#2F6BE0` and Deep Violet `#6A4BEB`
  (all ≥ 3:1 on Ice White).
- **Type:** Lexend (logo only), Geologica (headings, UI, Greek, tabular figures), JetBrains Mono (code). All SIL OFL 1.1.
- The master is flat colour; the gradient and glow are digital treatments only.

## Files

| Path | Contents |
|---|---|
| `guidelines/ElIT-Solutions-Brand-Guidelines.pdf` | The approved 13-page guidelines (identical to the client-confirmed PDF) |
| `guidelines/pages/`, `guidelines/fonts.md` | Each page as PNG; font sources, licences and embed links |
| `logo/svg/`, `logo/png/` | Every lockup (primary with SOLUTIONS · compact · stacked · wordmark · symbol) in every colourway (dark · light · mono-white · mono-midnight · mono-black · dark-gradient) |
| `logo/app-icon/`, `logo/favicon/` | App icons (midnight, navy, white, gradient) at 1024 px; favicon SVG (adapts to light/dark), ICO, PNG 16–512 |
| `logo/kit-variants/` | The guideline kit's logo variants (full colour, on dark, one colour, 16/32 px cuts) |
| `tokens/` | `tokens.css`, `tokens.scss`, `tokens.dtcg.json`, `tailwind.palette.js`, `palette.gpl`, `fonts.css`, `palette.json` |
| `presentation/` | Brand board, refinement sheet (before/after) and mocks: website, phone, business card (sample copy, placeholder details) |
| `reference/` | The client's original kit images |

## Rebuild

Source and tools: `brand/identity/`. Run:

```bash
.venv/bin/python brand/identity/tools/write_sets.py
.venv/bin/python .claude/skills/brand-identity/scripts/brand.py build brand/identity/elit-solutions
.venv/bin/python brand/identity/tools/patch_palette.py
.venv/bin/python .claude/skills/brand-identity/scripts/brand.py kit brand/identity/elit-solutions/sets/A --full
.venv/bin/python brand/identity/tools/package.py
```

Then copy the outputs here.

## Notes

- On Midnight, use the full-colour dark lockup (`logo/svg/elit-primary-dark.svg`). The guidelines' dark-mode page
  shows the one-colour version because of a kit template limitation.
- In running text set in Geologica, "ElIT" can look like "EIIT" (l and I are alike). Use the logo, or set the name in Lexend.
- Print colours: ask the printer for CMYK/Pantone matches against the Lab D50 values in the guidelines.
