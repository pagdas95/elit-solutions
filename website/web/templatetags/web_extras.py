"""Brand-native icons: three mini isometric slabs (the mark's construction), one or two lit per service."""
import math

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

C = math.cos(math.radians(30))
LIT = {"web": (0,), "software": (1,), "automation": (2,), "integration": (0, 2)}
COLS = ("#36D9FF", "#5FA2FF", "#9174FF")


def _slab(a0, b0, la, lb):
    pts = [(a0, b0), (a0 + la, b0), (a0 + la, b0 + lb), (a0, b0 + lb)]
    return " ".join(f"{(a + b) * C:.2f},{(b - a) * 0.5:.2f}" for a, b in pts)


@register.simple_tag
def slab_icon(kind, size=56):
    lit = LIT.get(kind, (0,))
    polys = []
    for i, (a0, b0) in enumerate(((0, 0), (-2.2, 4.4), (-4.4, 8.8))):
        fill = COLS[i] if i in lit else "rgba(244,247,255,.16)"
        polys.append(f'<polygon points="{_slab(a0, b0, 9, 3.2)}" fill="{fill}"/>')
    return mark_safe(f'<svg class="slab-icon" width="{size}" height="{size}" viewBox="-0.5 -5.5 15.5 15" aria-hidden="true">'
                     + "".join(polys) + "</svg>")
