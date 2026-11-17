#!/usr/bin/env python3
"""After `brand.py build`, pin the mark colours' dark-ground values to the client's exact hexes.

The mark uses extended colours whose `hex` is the light-ground (deep, >= 3:1 on Ice White) tone and whose
`dark.hex` is the brand colour used on Midnight/Navy. palette_build derives dark tones itself; this restores the
exact brand values. Run before `brand.py kit`.
"""
import json
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "elit-solutions", "sets", "A", "palette.json")
DARK = {"Midnight": "#080D1B", "Navy": "#17243B", "Deep Cyan": "#36D9FF", "Deep Blue": "#5FA2FF", "Deep Violet": "#9174FF"}
pal = json.load(open(P))
for x in pal.get("extended", []):
    if x["name"] in DARK:
        x.setdefault("dark", {})["hex"] = DARK[x["name"]].lower()
        x["dark"]["on"] = "#080d1b"
json.dump(pal, open(P, "w"), indent=2, ensure_ascii=False)
print("patched:", [(x["id"], x["name"], x["hex"], x["dark"]["hex"]) for x in pal["extended"]])
