# Vendored Agent Skills

These skills were copied in by hand because `/plugin` commands are not available in Claude Code on the web.
Claude Code loads them from `.claude/skills/<name>/SKILL.md`.

| Skill | Upstream | Commit | License |
|---|---|---|---|
| `logo-design` | https://github.com/kaankiziltug/logo-design-skill (`skills/logo-design/`) | `e9eaddc07895575253d6663320354a708f53e955` | MIT, see `logo-design/LICENSE` |
| `brand-identity` | https://github.com/fatihaydost/brand-identity-skill (`skills/brand-identity/`) | `af7ba40fe067b8b4aaeb2af90ed6c8996d014791` | MIT, see `brand-identity/LICENSE` and `THIRD_PARTY_NOTICES.md` |

All copied files are byte-identical to upstream. Folder layout is unchanged, so the relative paths the skills use
(`scripts/`, `references/`, `templates/`, `assets/`) still resolve.

## What was left out

- `logo-design/assets/library/svg/` (1,432 third-party logo SVGs, about 12 MB) and `assets/library/gallery.html`,
  which only displays those SVGs. The library metadata (`catalog.json`, `classifications.json`, `stats.json`) is kept,
  so library searches, `--summary` and the complexity percentiles in `svg_audit.py` still work.
- Development files from both repos: tests, evals (including `brand-identity/evals/`), CI workflows, docs images,
  plugin manifests and maintainer tools.

## Added from the repo roots

- `logo-design/LICENSE`, `logo-design/TRADEMARKS.md`
- `brand-identity/requirements.txt` (the dependency loader `scripts/pydeps.py` looks for it next to the skill),
  `brand-identity/THIRD_PARTY_NOTICES.md`, `brand-identity/TRADEMARKS.md`

## Dependencies

- **logo-design**: Python 3 standard library only. PNG output needs one renderer: `cairosvg`, `rsvg-convert`,
  Inkscape or Chrome/Chromium.
- **brand-identity**: Python 3 plus `fonttools[woff]`, `uharfbuzz` and `skia-pathops` (`requirements.txt`), and
  Chrome/Chromium for renders. If `uv` is on PATH and packages are missing, the scripts re-run themselves through
  `uv run --with-requirements requirements.txt`, which downloads those packages from PyPI into uv's cache.
  Font lookups download files from Google Fonts (`raw.githubusercontent.com/google/fonts`, `fonts.googleapis.com`).

## Known limitations without the SVG library

- `search_library.py --format paths` prints paths to SVGs that do not exist here.
- `preview_sheet.py --refs-industry …` fails with `FileNotFoundError`. Pass your own competitor files with `--refs`
  instead.
- `references/library-guide.md` mentions files under `assets/library/svg/` that are not included.

To restore the library, copy `skills/logo-design/assets/library/svg/` and `gallery.html` from the upstream commit
above into `logo-design/assets/library/`.
