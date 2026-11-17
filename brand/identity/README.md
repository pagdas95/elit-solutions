# ElIT Solutions: brand identity v1.0 (release candidate)

The client's **Layered E** kit (Nov 2026), refined. Same idea, silhouette and palette, rebuilt so it's exact,
reproducible and measured. Still a release candidate: two decisions are open (see the end).

## What's here

| Path | Contents |
|---|---|
| `board/brand-board.png` | One-page brand board (dark-first), in the layout of the client kit |
| `board/refinement.png` | Before/after: what changed in the mark, wordmark, colour and type, and why |
| `board/mock-*.png` | Website hero, phone splash, business card (sample copy, placeholder details) |
| `elit-solutions/kit/A/elit-solutions-guidelines.pdf` | 13-page guidelines from the brand-identity skill (logo, clear space, minimum sizes, misuse, colour, type, grid, dark mode, accessibility, iconography, imagery) |
| `elit-solutions/kit/A/tokens/` | Design tokens (CSS, JSON, Tailwind, palette files) |
| `logo/svg`, `logo/png` | Every lockup (primary · compact · stacked · wordmark · symbol) in every colourway (dark · light · mono-white · mono-midnight · mono-black · dark-gradient) |
| `logo/app-icon`, `logo/favicon` | App icons (midnight, navy, white, gradient) at 1024 px; favicon SVG (adapts to light/dark), ICO, PNG 16–512 |
| `reference/` | The client's original kit images, kept for comparison |
| `tools/` | `mark.py` (isometric geometry), `write_sets.py`, `patch_palette.py`, `package.py` |

## The system in one paragraph

**Mark:** three slabs on a true 30° isometric lattice, with one gap (2 units) between all slabs and both fold notches
at 1.5 units. **Wordmark:** "ElIT" in Lexend Bold (outlined). Its slab-serifed capital I keeps it from reading as
"EIIT". "IT" is in Cyan, and "SOLUTIONS" is in Lexend Light, outlined. **Colour:** Midnight `#080D1B`, Navy `#17243B`,
Cyan `#36D9FF`, Layer Blue `#5FA2FF`, Violet `#9174FF`, Ice White `#F4F7FF`. On light grounds the mark uses Deep Cyan
`#0A86B0`, Deep Blue `#2F6BE0` and Deep Violet `#6A4BEB` (all ≥ 3:1 on Ice White). **Type:** Lexend (logo only),
Geologica (headings and UI; Greek and tabular figures), JetBrains Mono (code). The gradient and glow are digital
treatments; the master is flat.

## Rebuild

```bash
.venv/bin/python brand/identity/tools/write_sets.py
.venv/bin/python .claude/skills/brand-identity/scripts/brand.py build brand/identity/elit-solutions
.venv/bin/python brand/identity/tools/patch_palette.py
.venv/bin/python .claude/skills/brand-identity/scripts/brand.py kit brand/identity/elit-solutions/sets/A --full
.venv/bin/python brand/identity/tools/package.py
```

## Known limits

- The guidelines PDF's dark-mode page shows the one-colour logo. The kit template tests the light-ground tones on
  dark grounds. Use the full-colour dark lockup (`logo/svg/elit-primary-dark.svg`) on Midnight, as on the brand board.
- Geologica draws l and I alike, so in running text "ElIT" can look like "EIIT". The logo is unaffected; in UI
  headings, prefer the logo or "ElIT Solutions" set in Lexend.
- Print colours: ask the printer for CMYK/Pantone matches against the Lab values in the guidelines.

## Open decisions (client)

1. Wordmark face: Lexend (proposed, reads ElIT in one colour) or Sora as in the client kit (reads "E1IT"/"EIIT").
2. Palette: the typed palette above (used here) or the client kit's swatches (#0A0F1F / #06B6D4 / #8B5CF6 / #F8FAFC,
   which are Tailwind defaults).
