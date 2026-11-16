# Elit Solutions

## Overview

_Add a short description of the project here._

## Getting Started

_Add setup and installation steps here._

### Design skills environment

The `logo-design` and `brand-identity` skills in `.claude/skills/` need a few Python packages (CairoSVG for PNG
renders, plus fontTools, uharfbuzz and skia-pathops). Install them into an isolated venv (`.venv/` is gitignored):

```bash
uv venv .venv && uv pip install --python .venv/bin/python -r requirements-design.txt
```

Run the skill scripts with `.venv/bin/python` (for example
`.venv/bin/python .claude/skills/logo-design/scripts/render_png.py --which` should list `cairosvg`).
CairoSVG uses the system `libcairo2`. HTML screenshots and the brand kit use Chrome/Chromium.

## License

Proprietary. Copyright (c) 2026 Elit Solutions. All rights reserved. See [LICENSE](LICENSE).
