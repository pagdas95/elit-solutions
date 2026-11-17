# ElIT Solutions: brand identity, Phase 1 concepts

Three different identity directions for review. **Nothing here is final.** No logo, palette or typeface has been approved.

| | Concept | Idea | Logo | Type | Palette |
|---|---|---|---|---|---|
| **A** | **Signal** (recommended) | ElIT is spelled only with straight bars. A segmented E with one lit "signal" bar. | Symbol + wordmark | Moderustic / Geologica / JetBrains Mono | Midnight `#0B1531`, Ion Cyan `#3DDCF4`, Aurora Violet `#8B7BFF` |
| **B** | **Frame** | Chamfered brackets hold an ember core: the frame every product is built in. | Symbol + wordmark | Tektur / Sofia Sans | Concrete `#F1F1EE`, Graphite `#17191F`, Ember `#FF5A1F` |
| **C** | **Edition** | A high-contrast serif wordmark in cobalt with an overline above IT. | Wordmark only | Noto Serif Display / Noto Sans | Porcelain `#F7F7F4`, Ink `#0E1124`, Cobalt `#1838C9`, Signal Mint `#5EF0C0` |

## Where to look

- `comparison/comparison.png`: all three side by side.
- `<concept>/board.png`: the full board for each concept: strategy, logo system, explorations, colour, type, patterns,
  product sub-brands, applications, strengths and weaknesses.
- `<concept>/website.png`, `app.png`, `business-card.png`: application mocks at full size (sample copy and data,
  placeholder names; not the website build).
- `<concept>/logo/`: outlined SVG masters, colour and one-colour variants, favicons and app icon.
- `<concept>/palette.json`, `pattern.svg`: palette tokens (OKLCH scales, light and dark roles) and the pattern.

## How it was made

- `elit-solutions/`: the brand-identity skill's work folder (brief, `sets.json`, audits, logo builds, review
  board `review.png`, generic mock pages in `site/`).
- `tools/write_sets.py` writes the three concepts into `sets.json`; `tools/details.json` holds the wordmark
  details measured from the first logo rounds.
- `tools/boards.py` builds the custom boards and mocks from the pipeline's outlines, palettes and fonts.

Rebuild (after `uv venv .venv && uv pip install --python .venv/bin/python -r requirements-design.txt`):

```bash
.venv/bin/python brand/concepts/tools/write_sets.py
.venv/bin/python .claude/skills/brand-identity/scripts/brand.py logos brand/concepts/elit-solutions
.venv/bin/python .claude/skills/brand-identity/scripts/brand.py build brand/concepts/elit-solutions
.venv/bin/python brand/concepts/tools/boards.py
```

All three concepts pass the pipeline gates: text contrast, English and Greek glyph coverage, OFL font licences, and
logo renders at 16 and 32 px. Warnings (accent colours below 3:1 used as fills only) are listed in
`elit-solutions/table.md`.

> **Decision (17 Nov 2026):** Concept A, Signal, was chosen as final with no further changes. Deliverables: `brand/final/`.
