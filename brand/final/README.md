# ElIT Solutions: final brand identity (v1.0)

**Chosen direction: Signal** (Phase 1, Concept A), approved by the client on 17 Nov 2026 with no further design
changes. This folder is the source of truth; everything else under `brand/` is exploration.

## The identity

- **Symbol:** a segmented E. A stem and three arms that never touch, with the middle arm lit in Ion Cyan:
  precise modules plus one live signal.
- **Wordmark:** "ElIT" in Moderustic Bold, outlined. Its tailed lowercase l keeps the name from reading "EIIT".
- **Colour:** Midnight `#0B1531` (ground), Ion Cyan `#3DDCF4` (the signal, actions), Aurora Violet `#8B7BFF` (glows
  and charts only, never text), Cloud `#F1F3F7` (type on dark). Cyan is a fill colour on light grounds, never text.
- **Type:** Moderustic (logo and display), Geologica (text, UI, Greek, tabular figures), JetBrains Mono (code and data).
  All are SIL OFL 1.1.

## Files

| Path | Contents |
|---|---|
| `guidelines/ElIT-Solutions-Brand-Guidelines.pdf` | 13-page guidelines: idea, logo, clear space, versions, minimum sizes (20 px / 7 mm), logo on colour, misuse, colours (HEX/RGB/OKLCH/Lab), typography, applications, grid, dark mode, accessibility, iconography, imagery |
| `guidelines/pages/` | Each guideline page as PNG |
| `guidelines/fonts.md` | Font sources, licences and embed links |
| `logo/variants/` | Production files: primary, horizontal and stacked lockups, symbol, wordmark, full colour, on dark, one colour, small-size cuts (16/32 px), favicons, app icon (SVG + PNG) |
| `logo/masters/` | Outlined masters and colour variants from the concept build |
| `logo/favicon.ico` | 16/32/48 px |
| `logo/pattern-segment-field.svg` | The supporting pattern (bars on the symbol's grid) |
| `tokens/` | `tokens.css`, `tokens.scss`, `tokens.dtcg.json`, `tailwind.palette.js`, `palette.gpl`, `fonts.css`, `palette.json` |
| `presentation/` | Brand board and mocks (website, app, business card; sample copy and placeholder details) |

## Rebuild

The design is defined in `brand/concepts/tools/write_sets.py` (set A). To regenerate:

```bash
.venv/bin/python brand/concepts/tools/write_sets.py
.venv/bin/python .claude/skills/brand-identity/scripts/brand.py build brand/concepts/elit-solutions --sets A
.venv/bin/python .claude/skills/brand-identity/scripts/brand.py kit brand/concepts/elit-solutions/sets/A --full
```

Then copy `brand/concepts/elit-solutions/kit/A/` into this folder.

## Notes

- Print colours: ask the printer for CMYK/Pantone matches against the Lab D50 values in the guidelines.
- The horizontal lockup repeats the E (symbol plus wordmark). Use the symbol alone for app icons and avatars, and the
  wordmark alone in small text.
