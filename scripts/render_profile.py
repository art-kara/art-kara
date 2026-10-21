#!/usr/bin/env python3
"""Generate the editorial profile header and README with the standard library.

Edit profile.json, then run python3 scripts/render_profile.py.
The illustration is a projected trefoil curve. No portrait or remote asset is used.
"""
from html import escape
import json
from math import cos, sin, pi
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / 'profile.json').read_text())
THEMES = {
    'dark': dict(bg='#1c1c1a', ink='#f5f0e8', muted='#b0a99c', line='#48453d', accent='#f38963'),
    'light': dict(bg='#f5f1e9', ink='#27251f', muted='#70695d', line='#d6cfc2', accent='#c94d28'),
}


def trefoil(offset):
    """A continuous knot projected obliquely, with parallel strands."""
    points = []
    for i in range(721):
        t = i / 720 * 2 * pi
        r = 2 + cos(3 * t) + offset
        x, y, z = r * cos(2 * t), r * sin(2 * t), sin(3 * t)
        u = x * cos(.38) - y * sin(.38)
        v = x * sin(.38) + y * cos(.38)
        projected_y = v * cos(.82) - z * sin(.82)
        points.append((867 + u * 48, 189 + projected_y * 48))
    return 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in points) + ' Z'


def render(theme):
    c = THEMES[theme]
    strands = '\n'.join(
        f'<path d="{trefoil(i * .038)}" stroke-width="{1.0 if i % 4 == 0 else .65}" opacity="{.9 if i % 4 == 0 else .5}"/>'
        for i in range(-8, 9)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="380" viewBox="0 0 1120 380" role="img" aria-labelledby="title desc">
  <title id="title">{escape(PROFILE['name'])}</title>
  <desc id="desc">Founder, engineer, builder. A typographic cover with an original mathematical trefoil drawing.</desc>
  <rect width="1120" height="380" fill="{c['bg']}"/>
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" fill="{c['muted']}" font-size="12" letter-spacing="1.8">
    <text x="44" y="35">ART-KARA</text>
    <text x="1076" y="35" text-anchor="end">A WORK IN PROGRESS, ALWAYS.</text>
  </g>
  <path d="M44 55H1076" stroke="{c['line']}"/>
  <g font-family="Georgia, 'Times New Roman', serif" fill="{c['ink']}" letter-spacing="-5">
    <text x="40" y="174" font-size="126">Artur</text>
    <text x="39" y="288" font-size="110">Karapetian<tspan fill="{c['accent']}">.</tspan></text>
  </g>
  <g fill="none" stroke="{c['accent']}" stroke-linecap="round" stroke-linejoin="round">{strands}</g>
  <path d="M44 327H1076" stroke="{c['line']}"/>
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="12" letter-spacing="1.6">
    <text x="44" y="355" fill="{c['ink']}">FOUNDER / ENGINEER / BUILDER</text>
    <text x="1076" y="355" text-anchor="end" fill="{c['muted']}">MATH → IDEAS → WORKING THINGS</text>
  </g>
</svg>
'''


for theme in THEMES:
    (ROOT / f'{theme}_mode.svg').write_text(render(theme))
now = '\n'.join(f'- **[{p["name"]}]({p["url"]})** — {p["description"]}' for p in PROFILE['now'])
links = ' &nbsp; / &nbsp; '.join(f'<a href="{escape(url, quote=True)}">{escape(label)}</a>' for label, url in PROFILE['links'])
(ROOT / 'README.md').write_text(f'''<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/art-kara/art-kara/main/dark_mode.svg?v=editorial-1">
  <img src="https://raw.githubusercontent.com/art-kara/art-kara/main/light_mode.svg?v=editorial-1" width="100%" alt="Artur Karapetian — founder, engineer, builder.">
</picture>

{PROFILE['bio']}

### These days

{now}

### Earlier chapters

{PROFILE['before']}

---

{links}

<!-- Edit profile.json, then run python3 scripts/render_profile.py. -->
''')
print('Rendered both header themes and README.md')
